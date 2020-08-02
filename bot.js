var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
const fs = require('fs')
var lastNum = -1;
var birthdayLastDate = new Date(2019,3,31) 
// Require the module in your project
 
const getAllDirFiles = function(dirPath, arrayOfFiles) {
  files = fs.readdirSync(dirPath)

  arrayOfFiles = arrayOfFiles || []

  files.forEach(function(file) {
    if (fs.statSync(dirPath + "/" + file).isDirectory()) {
      arrayOfFiles = getAllFiles(dirPath + "/" + file, arrayOfFiles)
    } else {
      arrayOfFiles.push(file)
    }
  })

  return arrayOfFiles
}

const sendImage = function (num, fileName, channelID, message, bot) {
  lastNum = num;
  if (num <= 9) {
    fileName = fileName + "0" + num;
  } else {
    fileName = fileName + num;
  }
  if(fs.existsSync(fileName + ".gif")){
    fileName = fileName + ".gif"
    console.log(fileName)
    bot.uploadFile({
      to: channelID,
      file: fileName
  });
  } else if (fs.existsSync(fileName + ".png")) {
    fileName = fileName + ".png"
    console.log(fileName)
    bot.uploadFile({
      to: channelID,
      file: fileName
  });
  } else if (fs.existsSync(fileName + ".jpg")) {
      fileName = fileName + ".jpg"
      console.log(fileName)
      bot.uploadFile({
        to: channelID,
        file: fileName
  });
  } else if (fs.existsSync(fileName + ".mp4")) {
      fileName = fileName + ".mp4"
      console.log(fileName)
      bot.uploadFile({
        to: channelID,
        file: fileName
  });
  } else if (fs.existsSync(fileName + ".mov")) {
    fileName = fileName + ".mov"
    console.log(fileName)
    bot.uploadFile({
      to: channelID,
      file: fileName
  });
  } else {
    console.log("Error " + fileName + " not found...")
    bot.sendMessage({
      to: channelID,
      message: "This ain't it chief. I couldn't find the gif."
  });
  }
};

const sinList = function (message) {
  var list = "";  
  if (message.toLowerCase().includes("Connor".toLowerCase()) == true) {
    list = "Connor\nweeb, Furry, Bird, Faithful to Garbobo, Creator of All\n"
  } 
  if (message.toLowerCase().includes("Geoffery".toLowerCase()) == true) {
    list = "Geoffery\nBusy, weeb, Birthplace of Sin, Faithless, Hostess of Servers\n"
  } 
  if (message.toLowerCase().includes("Seth".toLowerCase()) == true) {
    list = "Seth\nGay, weeb, Garden of Sin, Rage Baby\n"
  } 
  if (message.toLowerCase().includes("Riley".toLowerCase()) == true) {
    list = "Riley\nHentai, Knower of truths, Weeb, Meem lord, Denial of wrongdoing, priest of garbobo, BAbaBa\n"
  } 
  if (message.toLowerCase().includes("Randy".toLowerCase()) == true) {
    list = "Randy\nAlcoholic, Rage Baby, Owner of The Broken Sleep, Inquisitor\n"
  } 
  if (message.toLowerCase().includes("Isaac".toLowerCase()) == true) {
    list = "Isaac\nweeb, Scalie, Hentai,  Murderer, Faithless, Cataloger of Crimes\n"
  } 
  if (message.toLowerCase().includes("Pete".toLowerCase()) == true) {
    list = "Pete\nGeneric heresy\n"
  } 
  if (message.toLowerCase().includes("Andy".toLowerCase()) == true) {
    list = "Andy\nHeretic Detector\n"
  }
  if ((message.toLowerCase().includes("Nathanial".toLowerCase()) == true) || (message.toLowerCase().includes("DonutMc_Pastery".toLowerCase()) == true)) {
    list = "Nathanial\nweeb, Denier of Meta, Owner of The Broken Sleep\n"
  }
  if (message.toLowerCase().includes("Katherine".toLowerCase()) == true) {
    list = "Katherine\nFurry, Sickly, Betrothed to the Evil Dragon God, Baker of Cookies\n"
  }

  return list
}

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
    // Our bot needs to know if it will execute a command
    // It will listen for messages that will start with `!`

    if (message.toLowerCase().includes("anime".toLowerCase()) == true) {
      {
          if ((message.substring(0, 6) == "anime_".toLowerCase()) && (parseInt(message.substring(6))) != NaN) {
              console.log("Trying to find anime_" + parseInt(message.substring(6)))
              var num = parseInt(message.substring(6))
              var fileName = "./images/anime/anime_"
              sendImage(num, fileName, channelID, message, bot)
          } else {
            var num = Math.floor(Math.random() * getAllDirFiles("./images/anime").length)
            console.log(getAllDirFiles("./images/anime").length)
            var fileName = "./images/anime/anime_"
            if (num == 5) {
              console.log("Rerolling...")
              num = Math.floor(Math.random() * getAllDirFiles("./images/anime").length)
            }
            sendImage(num, fileName, channelID, message, bot)
          }
      }
          
    }

    if ((message.toLowerCase().includes("happy".toLowerCase()) == true) && (message.toLowerCase().includes("birth".toLowerCase()) == true)) {
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

    if (message.toLowerCase().includes("OwO".toLowerCase()) == true || message.toLowerCase().includes("Uwu".toLowerCase()) == true) {
      console.log("OwO")
        bot.uploadFile({
          to: channelID,
          file: './images/owo.png'
        });
    }

    if (message.toLowerCase().includes("is it possible to learn this power".toLowerCase()) == true) {
      console.log("Is it possible to learn this power?")
        bot.uploadFile({
          to: channelID,
          file: './video/Palpatine_00.mp4'
        });
    }

    if (message.toLowerCase().includes("hot".toLowerCase()) == true) {
      console.log("HOT")
        bot.uploadFile({
          to: channelID,
          file: './video/Hot.mp4'
        });
    }

    if (message.toLowerCase().includes("the sun is a deadly lazer".toLowerCase()) == true || message.toLowerCase().includes("the sun is a deadly laser".toLowerCase()) == true) {
      console.log("The sun is a deadly lazer!")
        bot.uploadFile({
          to: channelID,
          file: './video/Blanket.mp4'
        });
    }

    if (message.toLowerCase().includes("10th time".toLowerCase()) == true) {
      console.log("9th time")
      bot.sendMessage({
        to: channelID,
        message: "9th time!"
    });
    }

    if (message.toLowerCase().includes("sauce".toLowerCase()) == true && !(message.includes("Sauce: "))) {
        var num = Math.floor(Math.random() * Math.floor(321861))
        console.log("Sauce: " + num)
        console.log("nhentai.net/g/" + num)
        sauce = "Sauce: " + num
                  bot.sendMessage({
                    to: channelID,
                    message: sauce
                });
    }

    if (message.toLowerCase().includes("heresy".toLowerCase()) == true) {
        var num = Math.floor(Math.random() * getAllDirFiles("./images/heresy").length)
        console.log("HERESY!!")
        if ((message.substring(0, 7) == "heresy_".toLowerCase()) && (parseInt(message.substring(7))) != NaN) {
            console.log("Trying to find heresy_" + parseInt(message.substring(7)))
            var num = parseInt(message.substring(7))
            var fileName = "./images/heresy/heresy_"
            sendImage(num, fileName, channelID, message, bot)
        } else {
          var num = Math.floor(Math.random() * getAllDirFiles("./images/heresy").length)
          console.log(getAllDirFiles("./images/heresy").length)
          var fileName = "./images/heresy/heresy_"
          sendImage(num, fileName, channelID, message, bot)
        }
    }

    if (message.toLowerCase().includes("ravioli ravioli".toLowerCase()) == true) {
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

    if (message.toLowerCase().includes("hentai".toLowerCase()) == true) {
      console.log("Hentai!")
        // bot.sendMessage({
        //     to: channelID,
        //     message: "WAIT THAT'S ILLEGAL!"
        // });
        bot.uploadFile({
          to: channelID,
          file: './images/hentai.gif'
        });
    }

    if (message.toLowerCase().includes("hello there".toLowerCase()) == true) {
      console.log("Hello there!")
      bot.uploadFile({
        to: channelID,
        file: './images/generalkenobi.gif'
      });
  }

    if (message.toLowerCase().includes("trap".toLowerCase()) == true) {
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

    if (message.substring(0, 1) == '!') {
        var args = message.substring(1).split(' ');
        var cmd = args[0];
        console.log("Command issued " + message) 
       
        args = args.splice(1);
        if (message.toLowerCase().includes('who is'.toLowerCase()) == true){
            if (message.toLowerCase().includes('your mother'.toLowerCase()) == true) {
                bot.sendMessage({
                    to: channelID,
                    message: 'Isaac is my mother'
                });
            } else if (message.toLowerCase().includes('your father'.toLowerCase()) == true) {
                bot.sendMessage({
                    to: channelID,
                    message: 'Geoffery is my father',
                    "embed": {
                        "image": {
                        "url": 'https://avatars3.githubusercontent.com/u/43981091?s=460&u=7216909e10eaadc9ab9263e93ef6c46560fb8c03&v=4'
                        }
                    }
                });
            } else if (message.toLowerCase().includes('step mother'.toLowerCase()) == true) {
                bot.sendMessage({
                    to: channelID,
                    message: 'Seth is my step mother'
                });
            } else if (message.toLowerCase().includes('your brother'.toLowerCase()) == true) {
                bot.sendMessage({
                    to: channelID,
                    message: 'Connor is my brother'
                });
            } else {
                bot.sendMessage({
                    to: channelID,
                    message: 'Who?'
                });
            }
        } else if (message.toLowerCase().includes('roll_d'.toLowerCase()) == true) { 
          var dice = 1
          dice = parseInt(cmd.substring(6))
          var num = Math.floor(Math.random() * dice) + 1;
          bot.sendMessage({
            to: channelID,
            message: ("You rolled " + num)
        });
        } else if (message.toLowerCase().includes('sins'.toLowerCase()) == true) { 
          var name = ""
          var info = ""
          if (message.toLowerCase().includes("Connor".toLowerCase()) == true) {
            name = "Connor"
            info = "weeb, Furry, Bird, Faithful to garbobo, Creator of All"
          } else if (message.toLowerCase().includes("Geoffery".toLowerCase()) == true) {
            name = "Geoffery"
            info = "Busy, weeb, Birthplace of Sin, Faithless, Hostess of Servers"
          } else if (message.toLowerCase().includes("Seth".toLowerCase()) == true) {
            name = "Seth"
            info = "Gay, weeb, Garden of Sin, Rage Baby"
          } else if (message.toLowerCase().includes("Riley".toLowerCase()) == true) {
            name = "Riley"
            info = "Hentai, Knower of truths, Weeb, Meem lord, Denial of Wrongdoing, Priest of Garbobo, BAbaBa"
          } else if (message.toLowerCase().includes("Randy".toLowerCase()) == true) {
            name = "Randy"
            info = "Alcoholic, Rage Baby, Owner of The Broken Sleep, Inquisitor"
          } else if (message.toLowerCase().includes("Isaac".toLowerCase()) == true) {
            name = "Isaac"
            info = "weeb, Scalie, Hentai,  Murderer, Faithless, Cataloger of Crimes"
          } else if (message.toLowerCase().includes("Pete".toLowerCase()) == true) {
            name = "Pete"
            info = "Generic heresy"
          } else if (message.toLowerCase().includes("Andy".toLowerCase()) == true) {
            name = "Andy"
            info = "Heretic Detector"
          } else if ((message.toLowerCase().includes("Nathanial".toLowerCase()) == true) || (message.toLowerCase().includes("DonutMc_Pastery".toLowerCase()) == true)) {
            name = "Nathanial"
            info = "weeb, Denier of Meta, Owner of The Broken Sleep"
          } else if (message.toLowerCase().includes("Katherine".toLowerCase()) == true) {
            name = "Katherine"
            info = "Furry, Sickly, Betrothed to the Evil Dragon God, Baker of Cookies"
          } else {
            name = message.substring(5)
            info = "Sinless... for now..."
          }
          
          bot.sendMessage({
            to: channelID,
            "embed": {
              "title": name,
              "description": info
            }
        });
        } else {
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
                case 'nani':
                    bot.sendMessage({
                            to: channelID,
                            message: '何'
                    });
                break;
                case 'lastNum':
                    bot.sendMessage({
                            to: channelID,
                            message: ("The last gif number was: " + lastNum)
                    });
                break;
                case 'birthdayReset':
                    birthdayLastDate = new Date(2019,3,31)
                    bot.sendMessage({
                      to: channelID,
                      message: ("Cooldown reset")
                    });
                break;
                case 'help':
                  console.log("Sending help!")
                    bot.sendMessage({
                            to: channelID,
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
                    });
                break;
            }
        }
     }
});