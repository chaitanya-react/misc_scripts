import math
import sys
import pandas as pd
import requests
import json
import io
import csv
import pprint
import json


my_headers = {'x-hasura-admin-secret' : 'pux6hp1r1KcZU4XLB9hIhCRDtO8MpuxTp5oQGhMxeQsDRzvPZCDBSksd1F4Ywmdl',
    'content-type': 'application/json'
}


response = requests.get("https://react-labs.hasura.app/api/rest/recipeChecker", headers=my_headers)

res = response.json()

recipes = res['Recipe_DB']

df_recipes = pd.DataFrame(recipes)

errors = []

path = '/Users/chaitanya/Documents/scratch/newjsonerrors/'

for recipe in recipes:
    steps = recipe['steps']

    #if recipe['Recipe_ID'] == '1d85401a-dbeb-4cd6-8d17-7bd483971b94':
    error_recipe = False
    for step in steps:
        #print(step)
        
        for subStep in step['subSteps']:

            if subStep['type'] in ['cook','cut','saute','cook','boil','mix','roast']:
            #if subStep['type'] == 'cook':
                if 'settings' in subStep['parameters']:
                    for setting in subStep['parameters']['settings']:
                        if 'scaleModel' in setting:    
                            pass

                            # CHECK IF: Scale mode = hardcode && settings are empty
                            if setting['scaleModel']['type'] == 'hardcode':
                                setParams = setting['scaleModel']['parameters']
                                
                                
                                for i, setParamSettings in enumerate(setParams['settings']):
                                    if setParamSettings['time'] == None or \
                                        setParamSettings['speed'] == None or \
                                        setParamSettings['temperature'] == '':
                                        pass
                                
                                    else:
                                        # get settings for serving size 2
                                        thisSpeed = setParams['settings'][1]['speed']
                                        thisTemp = setParams['settings'][1]['temperature']
                                            
                                        if setParamSettings['speed'] != thisSpeed or \
                                            setParamSettings['temperature'] != thisTemp:
                                            this_error = {}
                                            this_error['Error'] = 'Speed or temp not same'
                                            this_error['Recipe'] = recipe['Recipe_Name']
                                            this_error['RecipeID'] = recipe['Recipe_ID']
                                            this_error['Step'] = step['name']
                                            this_error['SubStep'] = subStep['name']
                                            errors.append(this_error)
                                            setParamSettings['speed'] = thisSpeed
                                            setParamSettings['temperature'] = thisTemp
                                            error_recipe = True

    if error_recipe is True:
        print(recipe['Recipe_Name'])                               
        #dump json
        with open(path+recipe['Recipe_Name']+'.json', 'w', encoding='utf-8') as \
            f:json.dump(steps, f, ensure_ascii=False, indent=4)
                    
                                            
                            

# pprint.pprint(errors)

