const Discord = require('discord.js');
const client = new Discord.Client();
var logger = require('winston');
var auth = require('./auth.json');
var fileManager = require('./fileManager.js');
var riskofrain2 = require('./riskofrain2.js');
var randomMod = require('./randomMod.js');
var members = require('./members.js');
const fs = require('fs')
const fetch = require('node-fetch');
const { json } = require('express');
var https = require('https');
var lastNum = -1;
var birthdayLastDate = new Date(2019,3,31) 
const masterColor = 7871916
// Require the module in your project

// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = 'debug';
// Initialize Discord Bot

client.once('ready', () => {
	console.log('Ready!');
});

client.login(auth.token);


client.on('message', message => {
  members.checkMember(message.author.username, message.author.id)
  var channel = message.channel;
  //var author = message.author;
  //console.log(user + "/" + userID + " sent: " + message)
  //console.log(auther + " on " + channel + ": " + message.content);

  if (message.content.toLowerCase().includes("anime".toLowerCase()) == true) {
    var path = "./images/anime/"
    if ((message.content.substring(0, 6) == "anime_".toLowerCase()) && (parseInt(message.content.substring(6))) != NaN) {
        console.log("Trying to find anime_" + parseInt(message.content.substring(6)))
        var num = parseInt(message.content.substring(6))
        var fileName = "anime_"
        channel.send(fileManager.sendImage(num, path, fileName, message, masterColor))
    } else {
      var num = Math.floor(Math.random() * fileManager.getAllDirFiles("./images/anime").length)
      console.log(fileManager.getAllDirFiles("./images/anime").length)
      var fileName = "anime_"
      if (num == 5) {
        console.log("Rerolling...")
        num = Math.floor(Math.random() * fileManager.getAllDirFiles("./images/anime").length)
      }
      channel.send(fileManager.sendImage(num, path, fileName, message, masterColor))
    }  
}

if ((message.content.toLowerCase().includes("happy".toLowerCase()) == true) && (message.content.toLowerCase().includes("birth".toLowerCase()) == true)) {
var date = new Date()
if ((date.setHours(0,0,0,0) - birthdayLastDate.setHours(0,0,0,0)) > 0) {
  birthdayLastDate = date
  console.log("Happy birthday!")
  bot.uploadFile({
    to: channelID,
    file: './images/happybirthday.gif'
  });
}
}

if (message.content.toLowerCase().includes("OwO".toLowerCase()) == true || message.content.toLowerCase().includes("Uwu".toLowerCase()) == true) {
  console.log("OwO")
  var embed= new Discord.MessageEmbed()
    .attachFiles(['./images/owo.png'])
    .setImage('attachment://owo.png');

  channel.send(embed);
}

if (message.content.toLowerCase().includes("is it possible to learn this power".toLowerCase()) == true) {
console.log("Is it possible to learn this power?")
  bot.uploadFile({
    to: channelID,
    file: './video/Palpatine_00.mp4'
  });
}

if (message.content.toLowerCase().includes("hot".toLowerCase()) == true) {
console.log("HOT")
  bot.uploadFile({
    to: channelID,
    file: './video/Hot.mp4'
  });
}

if (message.content.toLowerCase().includes("the sun is a deadly lazer".toLowerCase()) == true || message.content.toLowerCase().includes("the sun is a deadly laser".toLowerCase()) == true) {
console.log("The sun is a deadly lazer!")
  bot.uploadFile({
    to: channelID,
    file: './video/Blanket.mp4'
  });
}

if (message.content.toLowerCase().includes("10th time".toLowerCase()) == true) {
console.log("9th time")
message.channel.send("9th time!");
}

if (message.content.toLowerCase().includes("sauce".toLowerCase()) == true && !(message.content.includes("Sauce: "))) {
  var num = Math.floor(Math.random() * Math.floor(321861))
  console.log("Sauce: " + num)
  console.log("nhentai.net/g/" + num)
  sauce = "Sauce: " + num
            message.channel.send(sauce);
}

if (message.content.toLowerCase().includes("heresy".toLowerCase()) == true) {
  var num = Math.floor(Math.random() * fileManager.getAllDirFiles("./images/heresy").length)
  console.log("HERESY!!")
  if ((message.content.substring(0, 7) == "heresy_".toLowerCase()) && (parseInt(message.content.substring(7))) != NaN) {
      console.log("Trying to find heresy_" + parseInt(message.content.substring(7)))
      var num = parseInt(message.content.substring(7))
      var fileName = "./images/heresy/heresy_"
      channel.send(fileManager.sendImage(num, path, fileName, message, masterColor))
  } else {
    var num = Math.floor(Math.random() * fileManager.getAllDirFiles("./images/heresy").length)
    console.log(fileManager.getAllDirFiles("./images/heresy").length)
    var fileName = "./images/heresy/heresy_"
    channel.send(fileManager.sendImage(num, path, fileName, message, masterColor))
  }
}

if (message.content.toLowerCase().includes("ravioli ravioli".toLowerCase()) == true) {
  console.log("Don't lewd the drangon loli!")
          var data = {
              "to": channelID,
              message: "don't lewd the dragon loli",
              "embed": {
                  "image": {
                    "url": './images/ravioli.gif'
                  }
                }
            };
            bot.sendMessage(data);
}

if (message.content.toLowerCase().includes("hentai".toLowerCase()) == true) {
console.log("Hentai!")
  // bot.sendMessage({
  //     to: channelID,
  //     message.content: "WAIT THAT'S ILLEGAL!"
  // });
  bot.uploadFile({
    to: channelID,
    file: './images/hentai.gif'
  });
}

if (message.content.toLowerCase().includes("hello there".toLowerCase()) == true) {
console.log("Hello there!")
bot.uploadFile({
  to: channelID,
  file: './images/generalkenobi.gif'
});
}

if (message.content.toLowerCase().includes("trap".toLowerCase()) == true) {
console.log("It's a trap!")
  bot.sendMessage({
      to: channelID,
      "embed": {
          "image": {
            "url": 'https://i.kym-cdn.com/photos/images/newsfeed/001/297/055/875.gif'
          }
        }
  });
}

if (message.content.substring(0, 1) == '!') {
  var args = message.content.substring(1).split(' ');
  var cmd = args[0];
  console.log("Command issued " + message.content) 

  args = args.splice(1);

  if (message.content.toLowerCase().includes("selfie".toLowerCase()) == true) {
    if ((message.content.substring(0, 8) == "!selfie_".toLowerCase()) && (parseInt(message.content.substring(8))) != NaN) {
        console.log("Trying to find selfie_" + parseInt(message.content.substring(8)))
        var num = parseInt(message.content.substring(8))
        var fileName = "./images/selfies/selfie_"
        fileManager.sendImage(num, fileName, channelID, message.content, bot)
    } else {
      var num = Math.floor(Math.random() * fileManager.getAllDirFiles("./images/selfies").length)
      console.log(fileManager.getAllDirFiles("./images/selfies").length)
      while (num == lastNum) {
        num = Math.floor(Math.random() * fileManager.getAllDirFiles("./images/selfies").length)
      }
      lastNum = num
      var fileName = "./images/selfies/selfie_"
      fileManager.sendImage(num, fileName, channelID, message.content, bot)
    }  
  }
 
  if (message.content.toLowerCase().includes('who is'.toLowerCase()) == true){
      if (message.content.toLowerCase().includes('your mother'.toLowerCase()) == true) {
          message.channel.send('Isaac is my mother');
      } else if (message.content.toLowerCase().includes('your father'.toLowerCase()) == true) {
          bot.sendMessage({
              to: channelID,
              message: 'Geoffery is my father',
              "embed": {
                  "image": {
                  "url": 'https://avatars3.githubusercontent.com/u/43981091?s=460&u=7216909e10eaadc9ab9263e93ef6c46560fb8c03&v=4'
                  }
              }
          });
      } else if (message.content.toLowerCase().includes('step mother'.toLowerCase()) == true) {
          message.channel.send('Seth is my step mother');
      } else if (message.content.toLowerCase().includes('your brother'.toLowerCase()) == true) {
          message.channel.send('Connor is my brother');
      } else {
          message.channel.send('Who?');
      }
  } else if (message.content.toLowerCase().includes('roll_d'.toLowerCase()) == true) { 
    var dice = 1
    dice = parseInt(cmd.substring(6))
    var num = Math.floor(Math.random() * dice) + 1;
    bot.sendMessage({
      to: channelID,
      message: ("You rolled " + num)
  });
  } else if (message.content.toLowerCase().includes('sins'.toLowerCase()) == true) { 
    /* var mention = message.content.substring(6)
    if (mention.startsWith(' ')) {
      mention = mention.substring(1)
    }
    if (mention.startsWith('<@') && mention.endsWith('>')) {
      mention = mention.slice(2, -1);
  
      if (mention.startsWith('!')) {
        mention = mention.slice(1);
      }
    } */
    //var user = client.users.cache.get(mention)
    if (!message.mentions.users.size) {
      message.channel.send('You need to tag someone to get their sins...');
    } else {
      var member;
      const taggedUser = message.mentions.users.first();
      console.log(`Sins of: ${taggedUser.username}`)
      member = members.checkMember(taggedUser.username, taggedUser.id)
      console.log(`Sins: ${member}`)
      var data = {
        "to": channel,
        "embed": {
          "title": `Sins of ${taggedUser.username}`,
          "description": member.sins,
          "color": 7871916,
          "thumbnail": {
            "url": taggedUser.displayAvatarURL({ format: "png", dynamic: true }),
          }
        }
      };
      channel.send(data);
    }
    //var member = members.checkMember(taggedUser.user, tagged.userID)
    /* 
    } else if (message.content.toLowerCase().includes("Randy".toLowerCase()) == true) {
      name = "Randy"
      info = "Alcoholic, Rage Baby, Owner of The Broken Sleep, Inquisitor"
    } else if (message.content.toLowerCase().includes("Pete".toLowerCase()) == true) {
      name = "Pete"
      info = "Generic heresy"
    } else if (message.content.toLowerCase().includes("Andy".toLowerCase()) == true) {
      name = "Andy"
      info = "Heretic Detector"
    } else if ((message.content.toLowerCase().includes("Nathanial".toLowerCase()) == true) || (message.content.toLowerCase().includes("DonutMc_Pastery".toLowerCase()) == true)) {
      name = "Nathanial"
      info = "weeb, Denier of Meta, Owner of The Broken Sleep"
    } else if (message.content.toLowerCase().includes("Katherine".toLowerCase()) == true) {
      name = "Katherine"
      info = "Furry, Sickly, Betrothed to the Evil Dragon God, Baker of Cookies"
    } */
    
  } else {
    var url = "";
      switch(cmd) {
          case 'ping':
            message.channel.send('What are you expecting? Me to say pong back?');
          break;
          case 'wtf':
            message.channel.send('Rude!');
          break;
          case 'nani':
            message.channel.send('何');
          break;
          case 'lastNum':
            message.channel.send(("The last gif number was: " + lastNum));
          break;
          case 'random':
            var text = randomMod.randomCommands()
            message.channel.send((text));
          break;
          case 'birthdayReset':
              birthdayLastDate = new Date(2019,3,31)
              message.channel.send("Cooldown reset");
          break;
          case 'thispersondoesnotexist':
            var plScraper = require('./pl-scraper')
            url = "https://thispersondoesnotexist.com/";
            var filePath = "./images/thispersondoesnotexist/"
            var name = "tpdne.jpg"
            console.log(filePath + name)
            plScraper.makeScrape(url, filePath, name);
            bot.uploadFile({
              to: channelID,
              file: filePath + name
            });
          break;
            case 'waifu':
            var num = Math.floor(Math.random() * 100000)
            url = "https://www.thiswaifudoesnotexist.net/example-" + num + ".jpg";
            var filePath = "./images/waifu/"
            var name = "waifu"
            console.log(url)

            bot.sendMessage({
              to: channelID,
              "embed": {
                  "image": {
                    "url": url
                  }
                }
          });
          break;
          case 'joke':
            //Info at: https://sv443.net/jokeapi/v2/
            url = "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=racist&type=single";

            https.get(url, res => {
              res.setEncoding("utf8");
              let body = "";
              res.on("data", data => {
                body += data;
              });
              res.on("end", () => {
                body = JSON.parse(body);
                console.log(body);
                console.log(body.joke)
                var text = body.joke
                bot.sendMessage({
                  to: channelID,
                  message: (body.joke)
                });
              });
            });
          break;
          case 'insultme':
            //Info at: https://evilinsult.com/api/
            url = "https://evilinsult.com/generate_insult.php?lang=en&type=json";

            https.get(url, res => {
              res.setEncoding("utf8");
              let body = "";
              res.on("data", data => {
                body += data;
              });
              res.on("end", () => {
                body = JSON.parse(body);
                console.log(body);
                console.log(body.insult)
                var text = body.insult
                bot.sendMessage({
                  to: channelID,
                  message: (body.insult)
                });
              });
            });
            break;
          case 'yesorno':
            //Info at: https://yesno.wtf/api
            url = "https://yesno.wtf/api";

            https.get(url, res => {
              res.setEncoding("utf8");
              let body = "";
              res.on("data", data => {
                body += data;
              });
              res.on("end", () => {
                body = JSON.parse(body);
                console.log(body);
                console.log(body.answer)
                var text = body.answer
                bot.sendMessage({
                  to: channelID,
                  message: (body.answer)
                });
              });
            });
          break;
          case 'fact':
            //Info at: https://uselessfacts.jsph.pl/
            url = "https://uselessfacts.jsph.pl/random.json?language=en";

            https.get(url, res => {
              res.setEncoding("utf8");
              let body = "";
              res.on("data", data => {
                body += data;
              });
              res.on("end", () => {
                body = JSON.parse(body);
                console.log(body);
                console.log(body.text)
                var text = body.text
                bot.sendMessage({
                  to: channelID,
                  message: (body.text)
                });
              });
            });
          break;
          case 'cat':
            url = "https://api.thecatapi.com/v1/images/search?api_key=b9a826e6-fac5-43e7-8af1-aa47523e1bbd";

            https.get(url, res => {
              res.setEncoding("utf8");
              let body = "";
              res.on("data", data => {
                body += data;
              });
              res.on("end", () => {
                body = JSON.parse(body);
                console.log(body);
                var data = body[0]
                console.log(data)
                url = data.url
                var embed = {
                  "image": {
                    "url": url
                  }
                };
                message.channel.send({ embed });
              });
            });
          break;
          case 'r2loadout':
            // Start selection... Picking survivor
            var survivor = riskofrain2.randomLoadout('survivor')
            var white = riskofrain2.randomLoadout('white')
            var green = riskofrain2.randomLoadout('green')
            var red = riskofrain2.randomLoadout('red')
            var equipment = riskofrain2.randomLoadout('equipment')
            var yellow = riskofrain2.randomLoadout('yellow')
            var lunar = riskofrain2.randomLoadout('lunar')
            var lunarEquipment = riskofrain2.randomLoadout('lunarEquipment')
            //console.log("Loadout Data: %s - %s - %s - %s - %s - %s - %s - %s", survivor, white, green, red, equipment, yellow, lunar, lunarEquipment)
            var data = {
              "to": channel,
              "message": "Good luck survivor...",
              "embed": {
                "title": "Risk of Rain 2 - Random Loadout",
                "description": "Item info can be found at the [Risk of Rain 2 Wiki](https://riskofrain2.gamepedia.com/Items).",
                "color": 4726857,
                "footer": {
                  "icon_url": "https://static.wikia.nocookie.net/be327120-a2dd-4467-bf86-8c2212037668",
                  "text": "Good luck survivor..."
                },
                "thumbnail": {
                  "url": survivor
                },
                "fields": [
                  {
                    "name": "White",
                    "value": white
                  },
                  {
                    "name": "Green",
                    "value": green
                  },
                  {
                    "name": "Red",
                    "value": red
                  },
                  {
                    "name": "Equipment",
                    "value": equipment
                  },
                  {
                    "name": "Yellow",
                    "value": yellow
                  },
                  {
                    "name": "Lunar",
                    "value": lunar
                  },
                  {
                    "name": "Lunar Equipment",
                    "value": lunarEquipment
                  }
                ]
              }
            };
            channel.send(data);
          break;
          case 'help':
            console.log("Sending help!")
            var data = {
                    to: channel,
                    "embed": {
                      "title": "Commands",
                      "description": "This is a list of all the commands I can do:",
                      "fields": [
                        {
                          "name": "anime",
                          "value": "Anime gif\nIf send \"anime_<number>\" then you can call a specific gif."
                        },
                        {
                          "name": "hentai",
                          "value": "That's illegal!"
                        },
                        {
                          "name": "owo or uwu",
                          "value": "owo"
                        },
                        {
                          "name": "sauce",
                          "value": "nhentai.net/g/<number>"
                        },
                        {
                          "name": "heresy",
                          "value": "Yikes that bad?"
                        },
                        {
                          "name": "ravioli ravioli",
                          "value": "DON'T LEWD!"
                        },
                        {
                          "name": "hello there",
                          "value": "It's a star wars reference"
                        },
                        {
                          "name": "trap",
                          "value": "Danger!"
                        },
                        {
                          "name": "!ping",
                          "value": "Pong probably"
                        },
                        {
                          "name": "!r2loadout",
                          "value": "Gives you a complete random Risk of Rain 2 loadout to use in your next Artifact of Command run."
                        },
                        {
                          "name": "!wtf",
                          "value": "That's mean!"
                        },
                        {
                          "name": "!roll_d<Your Number Here>",
                          "value": "Roll any dice. Example: !roll_d20"
                        },
                        {
                          "name": "!nani",
                          "value": "What?"
                        },
                        {
                          "name": "!fact",
                          "value": "I'll tell you a random fact."
                        },
                        {
                          "name": "!joke",
                          "value": "I'll tell you a joke."
                        },
                        {
                          "name": "!insultme",
                          "value": "I'll tell you a different kind of joke..."
                        },
                        {
                          "name": "!yesorno",
                          "value": "I'll tell you yes or no."
                        },
                        {
                          "name": "!selfie",
                          "value": "I'll send you a random picture of me."
                        },
                        {
                          "name": "!cat",
                          "value": "Random cat pictures from Tumblr."
                        },
                        {
                          "name": "!thispersondoesnotexist",
                          "value": "Generates a person that does not exist."
                        },
                        {
                          "name": "!waifu",
                          "value": "Generates a waifu for you to love. <3"
                        },
                        {
                          "name": "!random",
                          "value": "One command sent at random..."
                        },
                        {
                          "name": "!lastNum",
                          "value": "I'll tell you the number of the last gif I sent. (Number 94 of an anime gif would equal anime_94)"
                        },
                        {
                          "name": "!birthdayReset",
                          "value": "Reset the cooldown on birthday messages."
                        },
                        {
                          "name": "!who is my \"Family Member Here\"",
                          "value": "I will reveal some of my relations..."
                        },
                        {
                          "name": "!help",
                          "value": "You just did that..."
                        }
                      ]
                    }
              };
              channel.send(data);
          break;
      }
  }
}


    
});