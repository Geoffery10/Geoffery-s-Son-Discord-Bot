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

module.exports.getAllDirFiles = getAllDirFiles;  
module.exports.sendImage = sendImage;