"""Shared pytest fixtures and setup.

The bot's modules (bot.py, prompts.py, etc.) import discord and project
modules like loggingChannel, fileManager, minecraftrcon. We stub those
out so tests can import the project modules without all of them being
present.

Each test file needs different things:
- test_prompts.py: discord as a MagicMock (so prompt regex logic works
  without a real client).
- test_onready.py: real discord (so bot.py imports cleanly and we can
  inspect the actual sync_slash_commands function).

We use pytest fixtures here so each test file gets exactly what it needs
without polluting sys.modules globally.
"""

import sys
import unittest.mock as m
from pathlib import Path


# Make project root importable for both test files.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# Project-specific modules that don't need real implementations for testing.
# Stubbed at import time so importing prompts/bot doesn't fail.
_PROJECT_MODULE_STUBS = {
    "loggingChannel": m.MagicMock(),
    "fileManager": m.MagicMock(),
    "minecraftrcon": m.MagicMock(),
    "twitch": m.MagicMock(),
    "zapier_commands": m.MagicMock(),
    "r2loadout": m.MagicMock(),
    "react": m.MagicMock(),
    "russianroulette": m.MagicMock(),
}
for name, stub in _PROJECT_MODULE_STUBS.items():
    sys.modules.setdefault(name, stub)