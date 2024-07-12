import sys
sys.path.append('libs/')

import discord
import random
from discord.ext import commands
from discord.ui import View, Select
from scraplegi import *


def truncate(text, max_length=100):
    return text if len(text) <= max_length else text[:max_length-3] + "..."

bot = commands.Bot(intents=discord.Intents.all(),command_prefix = "/", description ="bot de danji")


class ArticleSelectView(discord.ui.View):
    def __init__(self, articles):
        super().__init__()
        self.add_item(ArticleSelectMenu(articles))

class ArticleSelectMenu(discord.ui.Select):
    def __init__(self, articles):
        super().__init__(placeholder="Sélectionnez un article...", row=0)
        self.articles = articles  # Stocker la liste complète des articles
        for index, article in enumerate(articles):
            # Ici, article[0] est le titre, article[1] est le teaser, et article[2] est l'URL
            self.add_option(label=truncate(article[0]), description=truncate(article[1], 50), value=str(index))
    async def callback(self, interaction: discord.Interaction):
        # Récupérer l'article sélectionné à l'aide de l'index stocké dans `self.values[0]`
        selected_index = int(self.values[0])  # Convertir la valeur sélectionnée en un entier pour l'utiliser comme index
        selected_article = self.articles[selected_index]  # Récupérer l'article sélectionné de la liste

        # selected_article[2] devrait être l'URL de l'article sélectionné
        article_url = "https://www.legifrance.gouv.fr/"+selected_article[2]

        #aller scraper la page en question: 
        article = get_precise_article(article_url,selected_article[0])


        await interaction.response.send_message(selected_article[0]+": "+article)

class TitleSelectView(View):
	def __init__(self, titles, text, code):
		self.text=text
		self.code = code
		super().__init__(timeout=180)  # Timeout de 3 minutes par exemple
		# Ajouter le menu déroulant au view
		self.add_item(TitleSelectMenu(titles, text, code))
class TitleSelectMenu(Select):
    def __init__(self, titles, text, code):
        self.text = text
        self.code = code
        self.id_to_title_map = {str(index): title for index, title in enumerate(titles)}
        
        options = [
            discord.SelectOption(label=truncate(title), value=str(index))
            for index, title in enumerate(titles)
        ]
        
        super().__init__(placeholder="Choisissez un titre...", options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_title_index = self.values[0]  # La valeur sélectionnée est l'index du titre
        selected_title = self.id_to_title_map[selected_title_index]  # Récupérer le titre sélectionné

        # Utiliser self.text et self.code pour récupérer les articles associés au titre sélectionné
        articles = getAllResultsFrom(selected_title, self.text, self.code)
        await interaction.response.send_message("voilà:")
        # Afficher tous les articles récupérés
        for result in articles:
            await interaction.followup.send(f"{result[0]}: {result[1]}")

        # Créer et envoyer le menu de sélection des articles
        view = ArticleSelectView(articles)
        await interaction.followup.send("Sélectionnez un article pour plus de détails :", view=view)

@bot.event
async def on_ready():
	print("Ready !")

@bot.command(pass_context=True)
async def search(ctx,text,code=""):
	
	reaction = SendResultFrom(text,code)
	msg = await ctx.send(reaction)
	if reaction != "il n'y a aucun résultat à ce sujet.":
		#code si il y a des résultats
		await msg.add_reaction('👍')
		await msg.add_reaction('👎')
	def check(reaction, user):
		return user == ctx.author and str(reaction.emoji) in ['👍', '👎'] and reaction.message.id == msg.id

	try:
		reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

		if str(reaction.emoji) == '👍':
			titles = getAllTitlesFrom(text,code)
			view = TitleSelectView(titles, text, code)
			await ctx.send("Choisissez un titre :", view=view)                # Insérez ici le code pour afficher toutes les options
		else:
			await ctx.send("ok.")
	except TimeoutError:
		i=0




bot.run("[la référence]")