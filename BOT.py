import discord
from discord.ext import commands
bot = commands.Bot(command_prefix='?', help_command=None)
token = ''#ปล่อยว่างไว้
@bot.event
async def on_ready() :
    print("? Started")
@bot.event
async def on_message(message) :
    await bot.process_commands(message)
@bot.command()
async def start(ctx) :
    await ctx.send('OK')
@bot.command()#อันนี้ คำสั่ง help
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.set_author(name='Help?')
    embed.add_field(name='?start', value='OK', inline=False)
    await author.send(embed=embed)
bot.run(token)
