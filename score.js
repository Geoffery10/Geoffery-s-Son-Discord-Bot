const addScore = function (client, message, id) {
    member = members.checkMember(message.author.username, message.author.id)
    return message.guild.emojis.cache.find(emoji => emoji.name === id);
}

module.exports.addScore = addScore;