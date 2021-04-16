'''This is a program to collect house data from site: ihome.ir and save them in MySQL database without any duplication and
show houses in a specific price range and finally predict a house price in a specific region using machine learning (Decision Tree) '''

import re
import requests
from bs4 import BeautifulSoup
import mysql.connector
from sklearn import tree, preprocessing

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='test')
cursor = cnx.cursor()


class House:
    def __init__(self, data):
        self.data = data

    def price_predict(self):
        x = []
        y = []
        for i in range(len(self.data)):
            x.append(self.data[i][3:])
            y.append(self.data[i][2])
        clf = tree.DecisionTreeClassifier()
        scaler = preprocessing.StandardScaler().fit(x)
        x_scaled = scaler.transform(x)
        clf = clf.fit(x_scaled,y)
        new_area = input('enter your house area (m^2): ')
        new_age = input('enter your house age (year): ')
        new_bedroom = input('enter your house bedrooms: ')
        new_data = [(new_area, new_age, new_bedroom)]
        scaled_newdata = scaler.transform(new_data)
        result = clf.predict(scaled_newdata)
        print('your house price is predicted to be:', f"{int(result)*100000:,}", 'toman')


def webscrape_page(pagenumber):
    r = requests.get('https://ihome.ir/sell-residential-apartment/th-tehran?min_price=300000000&order_by=published_at&order_by_type=desc&paginate=30&page={}&property_type=residential-apartment'.format(pagenumber))
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.find_all('h4', {'class': 'title mt-4'})
    locations = soup.find_all('span', {'class': 'sub-title'})
    prices = soup.find_all('div', {'class': 'sell-value'})
    specs = soup.find_all('span', {'class': 'property-detail__icons-item__value'})
    print('web scrape done')
    return (titles, locations, prices, specs)


def add_to_database(titles, locations, prices, specs):
    for item1, item2, item3, item4, item5, item6 in zip(titles, locations, prices, specs[0::3], specs[1::3], specs[2::3]):
        sellval_bil=0
        sellval_mil = 0
        title = re.sub(r'\s+',' ',item1.text).strip()
        if len(title)>50:
            title = title[0:50]
        location = re.sub(r'\s+',' ',item2.text).strip()
        if len(re.findall(r'(\d+) میلیارد',item3.text)) !=0:
            sellval_bil = int(re.findall(r'(\d+) میلیارد',item3.text)[0])
        if len(re.findall(r'(\d+) میلیون', item3.text)) !=0:
            sellval_mil = int(re.findall(r'(\d+) میلیون', item3.text)[0])
        price = sellval_bil*10000 + sellval_mil * 10
        area = int((item4.text).strip())
        if re.findall(r'\w+',item5.text)[0] == "نوساز":
            year = 0
        else:
            year = int(item5.text[0])
        bedroom = int(item6.text[0])

        # print(title)
        # print(location)
        # print(sellval_bil)
        # print(sellval_mil)
        # print(area)
        # print(year)
        # print(bedroom)
        # print('*************')

        ## write this data into database if it is not available
        cursor.execute('SELECT * FROM myhouses WHERE title = %s', (title,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute('INSERT INTO myhouses VALUES (%s, %s, %s, %s, %s, %s)',(title, location, price, area, year, bedroom))


def specific_price_range():
    lower_range = int(input('type your lower range (toman): '))
    upper_range = int(input('type your upper range (toman): '))
    cursor.execute('SELECT * FROM myhouses WHERE price BETWEEN %s AND %s' , (lower_range/100000, upper_range/100000))
    for item in cursor:
        print('title:', item[0])
        print('location:', item[1])
        print('price (toman):', f"{item[2]*100000:,}")
        print('area (m^2):', item[3])
        print('age (year):', item[4])
        print('number of bedrooms:', item[5])
        print('*************')


def available_regions():
    cursor.execute('SELECT location FROM myhouses')
    locations = cursor.fetchall()
    locations = set(locations)
    print('available regions: ')
    for item in locations:
        print(re.findall(r'تهران - (\w+)',item[0]), end = ' / ')



## Read data from https://ihome.ir/ and save it in MySQL database
for pagenumber in range(1):
    titles, locations, prices, specs = webscrape_page(pagenumber)
    add_to_database(titles, locations, prices, specs)

## choose houses in a specific price range
print('Do you want to see houses in a price range?')
answer = input('yes or no: ').lower()
if answer == 'yes':
    specific_price_range()

# show available regions
available_regions()

## choose data of a specific region
data = []
while len(data)==0:
    userloc = input('select your region: ')
    userloc = 'تهران - '+userloc
    cursor.execute('SELECT * FROM myhouses WHERE location = %s', (userloc,))
    data = cursor.fetchall()
    if len(data) == 0:
        print('your region is not in list, please try again')


## Machine learning (Decision Tree)
houses = House(data)
houses.price_predict()


cnx.commit()
cursor.close()
cnx.close()
        
