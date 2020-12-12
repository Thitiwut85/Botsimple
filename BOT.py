import discord, time, asyncio, os, json
import random as rd
import quiz_choice
import quiz_pic
from discord.ext import commands

bot = commands.Bot(command_prefix='?', help_command=None)
token = '' #ใส่token bot discord
os.chdir(r"D:\Quizbot")
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
async def on_ready() :
    print("? Started")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('?help'))
@bot.event
async def on_message(message) :
    await bot.process_commands(message)
@bot.command()
async def help(ctx):#คำสั่งแสดงคำสั่งต่างๆ
    embed=discord.Embed(title="Command", color=0xef8206)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/786169057953972224/786504574042243072/question.png")
    embed.add_field(name="`?help`", value="คำสั่งต่างๆ", inline=False)
    embed.add_field(name="`?quiz <ตัวเลข>`", value="เลือกข้อที่จะทำ", inline=True)
    embed.add_field(name="**ตัวเลข**", value="1-27", inline=True)
    embed.add_field(name="`?random`", value="สุ่ม quiz", inline=False)
    embed.add_field(name="`?pic <ตัวเลข>`", value="เลือกข้อที่จะทำแบบรูปภาพ", inline=True)
    embed.add_field(name="ตัวเลข", value="1-2", inline=True)
    embed.add_field(name="`?stats`", value="โชว์คะแนนรวม, เลเวล, จำนวนข้อถูก-ข้อผิด, จำนวนข้อที่ทำ, ความแม่นยำเฉลี่ย", inline=False)
    await ctx.send(embed=embed)

@bot.command()#คำสั่งเลือก quiz
async def quiz(ctx, number) :
    await ctx.send(f'OK {ctx.author.mention}')
    embed=discord.Embed(title=f"Question {number}", color=0xef8206)
    newstr = ""
    num = 1
    for x in quiz_choice.allquiz[number]:
        nums = quiz_choice.emojinum.get(num)
        if len(x) == 2:
            newstr += f"{nums} {x[0]}\n\n"
            num += 1
            print(nums)
    embed.add_field(name=quiz_choice.allquiz[number][0], value=newstr, inline=True)
    embed.set_footer(text=f"Player: {ctx.author}\nPoints: {pointperquiz}\nTime: {timeperquiz} seconds", icon_url=f"{ctx.author.avatar_url}")
    question = await ctx.send(embed=embed)
    await question.add_reaction("1️⃣")
    await question.add_reaction("2️⃣")
    await question.add_reaction("3️⃣")
    await question.add_reaction("4️⃣")
    def check(reaction, user):
        if user == ctx.author and reaction.message.id == question.id:
            if str(reaction.emoji) == (quiz_choice.allquiz[number][5]).get('True'):
                return True
            raise ValueError
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=timeperquiz, check=check)
    except ValueError:
        with open("users.json", "r") as fi:
            users = json.load(fi)
        update_data(users, ctx.author)
        await ctx.channel.send("<:x_:786493309785735219> ตอบผิด")
        await add_incorrect(users, ctx.author)
        with open("users.json", "w") as fi:
            json.dump(users, fi)
    except:
        await ctx.channel.send("⏰ หมดเวลา")
    else:
        with open("users.json", "r") as fi:
            users = json.load(fi)
        update_data(users, ctx.author)
        await ctx.channel.send(":white_check_mark: ตอบถูก")
        await add_point(users, ctx.author, pointperquiz)
        await add_correct(users, ctx.author)
        await level_up(users, ctx.author, ctx.channel)
        with open("users.json", "w") as fi:
            json.dump(users, fi)

@bot.command()
async def random(ctx):#คำสั่งสุ่ม quiz
    await ctx.send(f'OK {ctx.author.mention}')
    await ctx.send('**Random Question**')
    number = str(rd.randint(1, len(quiz_choice.allquiz)))
    print(number)
    embed=discord.Embed(title=f"Question {number}", color=0xef8206)
    newstr = ""
    num = 1
    for x in quiz_choice.allquiz[number]:
        nums = quiz_choice.emojinum.get(num)
        if len(x) == 2:
            newstr += f"{nums} {x[0]}\n\n"
            num += 1
            print(nums)
    embed.add_field(name=quiz_choice.allquiz[number][0], value=newstr, inline=True)
    embed.set_footer(text=f"Player: {ctx.author}\nPoints: {pointperquiz}\nTime: {timeperquiz} seconds", icon_url=f"{ctx.author.avatar_url}")
    question = await ctx.send(embed=embed)
    await question.add_reaction("1️⃣")
    await question.add_reaction("2️⃣")
    await question.add_reaction("3️⃣")
    await question.add_reaction("4️⃣")
    def check(reaction, user):
        if user == ctx.author and reaction.message.id == question.id:
            if str(reaction.emoji) == (quiz_choice.allquiz[number][5]).get('True'):
                return True
            raise ValueError
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
    except ValueError:
        with open("users.json", "r") as fi:
            users = json.load(fi)
        update_data(users, ctx.author)
        await ctx.channel.send("<:x_:786493309785735219> ตอบผิด")
        await add_incorrect(users, ctx.author)
        with open("users.json", "w") as fi:
            json.dump(users, fi)
    except:
        await ctx.channel.send("⏰ หมดเวลา")
    else:
        with open("users.json", "r") as fi:
            users = json.load(fi)
        update_data(users, ctx.author)
        await ctx.channel.send(":white_check_mark: ตอบถูก")
        await add_point(users, ctx.author, pointperquiz)
        await add_correct(users, ctx.author)
        await level_up(users, ctx.author, ctx.channel)
        with open("users.json", "w") as fi:
            json.dump(users, fi)

@bot.command()
async def pic(ctx, number):#คำสั่งเลือก quiz แบบรูปภาพ
    embed=discord.Embed(title=f"Question Picture {number}", color=0xef8206)
    embed.set_image(url=quiz_pic.allquiz[number][0])
    newstr = ""
    num = 1
    for x in quiz_pic.allquiz[number]:
        nums = quiz_pic.emojinum.get(num)
        if len(x) == 2:
            newstr += f"{nums} {x[0]}\n\n"
            num += 1
            print(nums)
    embed.add_field(name=quiz_pic.allquiz[number][1], value=newstr, inline=True)
    embed.set_footer(text=f"Player: {ctx.author}\nPoints: {pointperquiz}\nTime: {timeperquiz} seconds", icon_url=f"{ctx.author.avatar_url}")
    question = await ctx.send(embed=embed)
    await question.add_reaction("1️⃣")
    await question.add_reaction("2️⃣")
    await question.add_reaction("3️⃣")
    await question.add_reaction("4️⃣")
    def check(reaction, user):
        if user == ctx.author and reaction.message.id == question.id:
            if str(reaction.emoji) == (quiz_pic.allquiz[number][6]).get('True'):
                return True
            raise ValueError
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
    except ValueError:
        with open("users.json", "r") as fi:
            users = json.load(fi)
        update_data(users, ctx.author)
        await ctx.channel.send("<:x_:786493309785735219> ตอบผิด")
        await add_incorrect(users, ctx.author)
        with open("users.json", "w") as fi:
            json.dump(users, fi)
    except:
        await ctx.channel.send("⏰ หมดเวลา")
    else:
        with open("users.json", "r") as fi:
            users = json.load(fi)
        update_data(users, ctx.author)
        await ctx.channel.send(":white_check_mark: ตอบถูก")
        await add_point(users, ctx.author, pointperquiz)
        await add_correct(users, ctx.author)
        await level_up(users, ctx.author, ctx.channel)
        with open("users.json", "w") as fi:
            json.dump(users, fi)

@bot.command()
async def stats(ctx):#คำสั่งโชว์หน้าต่างสถิติ
    with open("users.json", "r") as fi:
        users = json.load(fi)
    update_data(users, ctx.author)
    embed=discord.Embed(title=f"{ctx.author.name}'s stats", color=0xef8206)
    embed.set_author(name=f"{bot.user.name}", icon_url=f"{bot.user.avatar_url}")
    embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
    for key, i in users[str(ctx.author.id)].items():
        embed.add_field(name=key, value=i, inline=True)
    await ctx.send(embed=embed)

bot.run(token)
