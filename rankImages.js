const getImage = function(score) {
    var image = './images/owo.png'
    if (score < 100) {
        './images/rank/1.png'
    }
    return image;
}

module.exports.getImage = getImage;