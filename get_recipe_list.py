import requests
import json
import sys

url = 'https://www.paprikaapp.com/api/v2/'

# get paprika creds
with open('paprika_creds.txt', 'r') as myfile:
    creds_data=myfile.read()

creds_data_json = json.loads(creds_data)

# get paprika token
token_response = requests.post(url+'account/login/', data=creds_data_json)

token = token_response.json()['result']['token']

# setup auth header with token for future requests
auth_header = {
    'Authorization': 'Bearer ' + token
}

# get list of recipe uids
recipe_list_response = requests.get(url+'sync/recipes', headers=auth_header)

# parse list and get recipe names
recipe_name_list = []
i = 1

number_of_recipes = str(len(recipe_list_response.json()['result']))

for x in recipe_list_response.json()['result']:
    sys.stdout.write('\033[sGetting recipe ' + str(i) + ' of ' + number_of_recipes + '...\033[u')
    sys.stdout.flush()

    i=i+1
    recipe_response = requests.get(url+'sync/recipe/'+x['uid'], headers=auth_header)
    if not recipe_response.json()['result']['in_trash']:
        recipe_name_list.append(recipe_response.json()['result']['name'])

print('\n\n----------\n\nTable of Contents\n\n')

# sort the list
recipe_name_list.sort()

# print the sorted list
for y in recipe_name_list:
    print(y)
