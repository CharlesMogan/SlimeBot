# slimebot.py
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
from imagetest import slime_image, valid_image_url
from slimebot2.slimewords import remove_word
from slimewords import get_slime_list,get_black_list,write_words, blacklist_words

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ADMIN_ID = os.getenv('ADMIN_ID')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True
intents.guild_messages = True
intents.dm_messages = True
intents.members = True
#intents = discord.Intents.all()
bot = commands.Bot(command_prefix='sb ', intents=intents)







async def send_image(channel, slimed_image, slime_message="Sure thing"):
    try:
        await channel.send(slime_message, file=discord.File(slimed_image))
    except discord.errors.HTTPException as e:  # mostly concerned about 413 payload too large
        await channel.send("Sorry,  the finished image is too large. If only bots could have"
                           " Nitro.", file=discord.File("./images/src/SlimeSorry.png"))


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break


    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    slime_word_dict = get_slime_list()

    if message.author == bot.user:  # bot should not command itself
        return

    if message.content.split(' ')[0] == "sb":  # does nothing if the user enters a slimebot command
        return

    if isinstance(message.channel, discord.DMChannel):
        return

    word_list = message.content.split(' ')
    for word in word_list:
        if word in slime_word_dict:
            #testvar3 = bot.fetch_user(testvar)
            original_submitter = bot.get_user(slime_word_dict[word]["id"]).mention
            submission_time = time.ctime(slime_word_dict[word]["time"])
            response_message = (f"{message.author.mention} said the slimeword: {word}!\n"
                                f" it was added by {original_submitter}"
                                f" on {submission_time}")
            remove_word(word)
            slime_image(f"{message.author.avatar.url}")
            await send_image(message.channel, "./images/result/result.webp",response_message)



@bot.command(name='addwords', help='dm this bot a list of words in the format: "addwords word1 word2 word3"')
async def add_words(ctx):
    slime_word_dict = get_slime_list()
    print(f'adding word')
    if isinstance(ctx.channel, discord.DMChannel):
        word_list = ctx.message.content.split(' ')
        del word_list[0:2]  # removes the command words
        write_words(word_list, ctx.author.id)   #fixme why does it want this awaited???
        await ctx.send(f" You added the following words: {word_list}")
    else:
        await ctx.send(f"dm this bot a list of words in the format: addwords word1  word2  word3")


@bot.command(name='blacklistwords', help='dm this bot a list of words to blacklist, this words will be removed from '
                                         'the slime list pool and not addable again: "blacklistwords word1, word2, '
                                         'word3"')
async def blacklist_words_command(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        word_list = ctx.message.content.split(' ')
        del word_list[0:2]  # removes the command words
        blacklist_words(word_list,ctx.author.id)
        await ctx.send(f" You added the following words to the blacklist: {word_list}")
    else:
        await ctx.send(f"dm this bot a list of words in the format: blacklistwords word1 word2 word3")


@bot.command(name='slime', help='send me an image or a link to an image and I will silime it, to get slimed say '
                                '\"slime me\"')
async def slime_this(ctx, *args):
    print(f'sliming')
    if args:
        if args[0] == "me":
            slimed_image = slime_image(f"{ctx.author.avatar.url}")
            await send_image(ctx.channel, slimed_image)
            return

    for role in ctx.message.role_mentions:
        for user in role.members:
            slimed_image = slime_image(f"{user.avatar.url}")
            await send_image(ctx.channel, slimed_image)

    for user in ctx.message.mentions:
        slimed_image = slime_image(f"{user.avatar.url}")
        await send_image(ctx.channel, slimed_image)

    for arg in args:
        arg = str(arg).strip('<>')
        if valid_image_url(arg):
            slimed_image = slime_image(arg)
            await send_image(ctx.channel, slimed_image)

    for attachment in ctx.message.attachments:
        attachment_url = attachment.url
        print(attachment_url)
        if valid_image_url(attachment_url):
            slimed_image = slime_image(attachment_url)
            await send_image(ctx.channel, slimed_image)


@bot.command(name='fix', help='If slime bot is not working the way you would expect, send the dev a description '
                              'of the problem so that they can fix it, please include as much relevant'
                              'information as you can. You may be contacted for more information by the dev.'
                              ' Note that slimebot is running on an old computer, and may be'
                              'very slow at times. This is in itself not considered a reportable problem')
async def fix_me(ctx, *args):
    if args:
        author = ctx.message.author.mention
        message_to_admin = f"{author} has reported the following problem: {ctx.message.content}"
        try:
            admin_id_int = int(ADMIN_ID)
        except ValueError:
            await ctx.channel.send("If you see this message it means even the error reporting is broken!!")
        admin = bot.get_user(admin_id_int)
        await admin.send(message_to_admin)
        attachment_message = "the following attachments were included: "
        for attachment in ctx.message.attachments:
            await admin.send(f"{attachment_message}{attachment.url}")
        return
    await ctx.channel.send("You need to add a description of the problem!")


bot.run(TOKEN)

# add procedurly generated slime
# add progressive sliming
# add animated slimeq
# add animated slime to gifs
