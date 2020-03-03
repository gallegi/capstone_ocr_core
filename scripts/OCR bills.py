import glob
import json
import pandas as pd
from tqdm import tqdm

json_paths = glob.glob('/home/linhnq3/Disk2T/khanhtd2/utop/output/output OCR/*.json')

igore_characters = ':;'

def hard_filter(recipe):
    name = ''
    for character in igore_characters:
        recipe.replace(character,' ')

    if 'ler' in recipe:
        name = recipe.split('ler')[-1].split('\n')[0].strip()
    if 'lar' in recipe:
        name = recipe.split('lar')[-1].split('\n')[0].strip()

    return name

seller_names = []
recipees = []
image_names =[]
df = pd.DataFrame()
df['image name'] = image_names
df['seller name'] = seller_names
df['recipe'] = recipees
df.to_csv('seller_names.csv',encoding='utf-8',index=False)

for path in tqdm(json_paths):
    data = json.loads(open(path).read())
    responses = data['responses']

    seller_names = []
    recipees = []
    image_names = []

    for response in responses:
        text = response['textAnnotations'][0]['description']
        text = text.lower()
        text = text.replace(' : ', ':').replace(': ', ':').replace(' :', ':')
        recipes = text.split('.jpg')
        for recipe in recipes:
            seller_name = ''
            image_name = recipe.split('name:')[-1] + '.jpg'
            seller_name = recipe.split('ler:')[-1].split('\n')[0]
            if len(seller_name) == 0:
                seller_name = hard_filter(recipe)

            image_names.append(image_name)
            seller_names.append(seller_name)
            if seller_name != '':
                recipe = ''
            recipees.append(recipe)

    df = pd.DataFrame()
    df['image name'] = image_names
    df['seller name'] = seller_names
    df['recipe'] = recipees
    df.to_csv('seller_names.csv', encoding='utf-8', index=False,header=False,mode='a')



