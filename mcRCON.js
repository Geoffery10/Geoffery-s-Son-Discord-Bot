const Rcon = require('modern-rcon');
var options = {
    tcp: true,       // false for UDP, true for TCP (default true)
    challenge: true  // true to use the challenge protocol (default true)
};
var host = '192.168.0.125'
var port = 25544
var password = 'FoodFood'


const sendCommand = async function (cmd, channel) {
    const rcon = new Rcon(host, port, password);
    var message = "Server not responding..."
    rcon.connect().then(() => {
    return rcon.send(cmd); // That's a command for Minecraft
    }).then(res => {
        console.log("Connected to MC Server.");
        console.log("Sent command: " + cmd)
        console.log(res);
        message = res + ""
        if (res === "") {
            console.log("Error: res is empty.");
            message = "Server not responding..."
        }
        var embed = {
            "embed": {
                "description": "``` " + message + " ```",
                "color": 4289797,
                "thumbnail": {
                "url": "https://media.forgecdn.net/avatars/136/944/636511227443004307.png"
                },
                "author": {
                "name": "RLCraft Server",
                "url": "https://www.curseforge.com/minecraft/modpacks/rlcraft",
                "icon_url": "https://i.pinimg.com/originals/85/78/bf/8578bfd439ef6ee41e103ae82b561986.png"
                }
            }
        }

        channel.send(embed);
    }).then(() => {
        console.log("Disconnecting from MC Server...");
        return rcon.disconnect();
    });
}

module.exports.sendCommand = sendCommand;