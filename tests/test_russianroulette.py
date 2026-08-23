"""Tests for Russian Roulette game state self-healing and slash acks.

The Russian Roulette slash commands used to fail with "application did
not respond" because:
- The data file (`gameData/Russian Roulette/games.json`) is gitignored
  runtime state. Fresh deploys or LXC rebuilds don't have it, so
  `check_game_file()` returns False and the user sees nothing.
- None of the helpers acknowledged the slash interaction early. Discord
  gives a 3-second window before showing "did not respond", and the
  helpers take longer than that on the cold path.

This test exercises both fixes.
"""

import json
import sys
import unittest.mock as m
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def rr_module():
    """Provide the real russianroulette module.

    conftest.py's autouse `reset_module_stubs` fixture stubs
    russianroulette and loggingChannel before every test. We need the
    real modules for these tests, so swap them in for the duration of
    the test.
    """
    # Drop the stubs installed by conftest's autouse fixture.
    sys.modules.pop("russianroulette", None)
    sys.modules.pop("loggingChannel", None)

    # Force a real loggingChannel import — russianroulette.py imports it.
    import loggingChannel  # noqa: F401

    # Now import the real russianroulette module.
    import russianroulette  # noqa: E402

    yield russianroulette

    # Restore stubs so the next test starts clean.
    sys.modules["russianroulette"] = m.MagicMock(name="stub_russianroulette")
    sys.modules["loggingChannel"] = m.MagicMock(name="stub_loggingChannel")


@pytest.fixture
def fresh_data_dir(tmp_path, monkeypatch):
    """Point BOT_DATA_DIR at a clean tmp dir so we don't pollute the repo."""
    monkeypatch.setenv("BOT_DATA_DIR", str(tmp_path))
    return tmp_path


@pytest.fixture
def fake_interaction():
    interaction = m.MagicMock()
    interaction.response = m.MagicMock()
    interaction.response.is_done = m.MagicMock(return_value=False)
    interaction.response.defer = m.AsyncMock()
    interaction.response.send_message = m.AsyncMock()
    interaction.followup = m.MagicMock()
    interaction.followup.send = m.AsyncMock()
    interaction.channel = m.MagicMock()
    interaction.channel.send = m.AsyncMock()
    interaction.guild = m.MagicMock()
    interaction.guild.id = 786690956514426910
    interaction.channel.id = 786690957042516001
    interaction.user = m.MagicMock()
    interaction.user.id = 253710834553847808
    interaction.user.name = "yui"
    interaction.user.display_avatar.url = "https://example.com/avatar.png"
    return interaction


class TestGameFileHelpers:
    def test_ensure_game_file_creates_file_when_missing(
        self, rr_module, fresh_data_dir
    ):
        game_file = fresh_data_dir / "gameData" / "Russian Roulette" / "games.json"
        assert not game_file.exists()

        rr_module.ensure_game_file()

        assert game_file.exists()
        assert json.loads(game_file.read_text()) == []

    def test_check_game_file_heals_missing_state(self, rr_module, fresh_data_dir):
        # Pre-condition: no data dir/file
        assert not (fresh_data_dir / "gameData").exists()
        rr_module.ensure_game_file()
        game_file = fresh_data_dir / "gameData" / "Russian Roulette" / "games.json"
        assert game_file.exists()

    def test_get_game_data_creates_file_if_missing(self, rr_module, fresh_data_dir):
        import asyncio
        data = asyncio.run(rr_module.get_game_data())
        assert data == []


class TestInteractionAck:
    async def test_acknowledge_interaction_defers_when_not_done(
        self, rr_module, fake_interaction
    ):
        fake_interaction.response.is_done.return_value = False
        await rr_module.acknowledge_interaction(fake_interaction)
        fake_interaction.response.defer.assert_awaited_once_with(ephemeral=True)

    async def test_acknowledge_interaction_is_idempotent(
        self, rr_module, fake_interaction
    ):
        fake_interaction.response.is_done.return_value = True
        await rr_module.acknowledge_interaction(fake_interaction)
        fake_interaction.response.defer.assert_not_called()


class TestStartGame:
    async def test_start_game_creates_file_when_missing(
        self, rr_module, fresh_data_dir, fake_interaction
    ):
        fake_interaction.response.is_done.return_value = False
        await rr_module.startGame(fake_interaction, client=m.MagicMock())

        game_file = fresh_data_dir / "gameData" / "Russian Roulette" / "games.json"
        assert game_file.exists()
        data = json.loads(game_file.read_text())
        assert isinstance(data, list)
        assert len(data) == 1
        new_game = data[0]
        assert new_game["channel"] == fake_interaction.channel.id
        assert new_game["active"] is True
        assert new_game["players"] == [fake_interaction.user.id]
        fake_interaction.response.defer.assert_awaited()


class TestShootSpin:
    async def test_shoot_calls_acknowledge(
        self, rr_module, fresh_data_dir, fake_interaction
    ):
        fake_interaction.response.is_done.return_value = False
        await rr_module.shoot(fake_interaction, client=m.MagicMock())
        assert fake_interaction.response.defer.await_count >= 1

    async def test_spin_calls_acknowledge(
        self, rr_module, fresh_data_dir, fake_interaction
    ):
        fake_interaction.response.is_done.return_value = False
        await rr_module.spin(fake_interaction, client=m.MagicMock())
        assert fake_interaction.response.defer.await_count >= 1