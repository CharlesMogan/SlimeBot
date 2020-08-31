const Discord = require('discord.js');
const client = new Discord.Client();
var sevrtword = "word";

client.once('ready', () => {
	console.log('Ready!');
});

client.login('NjU2NzM4MDM4NTc5NDYyMTQ0.Xf6WeQ.nRSD8Y05v2FGomOH_hB30ryq5Is');

client.on('message', message => {

    //adding new words
    if(message.channel.type == "dm"){


        if (!message.content.startsWith("addwords") || message.author.bot) return;
        const args = message.content.slice(prefix.length).split(/ +/);
        const command = args.shift().toLowerCase();
        if (!args.length) {
            return message.channel.send(`You didn't provide any words to add, ${message.author}!`);
        }


        console.log(message.content);
        if (message.content == "") {
            message.delete();
            // send back "Pong." to the channel the message was sent in
            message.channel.send('thank you for submiting a slime word, the new slime word is');
        }
    }



    //checking recieved words

});




