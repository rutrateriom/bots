import sys
sys.path.append('libs/')
import discord
import random
from discord.ext import commands


bot = commands.Bot(intents=discord.Intents.all(),command_prefix = "/", description ="bot de danji")
@bot.event
async def on_ready():
	print("Ready !")

@bot.command(pass_context=True)
async def channel(ctx):
	voice = ctx.author.voice
	channel = voice.channel
	name = channel.name
	await ctx.send(name)

@bot.command(pass_context=True)
async def team(ctx,joueur1="personne",joueur2="personne",joueur3="personne",joueur4="personne",joueur5="personne",joueur6="personne",joueur7="personne",joueur8="personne",joueur9="personne",joueur10="personne",joueur11="personne",joueur12="personne",joueur13="personne",joueur14="personne",joueur15="personne",joueur16="personne",joueur17="personne",joueur18="personne",joueur19="personne",joueur20="personne"):
	joueurs = [joueur1,joueur2,joueur3,joueur4,joueur5,joueur6,joueur7,joueur8,joueur9,joueur10,joueur11,joueur12,joueur13,joueur14,joueur15,joueur16,joueur17,joueur18,joueur19,joueur20]
	
	global teamsglob

	if joueur1=="personne":
		voice = ctx.author.voice
		channel = voice.channel
		members = channel.members
		noms = members
		print(noms,type(noms))
		await ctx.send("équipes formées à partir du channel, "+channel.name+":")
		joueurs = noms
		


		#motifs pour les équipes avec n personnes
		motif1=[1]
		motif2=[2]
		motif3=[3]
		motif4=[4]
		motif5=[5]
		motif6=[3,3]
		motif7=[4,3]
		motif8=[4,4]
		motif9=[5,4]
		motif10=[5,5]
		motif11=[4,4,3]
		motif12=[4,4,4]
		motif13=[5,4,4]
		motif14=[5,5,4]
		motif15=[5,5,5]
		motif16=[4,4,4,4]
		motif17=[5,4,4,4]
		motif18=[5,5,4,4]
		motif19=[5,5,5,4]
		motif20=[5,5,5,5]
		motifs = [[],motif1,motif2,motif3,motif4,motif5,motif6,motif7,motif8,motif9,motif10,motif11,motif12,motif13,motif14,motif15,motif16,motif17,motif18,motif19,motif20]

		nombrerien = 0

		nombrejoueurs = len(joueurs)

		joueursmelanges = []
		joueursmelangesnom = []

		teams = []
		teamsnom = []

		motifencours = motifs[nombrejoueurs]

		for i in range(nombrejoueurs):

			pif = random.randint(0,len(joueurs)-1)

			joueursmelanges.append(joueurs[pif])
			joueursmelangesnom.append(joueurs[pif].name)
			joueurs.pop(pif)

		for i in motifencours:
			teamsnom.append(joueursmelangesnom[0:i])
			teams.append(joueursmelanges[0:i])
			for p in range(i):
				joueursmelanges.pop(0)
				joueursmelangesnom.pop(0)



		print(teams)
		for g in range(len(teamsnom)):	
			teamtext = ""
			for joueur in teamsnom[g]:
				teamtext += joueur+", "
			await ctx.send("channel "+str(g+1)+": "+teamtext[:-2]+".")

		teamsglob = teams


	else:


		#motifs pour les équipes avec n personnes
		motif1=[1]
		motif2=[2]
		motif3=[3]
		motif4=[4]
		motif5=[5]
		motif6=[3,3]
		motif7=[4,3]
		motif8=[4,4]
		motif9=[5,4]
		motif10=[5,5]
		motif11=[4,4,3]
		motif12=[4,4,4]
		motif13=[5,4,4]
		motif14=[5,5,4]
		motif15=[5,5,5]
		motif16=[4,4,4,4]
		motif17=[5,4,4,4]
		motif18=[5,5,4,4]
		motif19=[5,5,5,4]
		motif20=[5,5,5,5]
		motifs = [[],motif1,motif2,motif3,motif4,motif5,motif6,motif7,motif8,motif9,motif10,motif11,motif12,motif13,motif14,motif15,motif16,motif17,motif18,motif19,motif20]

		nombrerien = 0

		for i in joueurs:
			if i == "personne":
				nombrerien+=1

		for i in range(nombrerien):
			joueurs.remove("personne")

		nombrejoueurs = len(joueurs)

		joueursmelanges = []

		teams = []

		motifencours = motifs[nombrejoueurs]

		for i in range(nombrejoueurs):

			pif = random.randint(0,len(joueurs)-1)

			joueursmelanges.append(joueurs[pif])
			joueurs.pop(pif)

		for i in motifencours:
			teams.append(joueursmelanges[0:i])
			for p in range(i):
				joueursmelanges.pop(0)

		print(teams)
		for g in range(len(teams)):	
			teamtext = ""
			for joueur in teams[g]:
				teamtext += joueur+", "
			await ctx.send("channel "+str(g+1)+": "+teamtext[:-2]+".")


@bot.command(pass_context=True)
async def arrange(ctx):
	for channel in ctx.guild.channels:
		print(channel.name)
		if channel.name == "Dota 2 Chan 1":
			channel1=channel
		if channel.name == "Dota 2 Channel 2":
			channel2=channel
		if channel.name == "Dota 2 Channel 3":
			channel3=channel
		if channel.name == "Dota 2 Channel 4":
			channel4=channel
	channels = [channel1,channel2,channel3]

	msgtosend = random.randint(0,3)
	if msgtosend == 0:
		await ctx.send("c'est parti !")
	if msgtosend == 1:
		await ctx.send("ok.")
	if msgtosend == 2:
		await ctx.send("let's go !")
	else:
		await ctx.send(":thumbsup:")

	global teamsglob
	for g in range(len(teamsglob)):	
		for joueur in teamsglob[g]:
			await joueur.move_to(channels[g])
		



bot.run("[la référence]")