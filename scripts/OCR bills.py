import glob
import json

from tqdm import tqdm

json_paths = glob.glob('data/google_api_response/*.json')

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


for path in json_paths:
    data = json.loads(open(path).read())
    responses = data['responses']
    for response in tqdm(responses):
        text = response['textAnnotations'][0]['description']
        text = text.lower()
        text = text.replace(' : ', ':').replace(': ', ':').replace(' :', ':')

        recipes = text.split('.jpg')
        for recipe in recipes:

            image_name = recipe.split('name:')[-1] + '.jpg'
            seller_name = recipe.split('ler:')[-1].split('\n')[0]
            print('-' * 50)
            if len(seller_name) == 0:
                print(recipe)
            seller_name = 'UNKNOWN'
            # print('Image NAME : {} SELLER NAME : {}'.format(image_name,seller_name))
