import sys
sys.path.append('libs/')

import discord
from discord.ext import commands


bot = commands.Bot(intents=discord.Intents.all(),command_prefix = "!", description ="bot de la guilde")

@bot.event
async def on_ready():
	print("Ready !")

@bot.command(pass_context=True)
async def channel(ctx):
	voice = ctx.author.voice
	channel = voice.channel
	await ctx.send(channel.name)

@bot.command(pass_context=True)
async def raid(ctx):
	voice = ctx.author.voice
	channel = voice.channel
	members = channel.members
	for channeltogo in ctx.guild.channels:
		if channeltogo.name == "『💀』- ʀᴀɪᴅ -":
			channelraid = channeltogo
	for member in members:	
		await member.move_to(channelraid)

@bot.command(pass_context=True)
async def taverne(ctx):
	voice = ctx.author.voice
	channel = voice.channel
	members = channel.members
	for channeltogo in ctx.guild.channels:
		if channeltogo.name == "『🍻』- ᴛᴀᴠᴇʀɴᴇ -":
			channelraid = channeltogo
	for member in members:	
		await member.move_to(channelraid)


bot.run("MTE2NzQ3MzYxMDMzNjc3MjE4Ng.Gj6onq.GydBIfwpDSbbm7JPkz8ptqjbDurz5uxrpsUKhs")