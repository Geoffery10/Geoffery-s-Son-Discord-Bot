const getImage = function(score) {
    var image = './images/owo.png'
    if (score >= 1) {
        image = './images/rank/1.png'
    }
    if (score >= 35) {
        image = './images/rank/35.png'
    }
    if (score == 69) {
        image = './images/rank/69.png'
    }
    if (score >= 100) {
        image = './images/rank/100.png'
    }
    if (score >= 700) {
        image = './images/rank/700.png'
    }
    if (score > 9000) {
        image = './images/rank/9000.png'
    }
    return image;
}

module.exports.getImage = getImage;