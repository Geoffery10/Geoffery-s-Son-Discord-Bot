const Discord = require('discord.js');
const client = new Discord.Client();
var logger = require('winston');
var auth = require('./auth.json');
var fileManager = require('./fileManager.js');
var riskofrain2 = require('./riskofrain2.js');
var randomMod = require('./randomMod.js');
var members = require('./members.js');
var mcRCON = require('./mcRCON.js');
var commands = require('./commands.js');
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
    var embed= new Discord.MessageEmbed()
      .attachFiles(['./images/happybirthday.gif'])
      .setImage('attachment://happybirthday.gif');

    channel.send(embed);
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
  channel.send({
    files: ['./video/Palpatine_00.mp4']
  });
}

/*if (message.content.toLowerCase().includes("hot".toLowerCase()) == true) {
  console.log("HOT")
  channel.send({
    files: ['./video/Hot.mp4']
  });
}*/

if (message.content.toLowerCase().includes("the sun is a deadly lazer".toLowerCase()) == true || message.content.toLowerCase().includes("the sun is a deadly laser".toLowerCase()) == true) {
  console.log("The sun is a deadly lazer!")
  channel.send({
    files: ['./video/Blanket.mp4']
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
  var embed = {
      "embed": {
        "description": "Here is the sauce in which you desire: " + num,
        "url": "https://discordapp.com",
        "color": 15541587,
        "author": {
          "name": "The Devil",
          "url": "https://youtu.be/dQw4w9WgXcQ",
          "icon_url": "https://i.imgur.com/uLAimaY_d.webp?maxwidth=728&fidelity=grand"
        }
      }
    }
    message.channel.send(embed);
}

if (message.content.toLowerCase().includes("heresy".toLowerCase()) == true) {
  var num = Math.floor(Math.random() * fileManager.getAllDirFiles("./images/heresy").length)
  var path = "./images/heresy/"
  console.log("HERESY!!")
  if ((message.content.substring(0, 7) == "heresy_".toLowerCase()) && (parseInt(message.content.substring(7))) != NaN) {
      console.log("Trying to find heresy_" + parseInt(message.content.substring(7)))
      var num = parseInt(message.content.substring(7))
      var fileName = "heresy_"
      channel.send(fileManager.sendImage(num, path, fileName, message, masterColor))
  } else {
    var num = Math.floor(Math.random() * fileManager.getAllDirFiles("./images/heresy").length)
    console.log(fileManager.getAllDirFiles("./images/heresy").length)
    var fileName = "heresy_"
    channel.send(fileManager.sendImage(num, path, fileName, message, masterColor))
  }
}

if (message.content.toLowerCase().includes("ravioli ravioli".toLowerCase()) == true) {
  console.log("Don't lewd the drangon loli!")
  var embed = new Discord.MessageEmbed()
    .attachFiles(['./images/ravioli.gif'])
    .setImage('attachment://ravioli.gif');
  channel.send(embed);
}

if (message.content.toLowerCase().includes("hentai".toLowerCase()) == true) {
  console.log("Hentai!")
  var embed = new Discord.MessageEmbed()
    .attachFiles(['./images/hentai.gif'])
    .setImage('attachment://hentai.gif');

  channel.send(embed);
}

if (message.content.toLowerCase().includes("hello there".toLowerCase()) == true) {
  console.log("Hello there!")
  var embed= new Discord.MessageEmbed()
      .attachFiles(['./images/generalkenobi.gif'])
      .setImage('attachment://generalkenobi.gif');

  channel.send(embed);
}

if (message.content.toLowerCase().includes("trap".toLowerCase()) == true) {
  console.log("It's a trap!")
  var embed = new Discord.MessageEmbed()
    .attachFiles(['./images/trap.gif'])
    .setImage('attachment://trap.gif');

  channel.send(embed);
}

if (message.content.substring(0, 1) == '!') {
  lastNum = commands.command(message, channel, lastNum)
}


    
});