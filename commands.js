var riskofrain2 = require('./riskofrain2.js');
var mcRCON = require('./mcRCON.js');
var https = require('https');
var fileManager = require('./fileManager.js');
var randomMod = require('./randomMod.js');
var members = require('./members.js');
const masterColor = 7871916

const command = function(client, message, channel, lastNum) 
{
  var args = message.content.substring(1).split(' ');
  var cmd = args[0];
  console.log("Command issued " + message.content) 

  args = args.splice(1);

  if (message.content.toLowerCase().includes("anime".toLowerCase()) == true) {
    var path = "./images/anime/"
    if ((message.content.substring(0, 7) == "!anime_".toLowerCase()) && (parseInt(message.content.substring(6))) != NaN) {
        console.log("Trying to find anime_" + parseInt(message.content.substring(7)))
        var num = parseInt(message.content.substring(7))
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

  if (message.content.toLowerCase().includes("selfie".toLowerCase()) == true) {
    var path = "./images/selfies/"
    if ((message.content.substring(0, 8) == "!selfie_".toLowerCase()) && (parseInt(message.content.substring(8))) != NaN) {
        console.log("Trying to find selfie_" + parseInt(message.content.substring(8)))
        var num = parseInt(message.content.substring(8))
        var fileName = "selfie_"
        channel.send(fileManager.sendImage(num, path, fileName, message, masterColor))
    } else {
      var num = Math.floor(Math.random() * fileManager.getAllDirFiles("./images/selfies").length)
      console.log(fileManager.getAllDirFiles("./images/selfies").length)
      while (num == lastNum) {
        num = Math.floor(Math.random() * fileManager.getAllDirFiles("./images/selfies").length)
      }
      lastNum = num
      var fileName = "selfie_"
      channel.send(fileManager.sendImage(num, path, fileName, message, masterColor))
    }  
  }

  if (message.content.toLowerCase().includes("!broadcast".toLowerCase()) == true) {
    message.content = message.content.substring(10)  

    client.channels.cache.get('254779349352448001').send(message.content);
  }
 
  if (message.content.toLowerCase().includes('who is'.toLowerCase()) == true){
      if (message.content.toLowerCase().includes('your mother'.toLowerCase()) == true) {
          message.channel.send('<@!256343280285908992> is my mother');
      } else if (message.content.toLowerCase().includes('your father'.toLowerCase()) == true) {
        message.channel.send('<@!253710834553847808> is my father');
      } else if (message.content.toLowerCase().includes('step mother'.toLowerCase()) == true) {
          message.channel.send('<@!280117740222676992> is my step mother');
      } else if (message.content.toLowerCase().includes('your brother'.toLowerCase()) == true) {
          message.channel.send('<@!251488731750465536> is my brother');
      } else {
          message.channel.send('Who?');
      }
  } else if (message.content.toLowerCase().includes('roll_d'.toLowerCase()) == true) { 
    var dice = 1
    dice = parseInt(cmd.substring(6))
    var num = Math.floor(Math.random() * dice) + 1;
    var embed = {
      "embed": {
        "description": `You rolled ${num} on your d${dice}. Good job! At the very least you get an A+ for effort so isn't that nice.`,
        "color": 2464068,
        "thumbnail": {
          "url": "https://gilkalai.files.wordpress.com/2017/09/dice.png?w=640"
        },
        "author": {
          "name": "Steve from Accounting",
          "url": "https://www.google.com/error",
          "icon_url": "https://www.topaccountingdegrees.org/wp-content/uploads/2015/08/Accounting-7.jpg"
        }
      }
    };
    channel.send(embed);
  } else if (message.content.toLowerCase().includes('sins'.toLowerCase()) == true) { 
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
            channel.send({
              files: [(filePath + name)]
            });
          break;
            case 'waifu':
            var num = Math.floor(Math.random() * 100000)
            url = "https://www.thiswaifudoesnotexist.net/example-" + num + ".jpg";
            var filePath = "./images/waifu/"
            var name = "waifu"
            console.log(url)

            var embed = {
              "image": {
                  "url": url
                }
              };
          case 'waifu':
            var num = Math.floor(Math.random() * 100000)
            url = "https://www.thiswaifudoesnotexist.net/example-" + num + ".jpg";
            var filePath = "./images/waifu/"
            var name = "waifu"
            console.log(url)

            var embed = {
              "image": {
                  "url": url
                }
              };
          message.channel.send({ embed });
          break;
          case 'hot':
            console.log("HOT")
            channel.send({
              files: ['./video/Hot.mp4']
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
                channel.send(body.joke);
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
                channel.send(body.insult);
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
                channel.send(body.answer);
              });
            });
          break;
          case 'mcday':
            console.log("Gettting Server Stat")
            mcRCON.sendCommand('time set day', channel)
          break;
          case 'mcnight':
            console.log("Gettting Server Stat")
            mcRCON.sendCommand('time set night', channel)
          break;
          case 'mctime':
            console.log("Gettting Server Stat")
            mcRCON.sendCommand('time world', channel)
          break;
          case 'mcseed':
            console.log("Gettting Server Stat")
            mcRCON.sendCommand('seed', channel)
          break;
          case 'mcinfo':
            console.log("Gettting Server Stat")
            mcRCON.LookServerFL(channel)
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
                var embed = {
                    "embed": {
                      "description": `Fact: ${text}\nSource: [${body.source}](${body.source_url})`,
                      "url": "https://discordapp.com",
                      "color": 4550821,
                      "author": {
                        "name": "Dr. Fact",
                        "url": "https://uselessfacts.jsph.pl/",
                        "icon_url": "https://img.icons8.com/bubbles/2x/light-on.png"
                      }
                    }
                  };
                  channel.send(embed);
                });
              });
          break;
          case 'advise':
            //Info at: https://api.adviceslip.com/
            url = "https://api.adviceslip.com/advice";

            https.get(url, res => {
              res.setEncoding("utf8");
              let body = "";
              res.on("data", data => {
                body += data;
              });
              res.on("end", () => {
                body = JSON.parse(body);
                console.log(body);
                console.log(body.slip.advice)
                var text = body.slip.advice
                var embed = {
                    "embed": {
                      "description": `Advice: ${text}`,
                      "url": "https://discordapp.com",
                      "color": 4550821,
                      "author": {
                        "name": "Advice Co.",
                        "url": "https://api.adviceslip.com/",
                        "icon_url": "https://www.partnersinprojectgreen.com/wp-content/uploads/2017/01/PPG_EV_ICON_HELP.png"
                      }
                    }
                  };
                  channel.send(embed);
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
          case 'zerotier':
            embed = {
              "embed": {
                "title": "ZeroTier Info",
                "url": "https://www.zerotier.com/",
                "color": 16763904,
                "thumbnail": {
                  "url": "https://my.zerotier.com/img/zerotier-logo-white.png"
                },
                "author": {
                  "name": "ZeroTier",
                  "url": "https://discordapp.com",
                  "icon_url": "https://my.zerotier.com/img/zerotier-logo-white.png"
                },
                "fields": [
                  {
                    "name": "Step 1",
                    "value": "[Download ZeroTier](https://www.zerotier.com/download/) and install it."
                  },
                  {
                    "name": "Step 2",
                    "value": "Join: 8850338390b695d0 by right clicking the ZeroTier icon in the task bar."
                  },
                  {
                    "name": "Step 3",
                    "value": "DM Geoffery10 and let him know to let you into the server."
                  },
                  {
                    "name": "Step 4",
                    "value": "Wait patiently..."
                  }
                ]
              }
            }
            channel.send(embed);
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
                          "name": "hentai",
                          "value": "That's illegal!"
                        },
                        {
                          "name": "owo or uwu",
                          "value": "owo"
                        },
                        {
                          "name": "sauce",
                          "value": "DANGER NSFW"
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
                          "name": "!anime",
                          "value": "Anime gif\nIf send \"!anime_<number>\" then you can call a specific gif."
                        },
                        {
                          "name": "!r2loadout",
                          "value": "Gives you a complete random Risk of Rain 2 loadout to use in your next Artifact of Command run."
                        },
                        {
                          "name": "!mctime",
                          "value": "The time in the Minecraft Server (if running)."
                        },
                        {
                          "name": "!mcseed",
                          "value": "The seed of the Minecraft Server (if running)."
                        },
                        {
                          "name": "!wtf",
                          "value": "That's mean!"
                        },
                        {
                          "name": "!hot",
                          "value": "HOT!"
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
                          "name": "!advise",
                          "value": "I'll tell you a some advice if you are that desperate..."
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
  return lastNum
}

module.exports.command = command;