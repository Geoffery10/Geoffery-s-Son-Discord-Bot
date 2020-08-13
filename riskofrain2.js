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
const whites = ['Armor-Piercing_Rounds', 'Backup_Magazine', 'Bundle_of_Fireworks', 'Bustling_Fungus', 'Crowbar', 'Energy_Drink', 'Focus_Crystal', 'Fresh_Meat', 
      'Gasoline', 'Lens-Makers_Glasses', 'Medkit', 'Monster_Tooth', 'Pauls_Goat_Hoof', 'Personal_Shield_Generator', 'Repulsion_Armor_Plate', 'Rusted_Key', 
      'Soldiers_Syringe', 'Sticky_Bomb', 'Stun_Grenade', 'Topaz_Brooch', 'Tougher_Times', 'Tri-Tip_Dagger', 'Warbanner']
const greens = ['AtG_Missile_Mk._1', 'Bandolier', 'Berzerkers_Pauldron', 'Chronobauble', 'Death_Mark', 'Fuel_Cell', 'Ghors_Tome', 'Harvesters_Scythe', 
'Hopoo_Feather', 'Infusion', 'Kjaros_Bandt', 'Leeching_Seed', 'Lepton_Daisy', 'Old_Guillotine', 'Old_War_Stealthkit', 'Predatory_Instincts', 
'Razorwire', 'Red_Whip', 'Rose_Buckler', 'Runalds_Band', 'Squid_Polyp', 'Ukulele', 'War_Horn', 'Wax_Quail', 'Will-o-the-wisp']
const reds = ['57_Leaf_Clover', 'Aegis', 'Alien_Head', 'Brainstalks', 'Brilliant_Behemoth', 'Ceremonial_Dagger', 'Dios_Best_Friend', 'Frost_Relic', 'H3AD-5T_v2', 
'Happiest_Mask', 'Hardlight_Afterburner', 'Interstellar_Desk_Plant', 'Nkuhanas_Opinion', 'Rejuvenation_Rack', 'Resonance_Disc', 'Sentient_Meat_Hook', 
'Shattering_Justice', 'Soulbound_Catalyst', 'Unstable_Tesla_Coil', 'Wake_of_Vultures']
const yellows = ['Genesis_Loop', 'Little_Disciple', 'Mired_Urn', 'Molten_Perforator', 'Queens_Gland', 'Shatterspleen', 'Titanic_Knurl']
const equipments = ['Blast_Shower', 'Disposable_Missile_Launcher', 'Eccentric_Vase', 'Foreign_Fruit', 'Forgive_Me_Please', 'Gnarled_Woodsprite', 'Gorags_Opus', 'Jade_Elephant', 
'Milky_Chrysalis', 'Ocular_HUD', 'Preon_Accumulator', 'Primordial_Cube', 'Radar_Scanner', 'Royal_Capacitor', 'Sawmerang', 'Super_Massive_Leech', 'The_Back-up', 
'The_Crowdfunder', 'Volcanic_Egg']
const lunars = ['Beads_of_Fealty', 'Brittle_Crown', 'Corpsebloom', 'Defiant_Gouge', 'Focused_Convergence', 'Gesture_of_the_Drowned', 'Mercurial_Rachis', 'Purity', 
'Shaped_Glass', 'Strides_of_Heresy', 'Transcendence', 'Visions_of_Heresy']
const lunarEquipments = ['Effigy_of_Grief', 'Glowing_Meteorite', 'Eccentric_Vase', 'Helfire_Tincture', 'Spinel_Tonic']

const randomLoadout = async function (bot, user, userID, channelID, message, evt) {
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