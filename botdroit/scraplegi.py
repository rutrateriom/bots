#imports
import requests
from bs4 import BeautifulSoup
#fonctions
import sys
sys.path.append('libs/')
def PageFromText(text,code=""):
	codecodes = {"civil" : "mNqhdw%3D%3D",
				 "commerce" : "Rg8KwQ%3D%3D",
				 "procédure_civile" : "3W3LkQ%3D%3D",
				 "procédure_pénale" : "aQb8lg%3D%3D",
				 "pénal" : "M94xeQ%3D%3D"}
	if code == "":
		page = "https://www.legifrance.gouv.fr/search/all?tab_selection=all&searchField=ALL&query="+text+"&searchType=ALL&typePagination=DEFAULT&pageSize=10&page=1&tab_selection=all#all"
	else:
		page = "https://www.legifrance.gouv.fr/search/code?tab_selection=code&searchField=ALL&query="+text+"&page=1&init=true&nomCode="+codecodes[code]
		page = "https://www.legifrance.gouv.fr/search/code?tab_selection=code&searchField=ALL&query="+text+"&page=1&init=true&nomCode="+codecodes[code]
	return page

def Nombre_Resultats(page):
	headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
	}

	legifrance = requests.get(page,headers)

	soup = BeautifulSoup(legifrance.text, 'html.parser')
	pages = soup.find_all(class_='pager-item')
	research = soup.find_all(class_='name-result-item')
	return len(research),len(pages)

def SendResultFrom(text,code=""):
	page = PageFromText(text,code)
	nombre_result,nombre_pages = Nombre_Resultats(page)
	if nombre_pages > 1:
		return "le nombre de pages est de "+str(nombre_pages)+", affichier la première ?"
	else:
		if nombre_result == 0:
			return "il n'y a aucun résultat à ce sujet."
		elif nombre_result >= 1:
			return "il y a " + str(nombre_result) + ". Les afficher ?"

def getAllTitlesFrom(text,code=""):
	headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
	}
	legifrance = requests.get(PageFromText(text,code),headers)
	soup = BeautifulSoup(legifrance.text, 'html.parser')
	titres = soup.find_all(class_='link')

	textes_uniques = set()

	# Initialisation d'une liste pour conserver les éléments uniques
	elements_uniques = []

	for element in titres:
		if element.text not in textes_uniques and element.text:
			# Ajout du texte à l'ensemble des textes uniques
			textes_uniques.add(element.text)
			# Ajout de l'élément à la liste des éléments uniques
			elements_uniques.append(element.text)



	return(elements_uniques)

def getAllResultsFrom(titresection, text, code):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    legifrance = requests.get(PageFromText(text, code), headers=headers)
    soup = BeautifulSoup(legifrance.text, 'html.parser')
    articles_data = []

    # Récupérer tous les éléments <h3> avec la classe "title-result-item link"
    h3_elements = soup.find_all("h3", class_="title-result-item link")

    # Filtrer manuellement les éléments dont le texte contient "famille"
    for h3 in h3_elements:
        if titresection in h3.get_text():  # Utiliser get_text() pour inclure tout le texte, y compris celui dans les balises HTML internes
            # Le reste de votre logique pour traiter les conteneurs "content" voisins
            for content in h3.find_next_siblings("div", class_="content"):
                article_title_tag = content.find("h3", class_="article-result-item")
                if article_title_tag and article_title_tag.find("a"):
                    article_title = article_title_tag.a.text.strip()
                    article_url = article_title_tag.a['href']
                    teaser_tag = content.find("div", class_="teaser")
                    teaser = teaser_tag.blockquote.text.strip() if teaser_tag and teaser_tag.blockquote else "Pas de teaser disponible"
                    articles_data.append([article_title, teaser, article_url])

    return articles_data

def get_precise_article(url,article_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    response = requests.get(url,headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trouver le <li> contenant le nom de l'article
    li_elements = soup.find_all("li", class_="opened", **{"data-a": "false"})
    for li in li_elements:
        name_article_tag = li.find("p", class_="name-article")
        if name_article_tag and name_article_tag.find("a") and article_name in name_article_tag.a.text:
            # Trouver le <div class="content"> correspondant
            content_div = li.find("div", class_="content")
            if content_div:
                # Extraire tous les paragraphes <p> et les séparer par des doubles sauts de ligne
                paragraphs = [p.get_text() for p in content_div.find_all("p")]
                article_content = "\n\n".join(paragraphs)
                return article_content
                
    # Retourner une chaîne vide si l'article n'est pas trouvé
    return ""
