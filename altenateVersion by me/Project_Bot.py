import discord, json, os
from discord.ext import commands
import quizchoice
import random as rd
bot = commands.Bot(command_prefix='x', help_command=None)
token = ""             #insert bot token
os.chdir(r"C:\Users\com\Desktop\Python\Discord_Bot")  #change dir where users.json and bot.py is
pointperquiz = 10
timeperquiz = 15
def update_data(users, user):
    if (str(user.id) not in users) and bot.user.id != user.id:
        users[str(user.id)] = {}
        users[str(user.id)]["point"] = 0
        users[str(user.id)]["level"] = 1
        users[str(user.id)]["correct"] = 0
        users[str(user.id)]["incorrect"] = 0
        users[str(user.id)]["attempt"] = 0
        users[str(user.id)]["ratio"] = "None"
async def add_point(users, user, point):
    users[str(user.id)]["point"] += point

async def add_correct(users, user):
    users[str(user.id)]["correct"] += 1
    users[str(user.id)]["attempt"] += 1
    users[str(user.id)]["ratio"] = round(users[str(user.id)]["correct"]/users[str(user.id)]["attempt"], 2)

async def add_incorrect(users, user):
    users[str(user.id)]["incorrect"] += 1
    users[str(user.id)]["attempt"] += 1
    users[str(user.id)]["ratio"] = round(users[str(user.id)]["correct"]/users[str(user.id)]["attempt"], 2)
    
async def level_up(users, user, channel):
    point = users[str(user.id)]["point"]
    lvl_start = users[str(user.id)]["level"]
    lvl_end = int(point ** (1/4))
    if lvl_start < lvl_end:
        await channel.send(f"{user.mention} has leveled up to level {lvl_end}")
        users[str(user.id)]["level"] = lvl_end

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('xhelp'))
@bot.event
async def on_message(message):
    print(message.content)
    await bot.process_commands(message)

@bot.command()
async def quiz(ctx, number=None):
    if number == None:
        number = str(rd.randint(1, len(quizchoice.allquiz)))
    await ctx.send(f'OK {ctx.author.mention}')
    embed=discord.Embed(title=f"Question {number}", color=0xeb0000)
    embed.set_thumbnail(url=f"{bot.user.avatar_url}")
    newstr = ""
    num = 1
    for x in quizchoice.allquiz[number]:
        if len(x) == 2:
            newstr += f"{quizchoice.emojinum[num]} {x[0]}\n\n"  
            num += 1
    embed.add_field(name=quizchoice.allquiz[number][0], value=newstr, inline=True)
    embed.set_footer(text=f"Player: {ctx.author}\nPoints: {pointperquiz}\nTime: {timeperquiz} seconds", icon_url=f"{ctx.author.avatar_url}")
    question = await ctx.send(embed=embed)
    num = 1
    for i in quizchoice.allquiz[number]:
        if len(i) == 2:
            await question.add_reaction(quizchoice.emojinum[num])
            num += 1
    def check(reaction, user):
        if user == ctx.author and reaction.message.id == question.id:
            if quizchoice.allquiz[number][quizchoice.emojinum.index(str(reaction.emoji))][1]:
                return True
            raise ValueError
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=timeperquiz, check=check)
    except ValueError:
        with open("users.json", "r") as fi:
            users = json.load(fi)
        update_data(users, ctx.author)
        await ctx.channel.send(":x: ตอบผิดครับ")
        await add_incorrect(users, ctx.author)
        with open("users.json", "w") as fi:
            json.dump(users, fi)
    except:
        await ctx.channel.send("หมดเวลาครับ")
    else:
        with open("users.json", "r") as fi:
            users = json.load(fi)
        update_data(users, ctx.author)
        await ctx.channel.send(":o: ตอบถูกครับ")
        await add_point(users, ctx.author, pointperquiz)
        await add_correct(users, ctx.author)
        await level_up(users, ctx.author, ctx.channel)
        with open("users.json", "w") as fi:
            json.dump(users, fi)
@bot.command()
async def stats(ctx):
    with open("users.json", "r") as fi:
        users = json.load(fi)
    update_data(users, ctx.author)
    embed=discord.Embed(title=f"{ctx.author.name}'s stats", color=0xeb0000)
    embed.set_author(name=f"{bot.user.name}", icon_url=f"{bot.user.avatar_url}")
    embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
    for key, i in users[str(ctx.author.id)].items():
        embed.add_field(name=key, value=i, inline=True)
    await ctx.send(embed=embed)
@bot.command()
async def join(ctx):
    connected = ctx.author.voice
    if connected:
        await connected.channel.connect()
    else:
        await ctx.channel.send("คุณไม่ได้เชื่อมต่อ")

@bot.command()
async def leave(ctx):
    voiu = ctx.message.guild.voice_client
    await voiu.disconnect()


@bot.command()#อันนี้ คำสั่ง help
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.set_author(name='Help?')
    embed.add_field(name='?start', value='OK', inline=False)
    await author.send(embed=embed)
bot.run(token)