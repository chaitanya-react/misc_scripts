

import math
import sys
import pandas as pd
import requests
import json
import io
import csv



my_headers = {'x-hasura-admin-secret' : 'pux6hp1r1KcZU4XLB9hIhCRDtO8MpuxTp5oQGhMxeQsDRzvPZCDBSksd1F4Ywmdl',
    'content-type': 'application/json'
}


response = requests.get("https://react-labs.hasura.app/api/rest/lookupdata", headers=my_headers)

res = response.json()

# query MyQuery {
#   Recipe_DB {
#     Recipe_ID
#     Recipe_Name
#   }
#   users {
#     id
#     nickName
#     altId
#   }
# }

users = res['users']
recipes = res['Recipe_DB']




#recipes

recipes.append({"Recipe_ID":"drivehardware","Recipe_Name":"Manual Mode"})

s_recipes = io.StringIO()

df_recipes = pd.DataFrame(recipes)
df_recipes.to_csv('recipes.csv', index=False, line_terminator='\
')
df_recipes.to_csv(s_recipes, index=False, line_terminator='\
')


put_headers = {"Accept": "application/json", "Content-Type": "text/csv"}
put_response = requests.put('https://api.mixpanel.com/lookup-tables/e34aecdd-58d7-4d67-9d31-05dc36d38eac?project_id=2762736',
    auth=('hasura_sync.28ae7f.mp-service-account', 'ySXiyq8zXl9EpvcnQyw7O2TvjBZj5Olg'), 
    headers=put_headers, 
    data=s_recipes.getvalue().encode('utf-8'))


print(put_response.json())



# users

s_users = io.StringIO()

users.append({"id":"any","nickName":"React Office", "altId": None })
users.append({"id":"default_user","nickName":"React Office", "altId": None})

df_users = pd.DataFrame(users)

for index, row in df_users.iterrows():
    if row.altId is not None:
        row.id = row.altId

df_users.drop('altId', axis=1, inplace=True)


df_users.rename({'id': 'user_id', 'nickName': 'user_name'}, axis=1, inplace=True)
df_users.to_csv('users.csv', index=False, line_terminator='\
')
df_users.to_csv(s_users, index=False, line_terminator='\
')


put_headers = {"Accept": "application/json", "Content-Type": "text/csv"}
put_response = requests.put('https://api.mixpanel.com/lookup-tables/10bbdb34-be71-415f-9c10-7a3013807c70?project_id=2762736',
    auth=('hasura_sync.28ae7f.mp-service-account', 'ySXiyq8zXl9EpvcnQyw7O2TvjBZj5Olg'), 
    headers=put_headers, 
    data=s_users.getvalue())


print(put_response.json())













# for r in recipes:
#     t_recipes[r['Recipe_ID']] = r['Recipe_Name']


# for u in users:
#     t_users[u['user_id']] = u['user_name']



# for d in devices:
#     t_devices[d['_id']] = d['displayName']

# session_list = list()

# # recipeID
# #     sessionID
# #     startTime
# #     userID
# #     deviceID
# for s in sessions:
#     this_session = dict()
#     this_session['session_id'] = s['sessionID']
    
#     #this_session['device_id'] = s['deviceID']
#     #this_session['display_name'] = t_devices[s['deviceID']]['displayName']    

#     this_session['recipe_id'] = s['recipeID']
#     if s['recipeID'] == "drivehardware":
#         this_session['recipe_name'] = "drivehardware"
#     elif s['recipeID'] not in t_recipes:
#         this_session['recipe_name'] = "UNKNOWN"
#     else:
#         this_session['recipe_name'] = t_recipes[s['recipeID']]

#     this_session['user_id'] = s['userID']

#     if s['userID'] == "any" or s['userID'] == "default_user":
#         this_session['user_name'] = "React Office"
#     elif s['userID'] not in t_users:
#         this_session['user_name'] = "UNKNOWN"
#     else:
#         this_session['user_name'] = t_users[s['userID']]

#     this_session['test'] = 'test'


#     session_list.append(this_session)
