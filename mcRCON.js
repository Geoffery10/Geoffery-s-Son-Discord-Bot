const Rcon = require('modern-rcon');
const http = require('http');
const https = require('https');
var options = {
    tcp: true,       // false for UDP, true for TCP (default true)
    challenge: true  // true to use the challenge protocol (default true)
};
var host = '50.80.62.13'
var port = 25575
var password = 'asgahdsghdf'

const LookServerFL = async function (channel, ip) {
    host = ip;
    url = "http://192.168.0.167:8000"
    http.get(url, res => {
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
                + "\nIP: "+ ip + ":" + body.port
                + "\nWeb Map: [http://" + ip + ":25568/](http://" + ip + ":25568/)"
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
    localhost = '192.168.0.167'
    const rcon = new Rcon(localhost, port, password);
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
                "url": "https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/340?cb=20190903234415"
                },
                "author": {
                "name": "RLCraft Server",
                "url": "https://www.minecraft.net/",
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