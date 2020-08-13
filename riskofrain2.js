var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
var fileManager = require('./fileManager.js');
const fs = require('fs')
const fetch = require('node-fetch');
var lastNum = -1;

//Options to choose from
const survivors = ['https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/8/8e/Acrid.png?version=a770995303bb4b03d7df6f923ef1fff9', 
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/9/98/Artificer.png/128px-Artificer.png?version=26b17dea06edace28354784b56353135',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/a/a9/Captain.png?version=57daf1c125136f82afdfeed472aa760a',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/5/50/Commando.png/128px-Commando.png?version=4531406629ba5d4aa666caac2b8d8ac0',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/d/d8/Engineer.png/128px-Engineer.png?version=2512c8d63d7f72346fc8d4844701bfb3', 
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/6/6f/Huntress.png/128px-Huntress.png?version=7b72eef62ac8a167fc8577a124144c88',
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/2/25/Loader.png?version=6ab3ac5a71553bcc805fc98bfa61a8a0', 
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/0/00/Mercenary.png/128px-Mercenary.png?version=049e8137daf69cb645908ac7affeace5', 
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/thumb/6/6f/MUL-T.png/128px-MUL-T.png?version=3d4235ee57a9b7145d79e9d342eb3e03', 
    'https://gamepedia.cursecdn.com/riskofrain2_gamepedia_en/7/74/REX.png?version=ddc456b15c26f92e4fc52fcd911c081b']
const whites = ['Armor-Piercing Rounds', 'Backup Magazine', 'Bundle of Fireworks', 'Bustling Fungus', 'Crowbar', 'Energy Drink', 'Focus Crystal', 'Fresh Meat', 
      'Gasoline', 'Lens-Maker\'s Glasses', 'Medkit', 'Monster Tooth', 'Paul\'s Goat Hoof', 'Personal Shield Generator', 'Repulsion Armor Plate', 'Rusted Key', 
      'Soldier\'s Syringe', 'Sticky Bomb', 'Stun Grenade', 'Topaz Brooch', 'Tougher Times', 'Tri-Tip Dagger', 'Warbanner']
const greens = ['AtG Missile Mk. 1', 'Bandolier', 'Berzerker\'s Pauldron', 'Chronobauble', 'Death Mark', 'Fuel Cell', 'Ghor\'s Tome', 'Harvester\'s Scythe', 
'Hopoo Feather', 'Infusion', 'Kjaro\'s Bandt', 'Leeching Seed', 'Lepton Daisy', 'Old Guillotine', 'Old War Stealthkit', 'Predatory Instincts', 
'Razorwire', 'Red Whip', 'Rose Buckler', 'Runald\'s Band', 'Squid Polyp', 'Ukulele', 'War Horn', 'Wax Quail', 'Will-o\'-the-wisp']
const reds = ['57 Leaf Clover', 'Aegis', 'Alien Head', 'Brainstalks', 'Brilliant Behemoth', 'Ceremonial Dagger', 'Dio\'s Best Friend', 'Frost Relic', 'H3AD-5T v2', 
'Happiest Mask', 'Hardlight Afterburner', 'Interstellar Desk Plant', 'N\'kuhana\'s Opinion', 'Rejuvenation Rack', 'Resonance Disc', 'Sentient Meat Hook', 
'Shattering Justice', 'Soulbound Catalyst', 'Unstable Tesla Coil', 'Wake of Vultures']
const yellows = ['Genesis Loop', 'Little Disciple', 'Mired Urn', 'Molten Perforator', 'Queen\'s Gland', 'Shatterspleen', 'Titanic Knurl']
const equipments = ['Blast Shower', 'Disposable Missile Launcher', 'Eccentric Vase', 'Foreign Fruit', 'Forgive Me Please', 'Gnarled Woodsprite', 'Gorag\'s Opus', 'Jade Elephant', 
'Milky Chrysalis', 'Ocular HUD', 'Preon Accumulator', 'Primordial Cube', 'Radar Scanner', 'Royal Capacitor', 'Sawmerang', 'Super Massive Leech', 'The Back-up', 
'The Crowdfunder', 'Volcanic Egg']
const lunars = ['Beads of Fealty', 'Brittle Crown', 'Corpsebloom', 'Defiant Gouge', 'Focused Convergence', 'Gesture of the Drowned', 'Mercurial Rachis', 'Purity', 
'Shaped Glass', 'Strides of Heresy', 'Transcendence', 'Visions of Heresy']
const lunarEquipments = ['Effigy of Grief', 'Glowing Meteorite', 'Eccentric Vase', 'Helfire Tincture', 'Spinel Tonic']

const randomLoadout = function (tag) {
    var num = 0
    var value = ''
    switch (tag){
        case 'survivor':
            num = Math.floor(Math.random() * survivors.length)
            if (num == lastNum) {
                num = Math.floor(Math.random() * survivors.length)
            }
            lastNum = num
            value = survivors[num]
            break;
        case 'white':
            num = Math.floor(Math.random() * whites.length)
            value = whites[num]
            break;
        case 'green':
            num = Math.floor(Math.random() * greens.length)
            value = greens[num]
            break;
        case 'red':
            num = Math.floor(Math.random() * reds.length)
            value = reds[num]
            break;
        case 'equipment':
            num = Math.floor(Math.random() * equipments.length)
            value = equipments[num]
            break;
        case 'yellow':
            num = Math.floor(Math.random() * yellows.length)
            value = yellows[num]
            break;
        case 'lunar':
            num = Math.floor(Math.random() * lunars.length)
            value = lunars[num]
            break;
        case 'lunarEquipment':
            num = Math.floor(Math.random() * lunarEquipments.length)
            value = lunarEquipments[num]
            break;
    }
    console.log(value)
    return value
    /*
    //Pick items
    //White 
    var folder = "./images/riskofrain2/"
    num = Math.floor(Math.random() * whites.length)
    var white = whites[num]
    console.log(white)

    //Green
    num = Math.floor(Math.random() * greens.length)
    var green = greens[num]
    console.log(green)

    //Red
    num = Math.floor(Math.random() * reds.length)
    var red = reds[num]
    console.log(red)

    //Yellow
    folder = "./images/riskofrain2/"
    num = Math.floor(Math.random() * yellows.length)
    var yellow = yellows[num]
    console.log(yellow)
    
    //Equipment
    folder = "./images/riskofrain2/equipment"
    num = Math.floor(Math.random() * equipments.length)
    var equiment = equipments[num]
    console.log(equiment)

    ///Lunar
    folder = "./images/riskofrain2/"
    num = Math.floor(Math.random() * lunars.length)
    var lunar = lunars[num]
    console.log(lunar)

    //Lunar Equipment
    folder = "./images/riskofrain2/"
    num = Math.floor(Math.random() * lunarEquipments.length)
    var lunarEquipment = lunarEquipments[num]
    console.log(lunarEquipment)

    //Send images in order
    let result = await survivorStart(bot, channelID)
    result = await uploadItem(bot, channelID, (folder+"white"), white)
    result = await uploadItem(bot, channelID, (folder+"green"), green)
    result = await uploadItem(bot, channelID, (folder+"red"), red)
    result = await uploadItem(bot, channelID, (folder+"yellow"), yellow)
    result = await uploadItem(bot, channelID, (folder+"equipment"), equiment)
    result = await uploadItem(bot, channelID, (folder+"lunar"), lunar)
    result = await uploadItem(bot, channelID, (folder+"lunar_equipment"), lunarEquipment)
    return result
    */
}

const survivorStart = async function(bot, channelID) {
    // Start selection... Picking survivor
    num = Math.floor(Math.random() * survivors.length)
    if (num == lastNum) {
      num = Math.floor(Math.random() * survivors.length)
    }
    lastNum = num
    var survivor = survivors[num]
    bot.sendMessage({
      to: channelID,
      "content": "Good luck survivor...",
      "embed": {
        "title": "Risk of Rain 2 - Random Loadout",
        "description": "Item info can be found at the [Risk of Rain 2 Wiki](https://riskofrain2.gamepedia.com/Items).",
        "color": 4726857,
        "thumbnail": {
          "url": survivor
        },
        "fields": [
          {
            "name": "Loading items...",
            "value": "................"
          }
        ]
      }
    });
    return 0
}

const uploadItem = async function(bot, channelID, folder, item) {
    console.log("Sending: " + item + " to channel " + channelID)
    bot.uploadFile({
        to: channelID,
        file: (folder + '/' + item + '.png')
      });
      return 0
}

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
  }


module.exports.randomLoadout = randomLoadout;