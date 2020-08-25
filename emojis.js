
const getEmojiID = function (client, message, id) {
    return message.guild.emojis.cache.find(emoji => emoji.name === id);
}


module.exports.getEmojiID = getEmojiID;