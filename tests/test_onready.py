"""Tests for bot.sync_slash_commands.

The actual logic was extracted from MyClient.on_ready into a free
function (sync_slash_commands) so we can test it without running
the full Discord client. This test imports the real function and
asserts the call sequence.

Regression target: the "doubled-up commands" bug. Pre-PR #11, the bot
iterated client.guilds and called tree.sync(guild=guild) for each,
which copied every global command into the guild's per-guild list.
After PR #11 stopped that, the per-guild copies persisted (Discord
stores them independently of the global list). The fix: explicitly
delete per-guild commands via tree.clear_commands + tree.sync.
"""

import sys
import unittest.mock as m
from pathlib import Path

import pytest

# Stub project-specific modules that aren't needed for these tests.
# Keep discord, dotenv, yaml, etc. as real imports (they're installed
# via requirements-dev.txt or via the regular install).
sys.modules.setdefault("loggingChannel", m.MagicMock())
sys.modules.setdefault("fileManager", m.MagicMock())
sys.modules.setdefault("minecraftrcon", m.MagicMock())
sys.modules.setdefault("twitch", m.MagicMock())
sys.modules.setdefault("zapier_commands", m.MagicMock())
sys.modules.setdefault("r2loadout", m.MagicMock())
sys.modules.setdefault("react", m.MagicMock())
sys.modules.setdefault("russianroulette", m.MagicMock())

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(scope="module")
def bot_module():
    """Import bot.py once per test module and return its namespace.

    bot.py calls client.run(TOKEN) at the bottom, which would try to
    connect to Discord. We strip that line before exec so we can
    import the module safely.
    """
    bot_path = Path(__file__).resolve().parent.parent / "bot.py"
    source = bot_path.read_text()
    # Strip the bottom line that triggers a real Discord connection.
    cleaned_source = source.replace("client.run(TOKEN)", "pass  # mocked")
    ns = {"__name__": "bot_test", "__file__": str(bot_path)}
    exec(compile(cleaned_source, str(bot_path), "exec"), ns)
    return ns


def make_tree_mock(num_global_commands=25):
    """Build a MagicMock that mimics discord.app_commands.CommandTree."""
    tree = m.MagicMock()
    tree.sync = m.AsyncMock()
    tree.sync.side_effect = lambda *, guild=None: (
        [m.MagicMock(id=f"global-{i}") for i in range(num_global_commands)]
        if guild is None
        else []  # per-guild sync after clear_commands sends empty list
    )
    tree.clear_commands = m.MagicMock()
    return tree


def make_guilds(*guild_ids):
    """Build a list of guild-like MagicMocks with the given IDs."""
    return [m.MagicMock(id=gid) for gid in guild_ids]


class TestClientEventHandlers:
    """Tests that Discord event handlers are actually registered on MyClient."""

    def test_myclient_overrides_on_message(self, bot_module):
        """Regression: on_message must be a MyClient method, not nested elsewhere.

        PR #18 accidentally left on_message indented inside sync_slash_commands
        after a return statement. The bot stayed online and slash commands still
        worked, but ambient trigger words stopped entirely because Discord never
        called our on_message logic.
        """
        import discord

        my_client = bot_module["MyClient"]
        base_on_message = getattr(discord.Client, "on_message", None)
        assert my_client.on_message is not base_on_message
        assert my_client.on_message.__qualname__ == "MyClient.on_message"


class TestSyncSlashCommands:
    """Tests for sync_slash_commands — the slash-command sync logic."""

    async def test_returns_global_count_and_guild_count(self, bot_module):
        sync_slash_commands = bot_module["sync_slash_commands"]
        tree = make_tree_mock(num_global_commands=25)
        guilds = make_guilds(1, 2, 3)

        result = await sync_slash_commands(tree, guilds)

        assert result == (25, 3), f"Expected (25, 3), got {result}"

    async def test_calls_global_sync_first(self, bot_module):
        """First sync call must be global (no guild kwarg)."""
        sync_slash_commands = bot_module["sync_slash_commands"]
        tree = make_tree_mock()
        guilds = make_guilds(1, 2)

        await sync_slash_commands(tree, guilds)

        first_call = tree.sync.call_args_list[0]
        assert "guild" not in first_call.kwargs, \
            f"First sync should be global, got kwargs={first_call.kwargs}"

    async def test_clears_per_guild_for_each_guild(self, bot_module):
        """tree.clear_commands must be called once per guild."""
        sync_slash_commands = bot_module["sync_slash_commands"]
        tree = make_tree_mock()
        guilds = make_guilds(100, 200, 300, 400, 500)

        await sync_slash_commands(tree, guilds)

        assert tree.clear_commands.call_count == 5, \
            f"Expected 5 clear_commands calls, got {tree.clear_commands.call_count}"

        for call in tree.clear_commands.call_args_list:
            assert "guild" in call.kwargs, \
                f"clear_commands must take guild kwarg, got {call}"

    async def test_per_guild_sync_uses_guild_kwarg(self, bot_module):
        """Each per-guild sync call must pass guild=... (not global)."""
        sync_slash_commands = bot_module["sync_slash_commands"]
        tree = make_tree_mock()
        guilds = make_guilds(42)

        await sync_slash_commands(tree, guilds)

        assert tree.sync.call_count == 2
        per_guild_call = tree.sync.call_args_list[1]
        assert "guild" in per_guild_call.kwargs, \
            f"Per-guild sync must use guild= kwarg, got {per_guild_call}"

    async def test_no_guilds_skips_per_guild_loop(self, bot_module):
        """If bot is in no guilds, only the global sync happens."""
        sync_slash_commands = bot_module["sync_slash_commands"]
        tree = make_tree_mock()
        guilds = []

        await sync_slash_commands(tree, guilds)

        assert tree.sync.call_count == 1, "Only global sync should happen"
        assert tree.clear_commands.call_count == 0, \
            "No clear_commands when there are no guilds"

    async def test_global_sync_happens_before_per_guild_clears(self, bot_module):
        """Global sync must happen before per-guild clears (order matters)."""
        sync_slash_commands = bot_module["sync_slash_commands"]
        tree = make_tree_mock()
        guilds = make_guilds(1, 2)

        await sync_slash_commands(tree, guilds)

        first_sync = tree.sync.call_args_list[0]
        first_clear = tree.clear_commands.call_args_list[0]

        # First sync was global (no guild kwarg)
        assert "guild" not in first_sync.kwargs
        # First clear had a guild kwarg
        assert "guild" in first_clear.kwargs

    async def test_idempotent(self, bot_module):
        """Calling sync_slash_commands twice produces the same effect."""
        sync_slash_commands = bot_module["sync_slash_commands"]
        tree = make_tree_mock()
        guilds = make_guilds(1, 2, 3)

        result1 = await sync_slash_commands(tree, guilds)
        result2 = await sync_slash_commands(tree, guilds)

        assert result1 == result2 == (25, 3)
        assert tree.clear_commands.call_count == 6  # 2 calls × 3 guilds


class TestRegressionDoubledUp:
    """Regression test for the original bug.

    The pre-fix scenario: a guild has 25 stale per-guild commands
    (from the old auto-sync code). The new code should clear them all.
    """

    async def test_clear_then_sync_results_in_empty_per_guild(self, bot_module):
        sync_slash_commands = bot_module["sync_slash_commands"]

        # Simulate Discord storing per-guild commands in a list
        per_guild_state = {
            "per_guild_commands": [m.MagicMock(id=i) for i in range(25)]
        }

        tree = m.MagicMock()

        async def fake_sync(*, guild=None):
            if guild is None:
                return [m.MagicMock(id=f"g-{i}") for i in range(25)]
            else:
                # tree.clear_commands was called first, so per-guild
                # state is empty; sync sends empty list = delete all.
                per_guild_state["per_guild_commands"] = []
                return []

        tree.sync = m.AsyncMock(side_effect=fake_sync)
        tree.clear_commands = m.MagicMock()

        guilds = make_guilds(786690956514426910)

        synced, cleared = await sync_slash_commands(tree, guilds)

        assert per_guild_state["per_guild_commands"] == [], \
            "Per-guild commands should be cleared after sync_slash_commands"
        assert synced == 25
        assert cleared == 1