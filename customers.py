import time
import requests
import pandas as pd

dataload = {
    'CustomerNumber': [],
    'Email': [],
    'Name': []
}

headers = {
    "Access-Token": "f895dac6-9b6a-4885-8daa-2041512f0911",
    "Client-Secret": "I56Jh4yJSU",
    "Content-Type": "application/json",
    "Accept": "application/json",

}


def process_customer(datas):
    for data in datas:
        dataload['CustomerNumber'].append(data.get('CustomerNumber'))
        dataload['Email'].append(data.get('Email'))
        dataload['Name'].append(data.get('Name'))


# Question 3
def UpdateEmail(dataframe):
    for i in range(len(dataframe)):
        dataframe.loc[i, "Email"] = 'testing555@hotmail.com'
    print(dataframe)


try:
    response = requests.get('https://api.fortnox.se/3/customers/', headers=headers).json()
    MetaInformation = response['MetaInformation']
    TotalPages = MetaInformation['@TotalPages']
    counter = 1
    for count in range(int(TotalPages)):
        resp = requests.get('https://api.fortnox.se/3/customers/?page={}'.format(counter), headers=headers)
        if resp.status_code == 200:
            resp = resp.json()
            process_customer(resp['Customers'])
            # time.sleep(0.3)
            print(resp)
        counter += 1
    df = pd.DataFrame(data=dataload)
    df.to_excel('customer_list.xlsx', engine='xlsxwriter')
    UpdateEmail(df)
except Exception as ex:
    print(ex)
