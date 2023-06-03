import requests
from PIL import Image, ImageDraw, ImageFont
import random

def ft_dl(url):
    # url = "https://i.pinimg.com/564x/7d/d0/d4/7dd0d4d75b8570eae49ce54e1abb13ab.jpg"
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

def search_from_mode(mode_recherche):
    with open("refmeme.txt", "r") as file:
        lines = file.readlines()
        lignes_mode = [line for line in lines if line.split()[0] == str(mode_recherche)]

        if lignes_mode:
            ligne_aleatoire = random.choice(lignes_mode)
            elements = ligne_aleatoire.split()

            if len(elements) >= 5 + mode_recherche*2:
                num_lines = int(elements[0])
                image_url = elements[1]
                coord_elements = elements[2:2 + mode_recherche*2]
                coords = [(int(coord_elements[i]), int(coord_elements[i + 1])) for i in range(0, len(coord_elements), 2)]
                text = ' '.join(elements[2 + mode_recherche*2:])

                result = "Nombre de text a generer : "+str(num_lines)+"\nCoordonnées de(s) text(s) : "
                print(f"URL de l'image : {image_url}")
                for coord in coords:
                    result += "\n - (x = "+str(coord[0])+", y = "+str(coord[1])+")"
                result += "\nContexte de l'image : "+text
            else:
                print("La ligne ne contient pas suffisamment d'éléments.")
        else:
            print(f"Aucune ligne ne correspond au mode {mode_recherche}.")
        return result
    

def ft_text_to_image(x,y,text):
    font = ImageFont.truetype("Memesique-Regular.ttf", 50)
    image = Image.open("ref.jpeg")
    draw = ImageDraw.Draw(image)
    draw.text((x, y), text, fill=color, font=font)
    image.save("meme.jpg")
    

sujet = "parcoursup"

ft_text_to_image()



# genere juste le texte d'un meme satirique qui parle parcoursup.
