channel.send();

var embed = {
    "image": {
        "url": url
        }
    };
channel.send({ embed });

var embed = new Discord.MessageEmbed()
	.setTitle('Some title')
	.attachFiles(['./images/discordjs.png'])
	.setImage('attachment://discordjs.png');

channel.send(embed);