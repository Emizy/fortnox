import time

import requests
import pandas as pd

dataload = {
    '@url': [],
    'ArticleNumber': [],
    'Description': [],
    'DisposableQuantity': [],
    'EAN': [],
    'Housework': [],
    'PurchasePrice': [],
    'SalesPrice': [],
    'QuantityInStock': [],
    'ReservedQuantity': [],
    'StockPlace': [],
    'StockValue': [],
    'Unit': [],
    'VAT': [],
    'WebshopArticle': [],
    'Active': []
}

headers = {
    "Access-Token": "f895dac6-9b6a-4885-8daa-2041512f0911",
    "Client-Secret": "I56Jh4yJSU",
    "Content-Type": "application/json",
    "Accept": "application/json",

}


def process_article(datas):
    for data in datas:
        dataload['@url'].append(data.get('@url'))
        dataload['ArticleNumber'].append(data.get('ArticleNumber'))
        dataload['Description'].append(data.get('Description'))
        dataload['DisposableQuantity'].append(data.get('DisposableQuantity'))
        dataload['EAN'].append(data.get('EAN'))
        dataload['Housework'].append(data.get('Housework'))
        dataload['PurchasePrice'].append(data.get('PurchasePrice'))
        dataload['SalesPrice'].append(data.get('SalesPrice'))
        dataload['QuantityInStock'].append(int(data.get('QuantityInStock')))
        dataload['ReservedQuantity'].append(data.get('ReservedQuantity'))
        dataload['StockPlace'].append(data.get('StockPlace'))
        dataload['StockValue'].append(data.get('StockValue'))
        dataload['Unit'].append(data.get('Unit'))
        dataload['VAT'].append(data.get('VAT'))
        dataload['WebshopArticle'].append(data.get('WebshopArticle'))
        url_call = requests.get(data.get('@url'), headers=headers).json()
        dataload['Active'].append(url_call['Article'].get('Active'))


# Question 3
def UpdateQuantityInStock(dataframe):
    for i in range(len(dataframe)):
        dataframe.loc[i, "QuantityInStock"] = 120
        payload = {
            'Article': {
                '@url': dataframe.loc[i, "@url"],
                'ArticleNumber': dataframe.loc[i, "ArticleNumber"],
                'Description': dataframe.loc[i, "Description"],
                'DisposableQuantity': dataframe.loc[i, "DisposableQuantity"],
                'EAN': dataframe.loc[i, "EAN"],
                'Housework': dataframe.loc[i, "Housework"],
                'PurchasePrice': dataframe.loc[i, "PurchasePrice"],
                'SalesPrice': dataframe.loc[i, "SalesPrice"],
                'QuantityInStock': dataframe.loc[i, "QuantityInStock"],
                'ReservedQuantity': dataframe.loc[i, "ReservedQuantity"],
                'StockPlace': dataframe.loc[i, "StockPlace"],
                'StockValue': dataframe.loc[i, "StockValue"],
                'Unit': dataframe.loc[i, "Unit"],
                'VAT': dataframe.loc[i, "VAT"],
                'WebshopArticle': dataframe.loc[i, "WebshopArticle"]
            }
        }
        print(dataframe.loc[i, "ArticleNumber"])
        response = requests.put('https://api.fortnox.se/3/articles/{}'.format(dataframe.loc[i, "ArticleNumber"]),
                                data=payload,
                                headers=headers)
        print('Successfully updated')


# Question 4
def ChangeDescriptionToTest(dataframe):
    dataframe = dataframe[dataframe.QuantityInStock > 50]
    for i in range(len(dataframe)):
        dataframe.loc[i, "Description"] = "{} {}".format(dataframe.loc[i, "Description"], 'TEST')
        payload = {
            'Article': {
                '@url': dataframe.loc[i, "@url"],
                'ArticleNumber': dataframe.loc[i, "ArticleNumber"],
                'Description': dataframe.loc[i, "Description"],
                'DisposableQuantity': dataframe.loc[i, "DisposableQuantity"],
                'EAN': dataframe.loc[i, "EAN"],
                'Housework': dataframe.loc[i, "Housework"],
                'PurchasePrice': dataframe.loc[i, "PurchasePrice"],
                'SalesPrice': dataframe.loc[i, "SalesPrice"],
                'QuantityInStock': dataframe.loc[i, "QuantityInStock"],
                'ReservedQuantity': dataframe.loc[i, "ReservedQuantity"],
                'StockPlace': dataframe.loc[i, "StockPlace"],
                'StockValue': dataframe.loc[i, "StockValue"],
                'Unit': dataframe.loc[i, "Unit"],
                'VAT': dataframe.loc[i, "VAT"],
                'WebshopArticle': dataframe.loc[i, "WebshopArticle"]
            }
        }
        response = requests.post('https://api.fortnox.se/3/articles/{}'.format(dataframe.loc[i, "ArticleNumber"]),
                                 data=payload,
                                 headers=headers)
        print('Successfully created')


try:
    response = requests.get('https://api.fortnox.se/3/articles', headers=headers).json()
    MetaInformation = response['MetaInformation']
    TotalPages = MetaInformation['@TotalPages']
    counter = 1
    for count in range(int(TotalPages)):
        resp = requests.get('https://api.fortnox.se/3/articles/?page={}'.format(counter), headers=headers)
        if resp.status_code == 200:
            resp = resp.json()
            process_article(resp['Articles'])
        counter += 1
    df = pd.DataFrame(data=dataload)
    # checking if active is True
    df = df[(df.Active == 'True') | (df.Description.str.contains('A'))
            | df.Description.str.contains('K')
            | df.Description.str.contains('M')
            | df.Description.str.contains('C') | (df.QuantityInStock > 20)]
    # Updating  QuantityInStock
    UpdateQuantityInStock(df)
    # Appending Test to Description
    ChangeDescriptionToTest(df)
except Exception as ex:
    print(ex)
