from langchain.agents import Tool
from langchain.agents import load_tools
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
import re
from langchain.tools import DuckDuckGoSearchRun
from langchain.chains import ConversationChain
import os
from langchain.agents.agent_toolkits import GmailToolkit
import requests
from PIL import Image, ImageDraw, ImageFont
import random
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)


key = 'Api-KEY'
template = "genere un meme (Humour d'internet) sur '{sujet}', il faut {mode} phrases, chaque phrases doit etre courtes (moins de 10 mots).Si la phrase n'est pas un dialogue alors ne pas mettre de quotes. Le formatage de la reponse doit etre les deux phrases separer par un '|' n'ecrit pas de ponctuation et ne precise pas le type du text."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "en français : {context}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo" ,openai_api_key=key)

def ft_dl(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_content = response.content

        with open("ref.jpeg", "wb") as file:
            file.write(image_content)
            print("L'image reference a été téléchargée avec succès.")
    else:
        print("Échec du téléchargement de l'image.")
        return 1
    return 0


def ft_text_to_image(mode,x1,y1,x2,y2,text,file="meme.jpg"):
    image = Image.open(file)
    draw = ImageDraw.Draw(image)
    point1 = (x1, y1)
    point2 = (x2, y2)
    font_size = 40
    font = ImageFont.truetype("Memesique-Regular.ttf", font_size)  # Chargement de la police
    text_width, _ = draw.textsize(text, font=font)
    if text_width > x2 - x1:
        new_font_size = int(font.size * (x2 - x1 - 20) / text_width)
        font = ImageFont.truetype("Memesique-Regular.ttf", new_font_size)

    text_width, text_height = draw.textsize(text, font=font)
    text_x1 = point1[0] + (point2[0] - point1[0]) // 2 - text_width // 2
    text_y1 = point1[1] + (point2[1] - point1[1]) // 2 - text_height // 2
    couleur_contour = (0,0,0)
    for adj in [-3,-2, -1, 0, 1, 2,3]:
        draw.text((text_x1+adj,text_y1), text, fill=couleur_contour, font=font)
        draw.text((text_x1,text_y1+adj), text, fill=couleur_contour, font=font)
        draw.text((text_x1+adj,text_y1+adj), text, fill=couleur_contour, font=font)
        draw.text((text_x1+adj,text_y1-adj), text, fill=couleur_contour, font=font)
    draw.text((text_x1, text_y1), text, font=font, fill='white')
    image.save("meme.jpg")

def search_from_mode(mode_recherche):
    with open("refmeme.txt", "r") as file:
        lines = file.readlines()
        lignes_mode = [line for line in lines if line.split()[0] == str(mode_recherche)]
        if lignes_mode:
            ligne_aleatoire = random.choice(lignes_mode)
            elements = ligne_aleatoire.split()
            if len(elements) >= 5 + mode_recherche*4:
                num_lines = int(elements[0])
                image_url = elements[1]
                coord_elements = elements[2:2 + mode_recherche*4]
                coords = []
                for i in range(0, len(coord_elements), 4):
                    x1 = int(coord_elements[i])
                    y1 = int(coord_elements[i + 1])
                    x2 = int(coord_elements[i + 2])
                    y2 = int(coord_elements[i + 3])
                    coords.append((x1, y1, x2, y2))
                text = ' '.join(elements[2 + mode_recherche*4:])
                result = "Coordonnées de(s) texte(s) : "
                print(f"URL de l'image : {image_url}")
                for coord in coords:
                    print(f" - (x1 = {coord[0]}, y1 = {coord[1]}, x2 = {coord[2]}, y2 = {coord[3]})")
            else:
                print("La ligne ne contient pas suffisamment d'éléments.")
                exit()
        else:
            print(f"Aucune ligne ne correspond au mode {mode_recherche}.")
            exit()
        return image_url, coords, text


def ft_split_text_format(chaine, longueur):
    i = 0
    result = ''
    for letter in chaine:
        if(i >= longueur and letter == ' '):
            result += '\n'
            i = -1
        elif((i == 0 or i == len(chaine)) and letter == '"'):
            continue
        else:
            result += letter
        i += 1
    return result.strip('\"').strip('\n')

def make_meme(coords, phrases, mode):
    if '|' in phrases:
        lstext = phrases.split('|')
    else:
        lstext = phrases.split('\n')
    i = 0
    for coord in coords:
        resultat = re.search(r'"([^"]*)"', lstext[i])
        if resultat is not None:
            lstext[i] = resultat.group(1)
        else:
            print("Aucune correspondance trouvée.")
        if len(lstext[i]) > 30:
            final = ft_split_text_format(lstext[i], 30)
        else:
            final = lstext[i].strip('\"').strip('\n')
        x1, y1, x2, y2 = coord
        if i == 0:
            ft_text_to_image(mode, x1, y1,x2,y2, final, "ref.jpeg")
            tmp = 0
        else:
            ft_text_to_image(mode, x1, y1, x2, y2 ,final)
        i += 1

def lemain():
    sujet = input("choisit un sujet de meme : ")
    mode = 2
    url , coords, context  = search_from_mode(mode)
    ft_dl(url)

    reponse = llm(chat_prompt.format_prompt(sujet=sujet,mode=str(mode),context=context).to_messages())
    reponse =str(reponse.content)

    print("\n\nREPONSE = "+reponse)

    print("coords = "+str(coords))
    make_meme(coords, reponse, mode)
    os.system("rm ref.jpeg")
    print("terminer")
    
lemain()
