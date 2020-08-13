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