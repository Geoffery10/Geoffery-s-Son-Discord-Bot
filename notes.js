message.channel.send();

var embed = {
    "image": {
        "url": url
    }
    };
    message.channel.send({ embed });
});

var embed= new Discord.MessageEmbed()
	.setTitle('Some title')
	.attachFiles(['../assets/discordjs.png'])
	.setImage('attachment://discordjs.png');

channel.send(embed);