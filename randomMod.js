commands = ['!anime', '!hentai', '!owo', '!sauce', '!heresy', 'Ravioli ravioli', 'Hello there!', 'trap', '!ping', '!r2loadout', '!wtf', '!roll_d20', '!nani', '!fact', '!joke', 
'!insultme', '!yesorno', '!selfie', '!cat', '!thispersondoesnotexist', '!waifu', '!lastNum', '!who is your mother'];

var randomCommands = function() {
    var num = Math.floor(Math.random() * commands.length);
    return commands[num];
}

module.exports.randomCommands = randomCommands;