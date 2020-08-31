import { fileURLToPath } from "url";
import { Certificate } from "crypto";
import { resolve } from "dns";

const execSync = require('child_process').execSync;
const https = require('https');
const fs = require('fs');
const Discord = require('discord.js');
const gm = require('gm');
const client = new Discord.Client();
var slimeWordMap:Map<string,submitter> = new Map();
var blacklistWordMap:Map<string,number> = new Map();
var d = new Date();
var n = d.getTime();


class  submitter{
    submitterName:any;
    timeOfSubmition:number; 
    constructor(submitterName: any,time: number) {
        this.submitterName = submitterName;
        this.timeOfSubmition = time;
    }

}

client.once('ready', () => {
    if(fs.existsSync('wordList.json')){
        let raw:string = fs.readFileSync('wordList.json');
        slimeWordMap = new Map(JSON.parse(raw));
    }
    if(fs.existsSync('blackList.json')){
        let raw:string = fs.readFileSync('blackList.json');
        blacklistWordMap = new Map(JSON.parse(raw));
    }
    
	console.log('Ready!');
});

client.login('');

client.on('message', async message => {
    if(message.author.bot){
        return;
    }
    var chatMessage:string[] = message.content.split(/ +/);
    //adding new words
    if(message.channel.type == "dm"){
        
        var args:string[] = chatMessage.slice(1,chatMessage.length);
        const command:string = chatMessage[0];
        console.log(`args ${args}`);
        console.log(`command ${command}`);
        if (command.toLowerCase() == 'addwords'){
            if (!args.length) {
                message.channel.send(`You didn't provide any words to add, ${message.author}!`);
            }else{
                args.forEach(element => {
                    if(!blacklistWordMap.has(element)){
                        let mysubmitter = new submitter(message.author.id, d.getTime());
                           
                        slimeWordMap.set(element,mysubmitter);
                    }else{
                        message.channel.send(`${element} is a blacklisted word and will not be added`);
                        args.splice(args.indexOf(element),1);
                    }
                });
                fs.writeFileSync('wordList.json', JSON.stringify([...slimeWordMap]));
                message.channel.send(`added the following words to the list ${args}`);
            }
        }else if (command.toLowerCase() == 'blacklistwords'){
            if (!args.length) {
                message.channel.send(`You didn't provide any words to blacklist:, ${message.author}!`);
            }else{
                args.forEach(element => {
                    blacklistWordMap.set(element,1);
                    if(slimeWordMap.has(element)){
                        slimeWordMap.delete(element);
                        fs.writeFileSync('wordList.json', JSON.stringify([...slimeWordMap]));
                    }
    
                });
                fs.writeFileSync('blackList.json', JSON.stringify([...blacklistWordMap]));
                message.channel.send(`added the following words to the blacklist ${args}`);
                
            }
        }else{
            message.channel.send(`dm this bot a list of words in the format: addwords word1, word2, word3`);
        }
    }



    if(message.channel.type != "dm"){
        if(chatMessage[0].toLowerCase() == "slimebot"){
            var args:string[] = chatMessage.slice(2,chatMessage.length);
            const command:string = chatMessage[1];
            if(command == undefined){
                return;
            }
            if(command.toLowerCase() == "help"){
                message.channel.send("slimebot is a bot what for having a good and joyous time with friends. \nits primary function is to \"slime\" the person who has sent a message containing a trigger word.\n Trigger words are added by dming this bot a list of words in the format \"addwords word1, word2, word3\"\n Words are removed from the trigger list once used");
            }
        }else{
            const matches = chatMessage.filter(word => {
                return slimeWordMap.has(word);
            });
            if(matches){
                var avatar:string = message.author.displayAvatarURL;
                console.log("statement before await");
                console.log(`the matches are: ${matches}`);
                //saveImage(avatar);









                async function makeSynchronousRequest() {
                    try {
                        let http_promise = getPromise(avatar);
                        let response_body = await http_promise;
                        //fs.writeFileSync('./images/taco.png', response_body);
                        //console.log(response_body);
                    }
                    catch (error) {
                        // Promise rejected
                        console.log(error);
                    }
                }
                console.log(1);
                // anonymous async function to execute some code synchronously after http request
                (async function () {
                    // wait to http request to finish
                    console.log(1.5);
                    await makeSynchronousRequest();
                    // below code will be executed after http request is finished
                    console.log("after async request returned");


                
                matches.forEach(element => {
                    console.log("entered for loop");
                    var wordmaker = client.users.get(slimeWordMap.get(element)?.submitterName);
                    message.channel.send(`${message.author} said the slimeword: ${element}!\n it was added by ${wordmaker} `,{file: "./images/result.png"});
                    slimeWordMap.delete(element);
                    fs.writeFileSync('wordList.json', JSON.stringify([...slimeWordMap]));
                });
                //fs.unlinkSync("./images/taco.png");
                //fs.unlinkSync("./images/slime1.png");
                //fs.unlinkSync("./images/result.png");
                })();


                
                //compositeImages();

               
            }
        }
    }
    //checking recieved words

});

function mapToJson(map) {
    return JSON.stringify([...map]);
  }
function jsonToMap(jsonStr) {
    return new Map(JSON.parse(jsonStr));
  }

/*function  saveImage(URL:string){
    //var image = fs.createWriteStream("./images/taco.png");
    const request = https.get(URL,  function(response) {
        //response.pipe(image);
        //fs.writeFileSync('./images/taco.png', response);
        response.on('end', function(){
            getsize();
        })
    });
}*/



// function returns a Promise
function getPromise(URL:string) {
	return new Promise((resolve, reject) => {
		https.get(URL, (response) => {
			let chunks_of_data : Uint8Array[] = [];

			response.on('data', (fragments) => {
				chunks_of_data.push(fragments);
			});

			response.on('end', () => {
                let response_body = Buffer.concat(chunks_of_data);
                fs.writeFileSync('./images/taco.png', response_body);
                console.log("before getsize()");
                getsize();
                console.log("after getsize()");
				resolve(response_body);
			});

			response.on('error', (error) => {
				reject(error);
			});
		});
	});
}





function getsize() {
    gm("./images/taco.png").size(function (err, size) {
        if (!err) {
            console.log('width = ' + size.width);
            console.log('height = ' + size.height);
            //execSync(`inkscape -z -e ./images/slime1.png -w ${size.width} -h ${size.height} ./images/slime1.svg`);
            //execSync(`gm composite ./images/slime1.png ./images/taco.png ./images/result.png`);
            execSync(`./maketheimage.sh ${size.width} ${size.height}`);
            //while(!fs.existsSync("./images/result.png")){
            //    console.log("the fucking file doesn't exist yet");
            //}

        }else{
            console.log("something went wrong");
            console.log(err);
        }
    });
}


// add word blacklist
// add help statements
// prevent bot from triggering based on itself
// say who added the word and when  when it is 

//identify  test.png
//inkscape -z -e slime1.png -w 512 -h 512 slime1.svg

//convert test.png slime1.png    -composite ./slimefirst.png
