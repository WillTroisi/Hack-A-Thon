from openfoodfacts import API, APIVersion, Country, Environment, Flavor
import pandas as pd
import openai
import requests
import numpy as np


api = API(
    user_agent= "menuApp",
    username=None,
    password=None,
    country=Country.us,
    flavor=Flavor.off,
    version=APIVersion.v2,
    environment=Environment.org,
)

ingredDict = {}

def ingredEmissions(searchKey):
    if searchKey in ingredDict:
        return ingredDict[searchKey]
    

    results = api.product.text_search(searchKey)['products']
    df = pd.DataFrame(results)
    print('Attempting to estimate', searchKey)

    for i in range(len(df)):
        foodID = df.loc[i,'_id']

        tempDict = api.product.get(foodID,fields=['ecoscore_data'])
        try:
            co2 = tempDict['ecoscore_data']['agribalyse']['co2_total']
            if co2 is not None:
                ingredDict[searchKey] = co2
                return co2
        except Exception as e:
            continue

    return 0 ## NUCLEAR OPTION, DELETE IF MUST

        
def dataFormatter(filename):
    temp_df = pd.read_json(filename)
    temp_df = temp_df.transpose()
    temp_df['Meal Emissions'] = temp_df.apply(lambda row: foodEmissions(row),axis=1)

    return(temp_df)


def foodEmissions(row):
    total_volume = float(row['total_g'])
    
    ingredients = row['ingredients']
    emissionsPerGram = 0

    if not ingredients:
        emissionsPerGram = ingredEmissions(row.name)
    else:
        temp_df = pd.DataFrame(ingredients).transpose()
        temp_df['Emissions'] = temp_df.apply(lambda row: ingredEmissions(row['name'])*((float(row['percent']))/100),axis=1)
        emissionsPerGram = temp_df['Emissions'].sum()
    


    return emissionsPerGram


def percentile(data, observation):
    sorted_data = sorted(data)

    index = sorted_data.index(observation)

    percentile_of_number = (index + 1) / len(sorted_data) * 100 
    
    return percentile_of_number


def rating(DataFrame):
    tempDF = DataFrame.copy()
    tempDF['tempCalorie'] = tempDF.apply(lambda row: -1 * row['calories'], axis = 1)
    calorie_data = tempDF['tempCalorie'].tolist()
    tempDF['Calorie Rating'] = tempDF.apply(lambda row: percentile(calorie_data,row['tempCalorie']),axis=1)
    
    tempDF['tempEmissions'] = tempDF.apply(lambda row: -1 * row['Meal Emissions'], axis = 1)
    emissions_data = tempDF['tempEmissions'].tolist()
    tempDF['Emission Rating'] = tempDF.apply(lambda row: percentile(emissions_data,row['tempEmissions']),axis=1)
    
    tempDF['Overall Rating'] = tempDF.apply(lambda row: ((row['Emission Rating'] + row['Calorie Rating'])/2),axis = 1)

    return tempDF


def finalFormat(DataFrame):
    tempDF = DataFrame.drop(columns = ['ingredients','tempCalorie','tempEmissions'])
    return tempDF

def main():
    rawData = dataFormatter('menu_info_info(2).json')
    rawData['meal'] = rawData.index
    rawData.to_csv('backup.csv',index=False)
    stillRawData = pd.read_csv('backup.csv')

    ratedData = rating(stillRawData)
    formattedData = finalFormat(ratedData)

    formattedData.to_json('output.json', orient='records')


main()











