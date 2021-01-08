import discord
import random

survivors = ['https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/8/8e/Acrid.png?version=a770995303bb4b03d7df6f923ef1fff9',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/9/98/Artificer.png/128px-Artificer.png?version=26b17dea06edace28354784b56353135',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/a/a9/Captain.png?version=57daf1c125136f82afdfeed472aa760a',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/5/50/Commando.png/128px-Commando.png?version=4531406629ba5d4aa666caac2b8d8ac0',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/d/d8/Engineer.png/128px-Engineer.png?version=2512c8d63d7f72346fc8d4844701bfb3',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/6/6f/Huntress.png/128px-Huntress.png?version=7b72eef62ac8a167fc8577a124144c88',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/2/25/Loader.png?version=6ab3ac5a71553bcc805fc98bfa61a8a0',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/0/00/Mercenary.png/128px-Mercenary.png?version=049e8137daf69cb645908ac7affeace5',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/6/6f/MUL-T.png/128px-MUL-T.png?version=3d4235ee57a9b7145d79e9d342eb3e03',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/7/74/REX.png?version=ddc456b15c26f92e4fc52fcd911c081b']
whites = ['Armor-Piercing Rounds', 'Backup Magazine', 'Bundle of Fireworks', 'Bustling Fungus', 'Crowbar', 'Energy Drink', 'Focus Crystal', 'Fresh Meat',
      'Gasoline', 'Lens-Maker\'s Glasses', 'Medkit', 'Monster Tooth', 'Paul\'s Goat Hoof', 'Personal Shield Generator', 'Repulsion Armor Plate', 'Rusted Key',
      'Soldier\'s Syringe', 'Sticky Bomb', 'Stun Grenade', 'Topaz Brooch', 'Tougher Times', 'Tri-Tip Dagger', 'Warbanner']
greens = ['AtG Missile Mk. 1', 'Bandolier', 'Berzerker\'s Pauldron', 'Chronobauble', 'Death Mark', 'Fuel Cell', 'Ghor\'s Tome', 'Harvester\'s Scythe',
'Hopoo Feather', 'Infusion', 'Kjaro\'s Bandt', 'Leeching Seed', 'Lepton Daisy', 'Old Guillotine', 'Old War Stealthkit', 'Predatory Instincts',
'Razorwire', 'Red Whip', 'Rose Buckler', 'Runald\'s Band', 'Squid Polyp', 'Ukulele', 'War Horn', 'Wax Quail', 'Will-o\'-the-wisp']
reds = ['57 Leaf Clover', 'Aegis', 'Alien Head', 'Brainstalks', 'Brilliant Behemoth', 'Ceremonial Dagger', 'Dio\'s Best Friend', 'Frost Relic', 'H3AD-5T v2',
'Happiest Mask', 'Hardlight Afterburner', 'Interstellar Desk Plant', 'N\'kuhana\'s Opinion', 'Rejuvenation Rack', 'Resonance Disc', 'Sentient Meat Hook',
'Shattering Justice', 'Soulbound Catalyst', 'Unstable Tesla Coil', 'Wake of Vultures']
yellows = ['Genesis Loop', 'Little Disciple', 'Mired Urn', 'Molten Perforator', 'Queen\'s Gland', 'Shatterspleen', 'Titanic Knurl']
equipments = ['Blast Shower', 'Disposable Missile Launcher', 'Eccentric Vase', 'Foreign Fruit', 'Forgive Me Please', 'Gnarled Woodsprite', 'Gorag\'s Opus', 'Jade Elephant',
'Milky Chrysalis', 'Ocular HUD', 'Preon Accumulator', 'Primordial Cube', 'Radar Scanner', 'Royal Capacitor', 'Sawmerang', 'Super Massive Leech', 'The Back-up',
'The Crowdfunder', 'Volcanic Egg']
lunars = ['Beads of Fealty', 'Brittle Crown', 'Corpsebloom', 'Defiant Gouge', 'Focused Convergence', 'Gesture of the Drowned', 'Mercurial Rachis', 'Purity',
'Shaped Glass', 'Strides of Heresy', 'Transcendence', 'Visions of Heresy']
lunarEquipments = ['Effigy of Grief', 'Glowing Meteorite', 'Eccentric Vase', 'Helfire Tincture', 'Spinel Tonic']


def get_r2loadout():
    embed = discord.Embed(title="Risk of Rain 2 Loadout", colour=discord.Colour(0x492049),
                          url="https://riskofrain2.fandom.com/wiki/Risk_of_Rain_2_Wiki",
                          description="Here is your Risk of Rain 2 loadout:")

    embed.set_thumbnail(
        url=random.choice(survivors))
    embed.set_author(name="Support Polyp",
                     icon_url="https://static.wikia.nocookie.net/riskofrain2_gamepedia_en/images/d/de/Squid_Polyp.png/revision/latest/scale-to-width-down/128?cb=20200331154526")


    embed.add_field(name="White", value=random.choice(whites))
    embed.add_field(name="Green", value=random.choice(greens))
    embed.add_field(name="Red", value=random.choice(reds))
    embed.add_field(name="Yellow", value=random.choice(yellows))
    embed.add_field(name="Equipment", value=random.choice(equipments))
    embed.add_field(name="Lunar", value=random.choice(lunars))
    embed.add_field(name="Lunar Equipment", value=random.choice(lunarEquipments))
    return embed