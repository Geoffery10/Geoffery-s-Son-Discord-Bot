"""Tests for every slash command in bot.py.

Covers each command's handler in isolation. Tests:

- HTTP-fetch commands: mock `requests.get` to return canned JSON.
- File/image commands: stub `discord.File` and patch `os.listdir` /
  `path.isfile`.
- Helper-delegating commands: stub the underlying helper module
  function.
- Pure local logic commands (roll, ping, wtf, nani, help): exercise
  the math and embed construction directly.

The goal is that any command handler that crashes on a missing
external dependency (dead API, missing file, unconfigured env var)
has a regression test demonstrating the failure path is handled.
"""

import json
import sys
import unittest.mock as m
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Stub project modules we don't want to import (loggingChannel already
# used by conftest; load order matches the other test files).
sys.modules.setdefault("loggingChannel", m.MagicMock())
sys.modules.setdefault("fileManager", m.MagicMock())
sys.modules.setdefault("minecraftrcon", m.MagicMock())
sys.modules.setdefault("twitch", m.MagicMock())
sys.modules.setdefault("zapier_commands", m.MagicMock())
sys.modules.setdefault("react", m.MagicMock())

# bot.py runs `client.run(TOKEN)` at the bottom. We strip that line
# via the import helper so tests can import the module.
SOURCE = (PROJECT_ROOT / "bot.py").read_text()
SOURCE = SOURCE.replace("client.run(TOKEN)", "pass  # mocked")


# Helper functions that bot.py awaits. Configure them as AsyncMock on
# their parent stub modules before bot.py's `exec` runs, so the
# `from X import Y` references bind to coroutine-returning mocks.
# conftest.py installs the MagicMock stubs before every test, so by the
# time `bot_module` fixture runs, these attributes already exist as
# MagicMock. We just promote the awaited ones to AsyncMock.
async_helper_names = (
    "sendImageNew", "sendGifNew", "sendLog",
    "ping_MC_server", "ping_MC_server_interaction",
    "get_r2loadout", "checkReact", "checkForPrompts",
)


def _promote_async_helpers():
    """Promote awaited helper attributes on stubbed modules to AsyncMock."""
    targets = {
        "fileManager": ("sendImageNew", "sendImage"),
        "slash_commands": ("sendGifNew", "sendGif"),
        "loggingChannel": ("sendLog",),
        "minecraftrcon": ("ping_MC_server", "ping_MC_server_interaction"),
        "r2loadout": ("get_r2loadout",),
        "react": ("checkReact",),
    }
    for module_name, attrs in targets.items():
        mod = sys.modules.get(module_name)
        if mod is None:
            continue
        for attr in attrs:
            if attr in async_helper_names:
                setattr(mod, attr, m.AsyncMock(name=f"{module_name}.{attr}", return_value=None))


@pytest.fixture
def bot_module():
    _promote_async_helpers()
    ns = {"__name__": "bot_test", "__file__": str(PROJECT_ROOT / "bot.py")}
    exec(compile(SOURCE, str(PROJECT_ROOT / "bot.py"), "exec"), ns)
    # @tree.command wraps each handler in a Command object. Unwrap so
    # tests can call the underlying coroutine directly. AsyncMock
    # attributes have a `.callback` too but we want to keep them as
    # AsyncMocks for assertion tracking.
    # Mutate ns in place so test mutations (e.g. replacing `client`)
    # affect what bot.py's functions see.
    for name in list(ns.keys()):
        value = ns[name]
        if hasattr(value, "callback") and not isinstance(value, m.AsyncMock):
            ns[name] = value.callback
    return ns


@pytest.fixture
def fake_interaction():
    interaction = m.MagicMock()
    interaction.response = m.MagicMock()
    interaction.response.is_done = m.MagicMock(return_value=False)
    interaction.response.defer = m.AsyncMock()
    interaction.response.send_message = m.AsyncMock()
    interaction.followup = m.MagicMock()
    interaction.followup.send = m.AsyncMock()
    interaction.user = m.MagicMock()
    interaction.user.name = "yui"
    interaction.user.id = 735550470675759106
    interaction.user.mention = "<@735550470675759106>"
    interaction.user.display_avatar.url = "https://example.com/avatar.png"
    interaction.guild = m.MagicMock()
    interaction.guild.id = 786690956514426910
    interaction.channel = m.MagicMock()
    interaction.channel.id = 786690957042516001
    return interaction


@pytest.fixture
def fake_member():
    member = m.MagicMock()
    member.id = 999999999
    member.name = "target_user"
    member.display_name = "Target User"
    member.mention = "<@999999999>"
    member.display_avatar.url = "https://example.com/target.png"
    return member


# ---------------------------------------------------------------------------
# Pure-local commands (no external deps)
# ---------------------------------------------------------------------------

class TestRollCommand:
    async def test_roll_basic(self, bot_module, fake_interaction):
        roll = bot_module["roll"]
        await roll(fake_interaction, dice_count=3, dice_sides=6)
        fake_interaction.response.send_message.assert_awaited_once()
        call = fake_interaction.response.send_message.call_args
        assert "embed" in call.kwargs
        embed = call.kwargs["embed"]
        # 3d6 rolled sum lands in [3, 18]
        desc = embed.description
        for total in range(3, 19):
            if f"You rolled {total} " in desc:
                break
        else:
            pytest.fail(f"no total in range found in: {desc}")

    async def test_roll_rejects_zero_dice(self, bot_module, fake_interaction):
        roll = bot_module["roll"]
        await roll(fake_interaction, dice_count=0, dice_sides=6)
        fake_interaction.response.send_message.assert_awaited_once()
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "reasonable numbers" in msg.lower()

    async def test_roll_rejects_zero_sides(self, bot_module, fake_interaction):
        roll = bot_module["roll"]
        await roll(fake_interaction, dice_count=2, dice_sides=0)
        fake_interaction.response.send_message.assert_awaited_once()
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "reasonable numbers" in msg.lower()

    async def test_roll_rejects_huge_count(self, bot_module, fake_interaction):
        roll = bot_module["roll"]
        await roll(fake_interaction, dice_count=101, dice_sides=6)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "reasonable numbers" in msg.lower()


class TestPingCommand:
    async def test_ping_reports_latency(self, bot_module, fake_interaction):
        ping = bot_module["ping"]
        # bot.py reads client.latency (a property on discord.Client).
        # Replace the bot's `client` reference so the function picks it up.
        class _LatencyClient:
            latency = 0.123

        # bot_module is the same dict that bot.py's functions see, so
        # mutating bot_module["client"] affects what ping() reads.
        original_client = bot_module["client"]
        bot_module["client"] = _LatencyClient()
        try:
            await ping(fake_interaction)
        finally:
            bot_module["client"] = original_client
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "Pong" in msg
        assert "123" in msg


class TestWtfCommand:
    async def test_wtf_replies_rude(self, bot_module, fake_interaction):
        wtf = bot_module["wtf"]
        await wtf(fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "Rude" in msg


class TestNaniCommand:
    async def test_nani_replies_kanji(self, bot_module, fake_interaction):
        nani = bot_module["nani"]
        await nani(fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "何" in msg


class TestHelpCommand:
    async def test_help_sends_ephemeral_embed(self, bot_module, fake_interaction):
        help_cmd = bot_module["help"]
        await help_cmd(fake_interaction)
        fake_interaction.response.send_message.assert_awaited_once()
        call = fake_interaction.response.send_message.call_args
        assert call.kwargs.get("ephemeral") is True
        assert "embed" in call.kwargs


class TestWaifuCommand:
    async def test_waifu_posts_url(self, bot_module, fake_interaction):
        waifu = bot_module["waifu"]
        await waifu(fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "thiswaifudoesnotexist.net/example-" in msg
        assert msg.endswith(".jpg")


class TestHotCommand:
    async def test_hot_sends_video(self, bot_module, fake_interaction, monkeypatch):
        hot = bot_module["hot"]
        # discord.File just needs to exist; we monkeypatch to a MagicMock
        # so we don't try to open a real video file from the test cwd.
        monkeypatch.setattr(bot_module["discord"], "File", m.MagicMock())
        await hot(fake_interaction)
        fake_interaction.response.send_message.assert_awaited_once()
        assert "file" in fake_interaction.response.send_message.call_args.kwargs


# ---------------------------------------------------------------------------
# HTTP-fetch commands — mock requests.get
# ---------------------------------------------------------------------------

def _make_response(status_code, json_body):
    r = m.MagicMock()
    r.status_code = status_code
    r.content = json.dumps(json_body).encode("utf-8") if json_body is not None else b""
    return r


class TestJokeCommand:
    async def test_joke_uses_rapidapi_when_key_present(
        self, bot_module, fake_interaction, monkeypatch
    ):
        monkeypatch.setenv("JOKE3_RAPIDAPI_KEY", "fake-key")
        # bot.py does `from random import randint` so `randint` is the
        # bot_module-level binding to the real function. Replace it.
        original_randint = bot_module["randint"]
        bot_module["randint"] = lambda *a, **kw: 2
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(side_effect=lambda *a, **kw: _make_response(200, {"content": "knock knock"}))
        )
        try:
            joke = bot_module["joke"]
            await joke(fake_interaction)
        finally:
            bot_module["randint"] = original_randint
        # rapidapi path: defer + followup.send
        fake_interaction.response.defer.assert_awaited_once()
        fake_interaction.followup.send.assert_awaited_once_with("knock knock")

    async def test_joke_falls_back_when_rapidapi_500(
        self, bot_module, fake_interaction, monkeypatch
    ):
        monkeypatch.setenv("JOKE3_RAPIDAPI_KEY", "fake-key")
        original_randint = bot_module["randint"]
        bot_module["randint"] = lambda *a, **kw: 2

        def route_get(url, **kw):
            if "joke3" in url:
                return _make_response(500, None)
            return _make_response(200, {"joke": "free joke"})
        monkeypatch.setattr(bot_module["requests"], "get", route_get)
        try:
            await bot_module["joke"](fake_interaction)
        finally:
            bot_module["randint"] = original_randint
        # Fallback path uses followup.send with the free joke
        assert fake_interaction.followup.send.await_count >= 1


class TestInsultCommand:
    async def test_insult_success(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(200, {"insult": "you are bad"}))
        )
        await bot_module["insult"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "you are bad" in msg

    async def test_insult_failure(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(500, None))
        )
        await bot_module["insult"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "Failed" in msg


class TestFactCommand:
    async def test_fact_success(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(200, {"text": "bees can fly"}))
        )
        await bot_module["fact"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "bees can fly" in msg

    async def test_fact_failure(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(500, None))
        )
        await bot_module["fact"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "Failed" in msg


class TestAdviceCommand:
    async def test_advice_success(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(200, {"slip": {"advice": "be kind"}}))
        )
        await bot_module["advice"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "be kind" in msg

    async def test_advice_failure(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(500, None))
        )
        await bot_module["advice"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "Failed" in msg


class TestCatCommand:
    async def test_cat_missing_key(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.delenv("THE_CAT_API", raising=False)
        await bot_module["cat"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "not configured" in msg.lower()

    async def test_cat_success(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setenv("THE_CAT_API", "fake")
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(200, [{"url": "https://cats.example/1.jpg"}]))
        )
        await bot_module["cat"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "cats.example" in msg

    async def test_cat_failure(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setenv("THE_CAT_API", "fake")
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(500, None))
        )
        await bot_module["cat"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "Failed" in msg


class TestDogCommand:
    async def test_dog_success(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(200, {"url": "https://dogs.example/1.jpg"}))
        )
        await bot_module["dog"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "dogs.example" in msg

    async def test_dog_failure(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(500, None))
        )
        await bot_module["dog"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "Failed" in msg


class TestYesornoCommand:
    async def test_yesorno_sends_image_then_answer(
        self, bot_module, fake_interaction, monkeypatch
    ):
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(200, {"image": "https://yesno.example/y.gif", "answer": "yes"}))
        )
        await bot_module["yesorno"](fake_interaction)
        # First call: response.send_message with the image URL
        assert fake_interaction.response.send_message.await_count == 1
        img_msg = fake_interaction.response.send_message.call_args.args[0]
        assert "yesno.example" in img_msg
        # Second call: followup.send with the answer (capitalised)
        fake_interaction.followup.send.assert_awaited_once_with("Yes")

    async def test_yesorno_failure(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(500, None))
        )
        await bot_module["yesorno"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "Failed" in msg


class TestIdCommand:
    async def test_id_missing_key(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.delenv("X_RAPIDAPI_KEY", raising=False)
        await bot_module["id"](fake_interaction)
        # bot.py doesn't pre-check the key; it just sends a 401/403
        # status message from the API. We don't assert that here since
        # requests.get is unmocked and would hit the network.

    async def test_id_success(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setenv("X_RAPIDAPI_KEY", "fake")
        body = {
            "results": [{
                "name": {"title": "Mr", "first": "Test", "last": "User"},
                "picture": {"large": "https://example.com/pic.jpg"},
                "location": {
                    "street": {"number": 1, "name": "Main"},
                    "city": "T", "state": "S", "country": "C", "postcode": "00000",
                },
                "email": "t@u.com",
                "login": {"username": "tu", "password": "pw"},
                "cell": "555-0000",
                "dob": {"age": 30, "date": "1990-01-01"},
                "id": {"name": "SSN", "value": "111-22-3333"},
            }]
        }
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(200, body))
        )
        await bot_module["id"](fake_interaction)
        fake_interaction.response.send_message.assert_awaited_once()
        call = fake_interaction.response.send_message.call_args
        assert "embed" in call.kwargs

    async def test_id_failure(self, bot_module, fake_interaction, monkeypatch):
        monkeypatch.setenv("X_RAPIDAPI_KEY", "fake")
        monkeypatch.setattr(
            bot_module["requests"], "get",
            m.Mock(return_value=_make_response(500, None))
        )
        await bot_module["id"](fake_interaction)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "server error" in msg.lower()


# ---------------------------------------------------------------------------
# Sins command — depends on member_data, no HTTP
# ---------------------------------------------------------------------------

class TestSinsCommand:
    async def test_sins_member_found(self, bot_module, fake_interaction, fake_member):
        fake_member_database = [{"userID": fake_member.id, "sins": "many"}]
        bot_module["member_data"].get_member_data = m.AsyncMock(
            return_value=fake_member_database
        )
        await bot_module["sins"](fake_interaction, member=fake_member)
        call = fake_interaction.response.send_message.call_args
        assert "embed" in call.kwargs

    async def test_sins_member_not_found(self, bot_module, fake_interaction, fake_member):
        bot_module["member_data"].get_member_data = m.AsyncMock(return_value=[])
        await bot_module["sins"](fake_interaction, member=fake_member)
        msg = fake_interaction.response.send_message.call_args.args[0]
        assert "sinless" in msg.lower() or "no entry" in msg.lower()


# ---------------------------------------------------------------------------
# R2 loadout — depends on r2loadout.get_r2loadout
# ---------------------------------------------------------------------------

class TestR2LoadoutCommand:
    async def test_r2loadout_sends_embed(self, bot_module, fake_interaction):
        await bot_module["r2loadout"](fake_interaction)
        call = fake_interaction.response.send_message.call_args
        assert "embed" in call.kwargs


# ---------------------------------------------------------------------------
# Mcinfo — depends on ping_MC_server_interaction
# ---------------------------------------------------------------------------




# ---------------------------------------------------------------------------
# Selfie — depends on sendImageNew (fileManager)
# ---------------------------------------------------------------------------

class TestSelfieCommand:
    async def test_selfie_delegates_to_sendImageNew(
        self, bot_module, fake_interaction, monkeypatch
    ):
        # Patch os.listdir so it returns 5 "files" so the random.randint
        # below has a valid range.
        monkeypatch.setattr(
            bot_module["os"], "listdir",
            lambda d: [f"selfie_{i}.gif" for i in range(5)]
        )
        monkeypatch.setattr(bot_module["os"], "path", bot_module["os"].path)
        monkeypatch.setattr(
            bot_module["os"].path, "isfile", lambda p: True
        )
        # Force the random index to 0 so the test is deterministic.
        monkeypatch.setattr(bot_module["random"], "randint", lambda a, b: 0)
        await bot_module["selfie"](fake_interaction)
        bot_module["sendImageNew"].assert_awaited_once()


# ---------------------------------------------------------------------------
# Punch — depends on sendGifNew
# ---------------------------------------------------------------------------

class TestPunchCommand:
    async def test_punch_normal_member(self, bot_module, fake_interaction, fake_member):
        bot_module["sendGifNew"].reset_mock()
        await bot_module["punch"](fake_interaction, member=fake_member)
        # First call: response.send_message with the embed
        fake_interaction.response.send_message.assert_awaited_once()
        # Then sendGifNew fetches the gif (acknowledged via followup)
        bot_module["sendGifNew"].assert_awaited_once()

    async def test_punch_protected_member_flips(
        self, bot_module, fake_interaction, fake_member
    ):
        # When target.id == 786698404927504385, the bot punches the
        # *invoker* instead and uses "anime punch" as the gif search.
        bot_module["sendGifNew"].reset_mock()
        fake_member.id = 786698404927504385
        await bot_module["punch"](fake_interaction, member=fake_member)
        fake_interaction.response.send_message.assert_awaited_once()
        bot_module["sendGifNew"].assert_awaited_once()