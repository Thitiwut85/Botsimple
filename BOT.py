import discord
import time
import asyncio
import random as rd
import quiz_choice
from discord.ext import commands

bot = commands.Bot(command_prefix='?', help_command=None)
token = ''#ปล่อยว่างไว้

@bot.event
async def on_ready() :
    print("? Started")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('?help'))
@bot.event
async def on_message(message) :
    await bot.process_commands(message)
@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Command", color=0xef8206)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/786169057953972224/786504574042243072/question.png")
    embed.add_field(name="`?help`", value="คำสั่งต่างๆ", inline=False)
    embed.add_field(name="`?quiz <ตัวเลข>`", value="เลือกข้อที่จะทำ", inline=True)
    embed.add_field(name="`ตัวเลข`", value="1-10", inline=True)
    embed.add_field(name="`?random`", value="สุ่ม quiz", inline=False)
    await ctx.send(embed=embed)
@bot.command()
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
    embed.set_footer(text="Time: 15 seconds")
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
        await ctx.channel.send("<:x_:786493309785735219> ตอบผิด")
    except:
        await ctx.channel.send("⏰ หมดเวลา")
    else:
        await ctx.channel.send(":white_check_mark: ตอบถูก")
@bot.command()
async def random(ctx):
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
    embed.set_footer(text="Time: 15 seconds")
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
        await ctx.channel.send("<:x_:786493309785735219> ตอบผิด")
    except:
        await ctx.channel.send("⏰ หมดเวลา")
    else:
        await ctx.channel.send(":white_check_mark: ตอบถูก")
bot.run(token)
