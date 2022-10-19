import math
import sys
import pandas as pd
import requests
import json
import io
import csv
import pprint


my_headers = {'x-hasura-admin-secret' : 'pux6hp1r1KcZU4XLB9hIhCRDtO8MpuxTp5oQGhMxeQsDRzvPZCDBSksd1F4Ywmdl',
    'content-type': 'application/json'
}


response = requests.get("https://react-labs.hasura.app/api/rest/recipeChecker", headers=my_headers)

res = response.json()

recipes = res['Recipe_DB']

df_recipes = pd.DataFrame(recipes)

errors = []

for recipe in recipes:
    steps = recipe['steps']

    #if recipe['Recipe_ID'] == '1d85401a-dbeb-4cd6-8d17-7bd483971b94':

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
                                thisSpeed = 0
                                thisTemp = 0
                                
                                for i, setParamSettings in enumerate(setParams['settings']):
                                    if setParamSettings['time'] == None or \
                                        setParamSettings['speed'] == None or \
                                        setParamSettings['temperature'] == '':
                                        this_error = {}
                                        this_error['Error'] = 'Empty hardcode settings'
                                        this_error['Recipe'] = recipe['Recipe_Name']
                                        this_error['RecipeID'] = recipe['Recipe_ID']
                                        this_error['Step'] = step['name']
                                        this_error['SubStep'] = subStep['name']
                                        errors.append(this_error)
                                
                                    else:
                                        if i == 0:
                                            thisSpeed = setParamSettings['speed']
                                            thisTemp = setParamSettings['temperature']
                                        if setParamSettings['speed'] != thisSpeed:
                                            this_error = {}
                                            this_error['Error'] = 'Speed not same'
                                            this_error['Recipe'] = recipe['Recipe_Name']
                                            this_error['RecipeID'] = recipe['Recipe_ID']
                                            this_error['Step'] = step['name']
                                            this_error['SubStep'] = subStep['name']
                                            errors.append(this_error)
                                        if setParamSettings['temperature'] != thisTemp:
                                            this_error = {}
                                            this_error['Error'] = 'Temperature not same'
                                            this_error['Recipe'] = recipe['Recipe_Name']
                                            this_error['RecipeID'] = recipe['Recipe_ID']
                                            this_error['Step'] = step['name']
                                            this_error['SubStep'] = subStep['name']
                                            errors.append(this_error)
                            
                            # CHECK IF: linear has parameters set
                            # if setting['scaleModel']['type'] == 'linear':
                            #     this_error = {}
                            #     if 'parameters' in setting['scaleModel']:
                            #         setParams = setting['scaleModel']['parameters']
                            #         if setParams['scaleFactor'] == None:
                            #             this_error['Error'] = 'Empty Scale Factor in linear settings'
                            #             this_error['Recipe'] = recipe['Recipe_Name']
                            #             this_error['RecipeID'] = recipe['Recipe_ID']
                            #             this_error['Step'] = step['name']
                            #             this_error['SubStep'] = subStep['name']
                            #             errors.append(this_error)                                    
                            #     else:
                            #         this_error['Error'] = 'NO Parameters in linear settings'
                            #         this_error['Recipe'] = recipe['Recipe_Name']
                            #         this_error['RecipeID'] = recipe['Recipe_ID']
                            #         this_error['Step'] = step['name']
                            #         this_error['SubStep'] = subStep['name']
                            #         errors.append(this_error)
            ## CHECK IF: addIngredients has ingredients
            # if subStep['type'] in ['addIngredients']:
            #     this_error = {}
            #     if 'parameters' in subStep:
            #         if len(subStep['parameters']['items']) == 0:
            #             this_error['Error'] = 'NO Items in addIngredients'
            #             this_error['Recipe'] = recipe['Recipe_Name']
            #             this_error['RecipeID'] = recipe['Recipe_ID']
            #             this_error['Step'] = step['name']
            #             #this_error['SubStep'] = subStep['name'] 
            #             errors.append(this_error)
            #     else:
            #         this_error['Error'] = 'NO Parameters in addIngredients'
            #         this_error['Recipe'] = recipe['Recipe_Name']
            #         this_error['RecipeID'] = recipe['Recipe_ID']
            #         this_error['Step'] = step['name']
            #         this_error['SubStep'] = subStep['name']
            #         errors.append(this_error)


pprint.pprint(errors)

