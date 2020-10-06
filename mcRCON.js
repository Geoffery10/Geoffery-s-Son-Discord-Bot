const Rcon = require('modern-rcon');
const https = require("http");
var options = {
    tcp: true,       // false for UDP, true for TCP (default true)
    challenge: true  // true to use the challenge protocol (default true)
};
var host = '192.168.0.125'
var port = 25544
var password = 'FoodFood'


const LookServerFL = async function (channel) {
    //Info at: https://sv443.net/jokeapi/v2/
    url = "http://192.168.0.125:8000/"

    https.get(url, res => {
        playerList = ""
        res.setEncoding("utf8");
        let body = "";
        res.on("data", data => {
        body += data;
        });
        res.on("end", () => {
        body = JSON.parse(body);
        console.log(body);
        if (body.players == "") {
            playerList = "None"
        } else {
            if (body.players.length == 1) {
                playerList += body.players[0].name
            } else {
                for (index = 0; index < body.players.length; index++) { 
                    if (index == (body.players.length - 1)) {
                        playerList += "and " + body.players[index].name
                    } else {
                        playerList += body.players[index].name + ", "
                    }
                } 
            }
        }

        body.bukkitVersion = body.bukkitVersion.substring(0, body.bukkitVersion.indexOf('-'))
        var embed = {
            "embed": {
                "description": "Info: " + body.motd
                + "\nOnline Players: " + playerList
                + "\nIP Zerotier: 172.25.44.20:" + body.port
                + "\nWeb Map Zerotier: [172.25.44.20:25568](172.25.44.20:25568)"
                + "\nVersion: " + body.bukkitVersion,
                "color": 4289797,
                "thumbnail": {
                "url": "https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/minecraft-icon.png"
                },
                "author": {
                "name": "Minecraft Server",
                "url": "https://www.minecraft.net/en-us",
                "icon_url": "https://i.pinimg.com/originals/85/78/bf/8578bfd439ef6ee41e103ae82b561986.png"
                }
            }
        }

        channel.send(embed);
        });
    });
}

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
module.exports.LookServerFL = LookServerFL;