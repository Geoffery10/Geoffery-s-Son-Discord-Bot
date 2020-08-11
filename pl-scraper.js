// pl-scraper.js

var Scraper = require('image-scraper');
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

var makeScrape = function makeScrape(url, filePath, name) {
    var scraper = new Scraper(url);
    scraper.scrape(function(image) { 
        image.name = name;
        image.saveTo = filePath;
        image.save();
    });
}
 

module.exports.makeScrape = makeScrape;