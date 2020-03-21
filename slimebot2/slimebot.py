# slimebot.py
import os
import time
import json
import pickle
import discord
from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter

from imagetest import slime_image, get_file_name, valid_image_url

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='sb ')

slime_word_dict = {}
black_list_dict = {}


def write_slime_dict_to_file():
    print(f"this method was called")
    with open('slimelist.json', 'w') as slime_list_file_descriptor:
        global slime_word_dict
        json.dump(slime_word_dict, slime_list_file_descriptor)


def write_blacklist_dict_to_file():
    with open('blacklist.json', 'w') as black_list_file_descriptor:
        global black_list_dict
        json.dump(black_list_dict, black_list_file_descriptor)


class SubmissionInformation:

    def __init__(self, submitter, submition_time):
        self.submitter = submitter
        self.time = submition_time


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    with open('slimelist.json') as slime_list_file_descriptor, open(
            'blacklist.json') as black_list_file_descriptor:
        global slime_word_dict
        global black_list_dict
        slime_word_dict = json.load(slime_list_file_descriptor)
        black_list_dict = json.load(black_list_file_descriptor)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    if message.content.split(' ')[0] == "sb":  # does nothing if the user enters a slimebot command
        return

    if isinstance(message.channel, discord.DMChannel):
        print(f"I recieved a direct message!")
        # await message.author.dm_channel.send()
        return

    changed_list = False
    word_list = message.content.split(' ')
    for word in word_list:
        if word in slime_word_dict:
            changed_list = True
            original_submitter = bot.get_user(slime_word_dict[word]["id"]).mention
            submission_time = time.ctime(slime_word_dict[word]["time"])
            response_message = (f"{message.author.mention} said the slimeword: {word}!\n"
                                f" it was added by {original_submitter}"
                                f" on {submission_time}")
            slime_word_dict.__delitem__(word)
            black_list_dict[word] = time.time()
            slime_image(f"{message.author.avatar_url}")

            await message.channel.send(response_message, file=discord.File("./images/result.png"))
    if changed_list:
        write_slime_dict_to_file()


@bot.command(name='addwords', help='dm this bot a list of words in the format: "addwords word1 word2 word3"')
async def add_words(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        word_list = ctx.message.content.split(' ')
        del word_list[0:2]  # removes the command words
        for word in word_list:
            if word not in slime_word_dict and word not in black_list_dict:
                submission_info = {"id": ctx.author.id, "time": time.time()}
                slime_word_dict[word] = submission_info
            else:
                word_list.remove(word)
        await ctx.send(f" You added the following words: {word_list}")
        write_blacklist_dict_to_file()
    else:
        await ctx.send(f"dm this bot a list of words in the format: addwords word1  word2  word3")


@bot.command(name='blacklistwords', help='dm this bot a list of words to blacklist, this words will be removed from '
                                         'the slime list pool and not addable again: "blacklistwords word1, word2, '
                                         'word3"')
async def blacklist_words(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        word_list = ctx.message.content.split(' ')
        del word_list[0:2]  # removes the command words
        for word in word_list:
            if word not in black_list_dict:
                submission_info = {"id": ctx.author.id, "time": time.time()}
                black_list_dict[word] = submission_info
                if word in slime_word_dict:
                    slime_word_dict.__delitem__(word)
            else:
                word_list.remove(word)
        await ctx.send(f" You added the following words to the blacklist: {word_list}")
        write_slime_dict_to_file()
    else:
        await ctx.send(f"dm this bot a list of words in the format: blacklistwords word1 word2 word3")


@bot.command(name='slime', help='send me an image or a link to an image and I will silime it, to get slimed say '
                                '\"slime me\"')
async def add_words(ctx, *args):
    if args:
        if args[0] == "me":
            slimed_image = slime_image(f"{ctx.author.avatar_url}")
            await ctx.channel.send("Sure thing", file=discord.File(slimed_image))
            return

    for role in ctx.message.role_mentions:
        for user in role.members:
            slimed_image = slime_image(f"{user.avatar_url}")
            await ctx.channel.send("Sure thing", file=discord.File(slimed_image))

    for user in ctx.message.mentions:
        slimed_image = slime_image(f"{user.avatar_url}")
        await ctx.channel.send("Sure thing", file=discord.File(slimed_image))

    for arg in args:
        arg = str(arg).strip('<>')
        if valid_image_url(arg):
            slimed_image = slime_image(arg)
            await ctx.channel.send("Sure thing", file=discord.File(slimed_image))

    for attachment in ctx.message.attachments:
        attachment_url = attachment.url
        print(attachment_url)
        if valid_image_url(attachment_url):
            slimed_image = slime_image(attachment_url)
            await ctx.channel.send("Sure thing", file=discord.File(slimed_image))


bot.run(TOKEN)

# fails when image 2 big
# add to lowercase
# add procedurly generated slime
# add progressive sliming
# add animated slimeq
# add animated slime to gifs
