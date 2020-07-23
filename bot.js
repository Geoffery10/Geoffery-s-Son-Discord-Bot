var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
// Require the module in your project
 

// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = 'debug';
// Initialize Discord Bot
var bot = new Discord.Client({
   token: auth.token,
   autorun: true
});
bot.on('ready', function (evt) {
    logger.info('Connected');
    logger.info('Logged in as: ');
    logger.info(bot.username + ' - (' + bot.id + ')');
});
bot.on('message', function (user, userID, channelID, message, evt) {
    let animeURLs = ['https://pa1.narvii.com/6204/dd03582be2d57e47c5378cd1ab19b8f39b1b2e76_hq.gif', 'https://media.tenor.com/images/bccc03037137312c211cace52bafa84d/tenor.gif', 
'https://k60.kn3.net/taringa/4/6/7/4/4/4/7/zongbie/E5E.gif', 'https://i.gifer.com/6mh.gif', 'https://cdn.discordapp.com/attachments/542189375975456780/735572673211531334/tumblr_inline_nr18tghWcp1rjj2rl_500.gif',
'https://pa1.narvii.com/6858/a80b1f14084168ac795b13e6062915ab893489f1_hq.gif', 'https://media.tenor.com/images/7393ac30cca2839ca79f8f4d52feb979/tenor.gif']
    let heresy = ['https://cdn.discordapp.com/attachments/254779349352448001/735584631860232232/reee.gif', 'https://pbs.twimg.com/media/DSTz1dsVwAAQElr.jpg' ,
'https://cdn.discordapp.com/attachments/254779349352448001/735584844922486804/15_-_AncI19F.jpg', 'https://cdn.discordapp.com/attachments/254779349352448001/735585058072559626/heresy_detected.jpg',
'https://cdn.discordapp.com/attachments/254779349352448001/735585071678881924/140_-_SFf3Thm.gif', 'https://cdn.discordapp.com/attachments/254779349352448001/735585103392276550/intervention.jpg',
'https://cdn.discordapp.com/attachments/254779349352448001/735585142650830851/139_-_DJp3O3C.jpg', 'https://cdn.discordapp.com/attachments/254779349352448001/735585202671452340/134_-_pgkZxPT.gif',
'https://cdn.discordapp.com/attachments/254779349352448001/735585237425324083/tumblr_ouhspkqdzq1s83dh2o3_400.gif', 'https://cdn.discordapp.com/attachments/254779349352448001/735585310800347166/STOP.png', 
'https://cdn.discordapp.com/attachments/254779349352448001/735585433467093112/du_eet.jpg']
    // Our bot needs to know if it will execute a command
    // It will listen for messages that will start with `!`

    if (message.toLowerCase().includes("anime".toLowerCase()) == true) {
        var num = Math.floor(Math.random() * animeURLs.length)
                var data = {
                    "to": channelID,
                    "embed": {
                      "image": {
                        "url": animeURLs[num]
                      }
                    }
                  };
                  bot.sendMessage(data);
    }

    if (message.toLowerCase().includes("OwO".toLowerCase()) == true || message.toLowerCase().includes("Uwu".toLowerCase()) == true) {
        var num = Math.floor(Math.random() * animeURLs.length)
                var data = {
                    "to": channelID,
                    "embed": {
                        "image": {
                          "url": 'https://cdn.drawception.com/drawings/MPPrYcG3Xa.png'
                        }
                      }
                  };
                  bot.sendMessage(data);
    }

    if (message.toLowerCase().includes("sauce".toLowerCase()) == true && !(message.includes("Sauce: "))) {
        var num = Math.floor(Math.random() * Math.floor(321861))
        sauce = "Sauce: " + num
                  bot.sendMessage({
                    to: channelID,
                    message: sauce
                });
    }

    if (message.toLowerCase().includes("heresy".toLowerCase()) == true) {
        var num = Math.floor(Math.random() * heresy.length)
                var data = {
                    "to": channelID,
                    "embed": {
                        "image": {
                          "url": heresy[num]
                        }
                      }
                  };
                  bot.sendMessage(data);
    }

    if (message.toLowerCase().includes("ravioli ravioli".toLowerCase()) == true) {
        var num = Math.floor(Math.random() * heresy.length)
                var data = {
                    "to": channelID,
                    message: "don't lewd the dragon loli",
                    "embed": {
                        "image": {
                          "url": 'https://pa1.narvii.com/6524/9faa750f3d296da6e0e19dcbc8fe1beb7d5f9760_hq.gif'
                        }
                      }
                  };
                  bot.sendMessage(data);
    }

    if (message.toLowerCase().includes("hentai".toLowerCase()) == true) {
        bot.sendMessage({
            to: channelID,
            message: "WAIT THAT'S ILLEGAL!",
            "embed": {
                "image": {
                  "url": 'https://media0.giphy.com/media/wkW0maGDN1eSc/giphy.gif'
                }
              }
        });
    }

    if (message.toLowerCase().includes("trap".toLowerCase()) == true) {
        bot.sendMessage({
            to: channelID,
            "embed": {
                "image": {
                  "url": 'https://i.kym-cdn.com/photos/images/newsfeed/001/297/055/875.gif'
                }
              }
        });
    }

    if (message.substring(0, 1) == '!') {
        var args = message.substring(1).split(' ');
        var cmd = args[0];
       
        args = args.splice(1);
        switch(cmd) {
            // !ping
            case 'ping':
                bot.sendMessage({
                    to: channelID,
                    message: 'What are you expecting? Me to say pong back?'
                });
            break;
            case 'wtf':
                bot.sendMessage({
                    to: channelID,
                    message: 'Rude!'
                });
            break;
            case 'rolld20':
                bot.sendMessage({
                    to: channelID,
                    "embed": {
                        "image": {
                          "url": 'https://media1.tenor.com/images/2cf373aef8fedfa21cc1f5587a6f9e2b/tenor.gif?itemid=8620719'
                        }
                      }
                });
            break;
            case 'nani':
                bot.sendMessage({
                        to: channelID,
                        message: '何'
                });
            break;
         }
     }
});