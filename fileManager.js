const Discord = require('discord.js');
const client = new Discord.Client();
const fs = require('fs')

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

const sendImage = function (num, path, fileName, message, lastNum, color) {
  var title = "" + fileName + num;
    lastNum = num;
    if (num <= 9) {
      fileName = fileName + "0" + num;
    } else {
      fileName = fileName + num;
    }
    if(fs.existsSync(path + fileName + ".gif")){
      fileName = fileName + ".gif"
      console.log(fileName)
      var embed = new Discord.MessageEmbed()
        .setTitle(title.toUpperCase())
        .setColor(color)
        .attachFiles([path + fileName])
        .setImage('attachment://' + fileName);
        return embed
    } else if (fs.existsSync(path + fileName + ".png")) {
      fileName = fileName + ".png"
      console.log(fileName)
      var embed = new Discord.MessageEmbed()
        .setTitle(title.toUpperCase())
        .setColor(color)
        .attachFiles([path + fileName])
        .setImage('attachment://' + fileName);
        return embed
    } else if (fs.existsSync(path + fileName + ".jpg")) {
        fileName = fileName + ".jpg"
        console.log(fileName)
        var embed = new Discord.MessageEmbed()
        .setTitle(title.toUpperCase())
        .setColor(color)
        .attachFiles([path + fileName])
        .setImage('attachment://' + fileName);
        return embed
    } else if (fs.existsSync(path + fileName + ".mp4")) {
        fileName = fileName + ".mp4"
        console.log(fileName)
        var embed = {files: [(path + fileName)]}
        return embed
    } else if (fs.existsSync(path + fileName + ".mov")) {
      fileName = fileName + ".mov"
      console.log(fileName)
      var embed = {files: [(path + fileName)]}
        return embed
    } else {
      console.log("Error " + path + fileName + " not found...")
      message.channel.send("This ain't it chief. I couldn't find the gif.");
    }
  };

const getItem = function(folder) {
  console.log("Checking " + folder + " for items...")
  var num = Math.floor(Math.random() * getAllDirFiles(folder).length)
  var counter = 0
  var item
  fs.readdirSync(folder).forEach(file => {
    //console.log(file)
    //console.log("Counter (" + num + "): " + counter)
    if (counter == num) {
      item = file
      //console.log(item + " has been saved...")
    }
    counter++
    console.log("Item to return: " + item)
    return item;
  });
}

module.exports.getAllDirFiles = getAllDirFiles;  
module.exports.sendImage = sendImage;
module.exports.getItem = getItem;