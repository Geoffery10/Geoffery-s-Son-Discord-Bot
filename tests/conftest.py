"""Shared pytest fixtures and setup.

The bot's modules (bot.py, prompts.py, etc.) import discord and project
modules like loggingChannel, fileManager, minecraftrcon. We stub those
out so tests can import the project modules without all of them being
present.

Some test files replace sys.modules entries with the *real* modules
(notably test_russianroulette.py needs the real `russianroulette`
module to test its functions). Those replacements persist across
tests. The `reset_module_stubs` autouse fixture re-installs the
MagicMock stubs before each test so order-of-collection doesn't
matter.

Note: this autouse fixture is **function-scoped**. Module-scoped
fixtures in test files (like bot_module) run AFTER this autouse,
because pytest schedules function-scoped fixtures first. If you make
this autouse session-scoped, module-scoped fixtures will run BEFORE
the autouse and pick up stale sys.modules state.
"""

import sys
import unittest.mock as m

import pytest


# Make project root importable for every test file.
sys.path.insert(0, str(__file__).rsplit("/", 2)[0])


# Project-specific modules that bot.py imports. These are stubs
# (MagicMock) by default so importing prompts/bot doesn't try to load
# real network code. Individual test files can replace them with real
# modules inside their own fixtures; the `reset_module_stubs` autouse
# fixture restores the stubs after each test.
_STUB_MODULE_NAMES = [
    "loggingChannel",
    "fileManager",
    "minecraftrcon",
    "twitch",
    "zapier_commands",
    "r2loadout",
    "react",
    "russianroulette",
    "slash_commands",
]


@pytest.fixture(autouse=True)
def reset_module_stubs():
    """Reset bot's transitive-dep stubs to MagicMock before every test."""
    for name in _STUB_MODULE_NAMES:
        sys.modules[name] = m.MagicMock(name=f"stub_{name}")
    yield
    # No teardown needed: next test will re-stub anyway.