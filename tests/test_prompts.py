"""Tests for prompts.checkForPrompts.

Strategy: import prompts.py directly, mock out its side effects (discord,
sendLog, sendImage, files on disk), and assert that message.channel.send is
called with the right content for each prompt match.

These tests are hermetic — no live Discord connection, no real files. They
verify the bot's matching and reply logic in isolation.
"""

import asyncio
import sys
import unittest.mock as m
from pathlib import Path
from typing import Optional

import pytest

# Stub out the heavy imports prompts.py pulls in (discord, loggingChannel,
# fileManager) so we can import the module without all of them being
# available. The stubs are minimal — anything we use in the tests gets a
# proper mock, anything else is just a MagicMock.
sys.modules.setdefault("discord", m.MagicMock())
sys.modules.setdefault("loggingChannel", m.MagicMock())
sys.modules.setdefault("fileManager", m.MagicMock())

# Make the project's modules importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import prompts  # noqa: E402


def make_msg(content: str, channel_send: Optional[m.AsyncMock] = None) -> m.MagicMock:
    """Build a fake discord.Message for checkForPrompts.

    channel_send defaults to a fresh AsyncMock so each test gets a clean
    record of what was sent. The message is set up so the im-joke logic sees
    `message.guild is None` (uses fallback client.user.name path).
    """
    msg = m.MagicMock()
    msg.content = content
    msg.author = m.MagicMock()
    msg.author.name = "tester"
    msg.guild = None
    msg.channel = m.MagicMock()
    msg.channel.id = 12345
    msg.channel.send = channel_send if channel_send is not None else m.AsyncMock()
    return msg


def make_client(user_name: str = "Geoffery's Son") -> m.MagicMock:
    """Build a fake discord.Client for checkForPrompts."""
    client = m.MagicMock()
    client.user = m.MagicMock()
    client.user.name = user_name
    return client


def find_text_reply(channel_send: m.AsyncMock, contains: str) -> bool:
    """Return True if any send() call had a string containing the substring."""
    for call in channel_send.call_args_list:
        args = call.args
        if args and isinstance(args[0], str) and contains in args[0]:
            return True
    return False


def find_text_equal(channel_send: m.AsyncMock, text: str) -> bool:
    """Return True if any send() call had exactly this string."""
    for call in channel_send.call_args_list:
        args = call.args
        if args and args[0] == text:
            return True
    return False


# ---------------------------------------------------------------------------
# Im-joke prompt
# ---------------------------------------------------------------------------

class TestImJokePrompt:
    """Tests for the 'Hi [something], I'm [bot]' Dad-joke response.

    Covers the regex and post-processing rules added in PR #15/17.
    """

    async def _run(self, content: str) -> m.AsyncMock:
        send = m.AsyncMock()
        msg = make_msg(content, channel_send=send)
        client = make_client()
        await prompts.checkForPrompts(msg, client)
        return send

    @pytest.mark.parametrize("content", [
        "I'm a bot",                # article -> suppressed
        "I'm an idiot",             # article -> suppressed
        "I'm the chosen one",       # article -> suppressed
        "I'm a tired programmer",   # article -> suppressed (first word is article)
        "I'm A BOT",                # lowered -> "a" -> suppressed
        "I'mhere",                  # no whitespace/punctuation between trigger and word
        "Hello there",              # unrelated message
    ])
    async def test_no_reply(self, content):
        send = await self._run(content)
        assert not find_text_reply(send, "Hi "), \
            f"Expected no reply for {content!r}, got {[c.args for c in send.call_args_list]}"

    @pytest.mark.parametrize("content,expected", [
        ("I'm tired",                      "Hi tired, I'm Geoffery's Son"),
        ("I'm so excited!",                "Hi so excited, I'm Geoffery's Son"),
        ("hello I'm new here",             "Hi new here, I'm Geoffery's Son"),
        (":wave: I'm here",                "Hi here, I'm Geoffery's Son"),
        ("Im hungry",                      "Hi hungry, I'm Geoffery's Son"),
        ("I am groot",                     "Hi groot, I'm Geoffery's Son"),
        # "I'M A BOT" lowered to "i'm a bot" — 'a' is article, suppressed.
        # Tested in test_no_reply instead.
        ("I'm not a robot",                "Hi not a robot, I'm Geoffery's Son"),
    ])
    async def test_reply_basic(self, content, expected):
        send = await self._run(content)
        assert find_text_equal(send, expected), \
            f"Expected {expected!r} for {content!r}, got {[c.args[0] if c.args else None for c in send.call_args_list]}"

    @pytest.mark.parametrize("content,expected", [
        ("I'm **tired**",      "Hi **tired**, I'm Geoffery's Son"),
        ("I'm _sad_",          "Hi _sad_, I'm Geoffery's Son"),
        ("I'm `coding`",       "Hi `coding`, I'm Geoffery's Son"),
        ("I'm (a bot)",        "Hi (a bot), I'm Geoffery's Son"),
        # Note: "I'M A BOT" lowered to "i'm a bot" — 'a' is article, suppressed.
        # Tested in test_no_reply instead.
    ])
    async def test_reply_preserves_markdown(self, content, expected):
        send = await self._run(content)
        assert find_text_equal(send, expected), \
            f"Expected {expected!r} for {content!r}, got {[c.args[0] if c.args else None for c in send.call_args_list]}"

    async def test_long_message_no_reply(self):
        """Run-on messages over 50 chars after the trigger shouldn't fire."""
        content = "I'm going to the store to get milk and also eggs because I forgot them yesterday"
        send = await self._run(content)
        assert not find_text_reply(send, "Hi "), \
            f"Expected no reply for long message, got {[c.args[0] if c.args else None for c in send.call_args_list]}"

    async def test_exactly_at_cap(self):
        """Exactly 50 chars captured should fire."""
        content = "I'm " + "x" * 49  # 49 x's — capture exactly 50 (incl. nothing extra)
        send = await self._run(content)
        expected = "Hi " + ("x" * 49) + ", I'm Geoffery's Son"
        assert find_text_equal(send, expected), \
            f"Expected {expected!r}, got {[c.args[0] if c.args else None for c in send.call_args_list]}"

    async def test_over_cap_no_reply(self):
        """51 chars captured should NOT fire."""
        content = "I'm " + "x" * 51
        send = await self._run(content)
        assert not find_text_reply(send, "Hi "), \
            f"Expected no reply for over-cap message, got {[c.args[0] if c.args else None for c in send.call_args_list]}"

    async def test_per_guild_display_name(self):
        """When the bot has a guild-specific nickname, use that name."""
        msg = m.MagicMock()
        msg.content = "I'm tired"
        msg.author = m.MagicMock()
        msg.author.name = "tester"
        msg.channel = m.MagicMock()
        msg.channel.send = m.AsyncMock()
        # Set up guild with a per-guild display name
        msg.guild = m.MagicMock()
        msg.guild.me = m.MagicMock()
        msg.guild.me.display_name = "Yui-chan"

        client = make_client(user_name="Geoffery's Son")
        await prompts.checkForPrompts(msg, client)
        assert find_text_equal(msg.channel.send, "Hi tired, I'm Yui-chan"), \
            f"Expected display-name reply, got {[c.args[0] if c.args else None for c in msg.channel.send.call_args_list]}"


# ---------------------------------------------------------------------------
# Other string-only prompts (smoke tests for the matching layer)
# ---------------------------------------------------------------------------

class TestStringOnlyPrompts:
    """Smoke tests for prompts that send a string (no file/image)."""

    async def _run(self, content: str) -> m.AsyncMock:
        send = m.AsyncMock()
        msg = make_msg(content, channel_send=send)
        client = make_client()
        await prompts.checkForPrompts(msg, client)
        return send

    async def test_sand(self):
        send = await self._run("I love sand")
        assert find_text_reply(send, "narvii.com/6995"), "Sand prompt should fire"

    async def test_9th_time(self):
        send = await self._run("9th time I've seen this")
        assert find_text_equal(send, "10th time!"), "9th time prompt should reply 10th time!"

    async def test_10th_time(self):
        send = await self._run("10th time's the charm")
        assert find_text_equal(send, "9th time!"), "10th time prompt should reply 9th time!"

    async def test_wentworth(self):
        send = await self._run("wentworth is great")
        assert find_text_equal(send, "877-CASH-NOW!"), "Wentworth prompt should reply 877-CASH-NOW!"

    async def test_a_scratch(self):
        send = await self._run("that was a scratch")
        assert find_text_reply(send, "Monty-Python"), "Scratch prompt should fire"

    async def test_no_match(self):
        send = await self._run("just a regular message about nothing")
        # No string-only prompt should fire
        for call in send.call_args_list:
            args = call.args
            if args and isinstance(args[0], str):
                # The only string sends should be from the im-joke (if it fired),
                # which we just tested separately. For a fully-no-match message
                # there should be no string sends at all.
                # If there's a send, it should be from the im-joke.
                assert "Hi " in args[0] and "I'm " in args[0], \
                    f"Unexpected string reply: {args[0]!r}"