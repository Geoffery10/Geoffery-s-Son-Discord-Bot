const Discord = require('discord.js');
const client = new Discord.Client();
var logger = require('winston');
var auth = require('./auth.json');
var fileManager = require('./fileManager.js');
var riskofrain2 = require('./riskofrain2.js');
var randomMod = require('./randomMod.js');
var members = require('./members.js');
var mcRCON = require('./mcRCON.js');
var emojis = require('./emojis.js');
var commands = require('./commands.js');
const fs = require('fs')
const fetch = require('node-fetch');
const { json } = require('express');
var https = require('https');
var birthdayLastDate = new Date(2019,3,31) 
const masterColor = 7871916
var lastUserID = "735550470675759106" 
var IP = 'ERROR'
// Require the module in your project

// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = 'debug';
// Initialize Discord Bot

client.once('ready', () => {
  IP = 'ERROR'
    console.log("Getting IP...")
    url = "https://api.ipify.org/?format=json";
    https.get(url, res => {
            res.setEncoding("utf8");
                let body = "";
                res.on("data", data => {
                    body += data;
                });
                res.on("end", () => {
                    body = JSON.parse(body);
                    let ip = body.ip;
                    IP = body.ip
                });
        });
  let rawdata = fs.readFileSync('status.json');
  let status = JSON.parse(rawdata);
  client.user.setPresence(status);
  client.user.setPresence(status)

  console.log('Geoffery\'s Son is Ready!');
});

client.login(auth.token);


client.on('message', message => {
  let rawdata = fs.readFileSync('status.json');
  let status = JSON.parse(rawdata);
  client.user.setPresence(status);
  if (message.author.id == "779431244222955520"){
    if (message.content.includes(" » ") == true) {
      message.content = message.content.substring(message.content.indexOf("»") + 2);
      console.log(`Updated message: ${message.content}`);
    }
  }
  member = members.checkMember(message.author.username, message.author.id)
  var channel = message.channel;
  var guild = message.guild;
  var simplify = false;
  console.log(`${message.author.username} sent: ${message} on Channel: ${channel}`)

  if (channel == "779436910841954354") {
    simplify = true;
  }
  
  var score = 1;

  var rip_regex = /(^.*\srip$)|(^rip\s.*)|(^rip$)|(^.*\srip\s.*$)/i;
  var ripdot_regex = /(^.*\sr.i.p$)|(^r.i.p\s.*)|(^r.i.p$)|(^.*\sr.i.p\s.*$)/i;
  var ripdotfinal_regex = /(^.*\sr.i.p.$)|(^r.i.p.\s.*)|(^r.i.p.$)|(^.*\sr.i.p.\s.*$)/i;
  if(rip_regex.test(message.content.toLowerCase()) || ripdot_regex.test(message.content.toLowerCase()) || ripdotfinal_regex.test(message.content.toLowerCase())) {
    message.react("372950049665318925")
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
      score = score + 1;
    }
  }

  var owo_regex = /(^.*\sowo$)|(^owo\s.*)|(^owo$)|(^.*\sowo\s.*$)/i;
  var uwu_regex = /(^.*\suwu$)|(^uwu\s.*)|(^uwu$)|(^.*\suwu\s.*$)/i;
  if (owo_regex.test(message.content.toLowerCase()) || uwu_regex.test(message.content.toLowerCase())) {
    console.log("OwO")
    var embed= new Discord.MessageEmbed()
      .attachFiles(['./images/owo.png'])
      .setImage('attachment://owo.png');

    channel.send(embed);
    score = score + 1;
  }

  if (message.content.toLowerCase().includes("is it possible to learn this power".toLowerCase()) == true) {
    console.log("Is it possible to learn this power?")
    channel.send({
      files: ['./video/Palpatine_00.mp4']
    });
    score = score + 1;
  }

  if (message.content.toLowerCase().includes("the sun is a deadly lazer".toLowerCase()) == true || message.content.toLowerCase().includes("the sun is a deadly laser".toLowerCase()) == true) {
    console.log("The sun is a deadly lazer!")
    channel.send({
      files: ['./video/Blanket.mp4']
    });
    score = score + 1;
  }

  if (message.content.toLowerCase().includes("10th time".toLowerCase()) == true) {
    console.log("9th time")
    message.channel.send("9th time!");
    score = score + 1;
  }


  if (message.content.toLowerCase().includes("sauce".toLowerCase()) == true && !(message.author.id == "735550470675759106")) {
    var num = Math.floor(Math.random() * Math.floor(321861))
    console.log("Sauce: " + num)
    console.log("nhentai.net/g/" + num)
    if (simplify == true) {
      message.channel.send("Here is the sauce in which you desire: " + num);
    } else {
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
      score = score + 1;
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
    score = score + 1;
  }

  if (message.content.toLowerCase().includes("ravioli ravioli".toLowerCase()) == true) {
    console.log("Don't lewd the drangon loli!")
    var embed = new Discord.MessageEmbed()
      .attachFiles(['./images/ravioli.gif'])
      .setImage('attachment://ravioli.gif');
    channel.send(embed);
    score = score + 1;
  }

  if (message.content.toLowerCase().includes("hentai".toLowerCase()) == true) {
    console.log("Hentai!")
    var embed = new Discord.MessageEmbed()
      .attachFiles(['./images/hentai.gif'])
      .setImage('attachment://hentai.gif');

    channel.send(embed);
    score = score + 1;
  }

  if (message.content.toLowerCase().includes("hello there".toLowerCase()) == true) {
    console.log("Hello there!")
    var embed= new Discord.MessageEmbed()
        .attachFiles(['./images/generalkenobi.gif'])
        .setImage('attachment://generalkenobi.gif');

    channel.send(embed);
    score = score + 1;
  }

  var trap_regex = /(^.*\strap$)|(^trap\s.*)|(^trap$)|(^.*\strap\s.*$)/i;
  if (trap_regex.test(message.content.toLowerCase())) {
    console.log("It's a trap!")
    var embed = new Discord.MessageEmbed()
      .attachFiles(['./images/trap.gif'])
      .setImage('attachment://trap.gif');

    channel.send(embed);
    score = score + 1;
  }

  if (message.content.substring(0, 1) == '!') {
    score = commands.command(Discord, client, message, channel, score, IP, simplify)
  }

  if (message.author.id == lastUserID) {
    score = 0;
  } else {
    lastUserID = message.author.id
  }
  member = members.addScore(message.author.username, message.author.id, score, member)
    
});