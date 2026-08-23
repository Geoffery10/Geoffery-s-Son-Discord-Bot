<p align="center">
<img align="center" width="200" height="200" src="https://github.com/Geoffery10/Geoffery-s-Son-Discord-Bot/blob/master/images/selfies/selfie_04.png?raw=true">
</p>

# Geoffery's Son Discord Bot
This is a Discord Bot for my own personal server. Most of his abilities are just for fun with a few useful commands.

> **Heads up:** this bot uses **Discord slash commands**, not text-prefix commands. In any channel, type `/` to see the full list of available commands. Slash commands work the same as other Discord bots — pick one from the popup, fill in any parameters, hit enter.

## Table of Contents
* [Slash Commands](#slash-commands)
* [Phrase Triggers](#phrase-triggers)
* [Reactions](#reactions)
* [License](#license)

## Slash Commands

### Casual
* `/selfie` - Sends a selfie of the bot.
* `/roll dice_count:3 dice_sides:6` - Rolls dice in `NdN` format. For example `/roll dice_count:3 dice_sides:2` rolls 3 d2 dice and reports the total.
* `/sins member:@yourfriend` - Tells you the sins of your friends. I'd watch out for Steve from accounting...
* `/punch member:@yourfriend` - Punch your friends over the internet from a safe distance.

* `/ping` - Pong! (with latency).
* `/wtf` - Why is this a command?
* `/nani` - It can translate to weeb characters.
* `/id` - This will create your new identity.
* `/hot` - BRRRRRRRR!!

### Image generators
* `/waifu` - The smart ai at [thiswaifudoesnotexist](https://www.thiswaifudoesnotexist.net) will send us a waifu that does not exist.
* `/cat` - I'll send a random image of a kitty!
* `/dog` - I'll send a random image of a dogo!
* `/yesorno` - I'll tell you if the answer is yes or no.
* `/r2loadout` - A random load out for a Risk of Rain 2 Command run. I hope Rnjesus is on your side.

### APIs
* `/joke` - I'll tell you a joke!
* `/insult` - I'll insult you! Be prepared some of these are pretty terrible...
* `/fact` - I'll tell you a random fact.
* `/advice` - I'll give you some advice.

### Russian Roulette Game
* `/rr` - Start a game of Russian Roulette.
* `/shoot` - Pull the trigger.
* `/spin` - Spin the cylinder.

### Meta
* `/help` - Sends this list (as an ephemeral message visible only to you).

> **Note:** the legacy `!quit` text command (admin-only bot shutdown) is **not** a slash command and is not currently implemented. Discord doesn't support terminating the bot process via slash command. The bot runs as a long-lived `systemd` service on the host and is restarted via `systemctl restart discord-bot.service`, not via Discord.

## Phrase Triggers

These are *not* commands. The bot listens for these phrases anywhere in chat and replies with a meme or image. There's nothing to type — just say the phrase in any channel the bot can read.

| Say... | The bot replies with... |
|---|---|
| `is it possible to learn this power` | Palpatine meme |
| `the sun is a deadly laser` | The Blanket meme |
| `10th time` | `9th time!` |
| `9th time` | `10th time!` |
| `badonkers`, `dobonhonkeros`, etc. | Big Chungus meme link |
| `sauce` | Random nhentai number "for the sauce" |
| `heresy` | Random heresy image |
| `ravioli ravioli` | Either ravioli gif or "police" video |
| `hentai` | Either hentai gif or "police" video |
| `hello there` | General Kenobi gif |
| `trap` | Trap gif |
| `wentworth` | `877-CASH-NOW!` |
| `a scratch` | Black Knight "It's just a scratch" gif |

## Reactions

The bot reacts with an emoji when it sees certain keywords. No action needed on your part — just type normally.

| See... | Bot reacts with |
|---|---|
| `rip` | `:rip:` |
| `stonks` | `:stonks:` |
| `cringe` / `cringy` | `:cringe_harold:` |
| `chad` | `:Yes_Chad:` |
| `to be continued` | `:to_be_continued:` |
| `shrug` / `shrugging` | `:Shrug:` |
| `f` (single letter, in chat) | `:press_F:` |
| `pog` / `pogger` | `:pog:` |
| `nani` / `何` | `:nani:` |
| `dio` | `:dio:` |
| `menacing` / `scary` | `:menacing:` |
| `doubt` / `press x` | `:doubt:` |
| `horny` / `bonk` / `sauce` / `sause` / `hentai` | `:bonk:` |
| `report` / `sus` | `:among_us_report:` |
| `fbi` / `f.b.i` | `:fbi:` |
| A message that mentions the bot | `:eyes:` |

## License
This code is was created and owned by me. You are free to use it in your own projects without credit (Just don't submit it to your Professor because that's a bad idea).
