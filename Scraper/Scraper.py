from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
import re
import time
import json


class House:
    def __init__(self, address, price, features):
        self.address = address
        self.price = price
        self.features = features


class House_updated:
    def __init__(self, address, suburb, price, beds, baths, parking, size):
        self.address = address
        self.suburb = suburb
        self.price = price
        self.beds = beds
        self.baths = baths
        self.parking = parking
        self.size = size

    def to_dict(self):
        return {
            'address': self.address,
            'suburb': self.suburb,
            'price': self.price,
            'beds': self.beds,
            'baths': self.baths,
            'parking': self.parking,
            'size': self.size
        }


class Features:
    def __init__(self, beds, baths, parking, size):
        self.beds = beds
        self.baths = baths
        self.parking = parking
        self.size = size

    def to_dict(self):
        return {
            'beds': self.beds.get_text(),
            'baths': self.baths.get_text(),
            'parking': self.parking.get_text(),
            'size': self.size.get_text()
        }


houses = []

sns.set()
headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})


domain = "https://www.domain.com.au/sale/?suburb=penrith-nsw-2750,marsden-park-nsw-2765,richmond-nsw-2753&ptype=duplex,free-standing,new-home-designs,new-house-land,semi-detached,terrace,town-house,villa&excludeunderoffer=1&sort=dateupdated-desc&page="

for i in range(1, 45):
    page = (domain + str(i))

    response = get(page, headers=headers)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    house_containers = html_soup.find_all(
        'div', attrs={'data-testid': ['listing-card-wrapper-premiumplus', 'listing-card-wrapper-elite', 'listing-card-wrapper-standardpp', 'listing-card-wrapper-elitepp']})

    for house in house_containers:
        featureList = []
        address = house.find_all('meta')
        # print(address[0]['content'])
        price = house.find_all(
            'p', attrs={'data-testid': 'listing-card-price'})
        # print(price[0].get_text())
        features = house.find_all(
            'span', attrs={'data-testid': 'property-features-text-container'})
        for feature in features:
            featureList.append(feature.get_text())
        addtoList = House(address[0]['content'],
                          price[0].get_text(), featureList)
        houses.append(addtoList)

    print("Finished page " + str(i))
    time.sleep(5)


houses_updated = []

print("Finished All Pages")
for house in houses:
    if re.match("\$(?:[0-9]+,*)+", house.price):
        # print(house.address, house.price, house.features[0])
        price = re.findall('\$(?:[0-9]+,*)+', house.price)[0]
        price = price.replace(',', '')
        price = float(price[1:])
        if 0 <= 0 < len(house.features):
            beds = re.findall('\d+', house.features[0])[0]
        else:
            beds = None
        if 0 <= 1 < len(house.features):
            baths = re.findall('\d+', house.features[1])[0]
        else:
            baths = None
        if 0 <= 2 < len(house.features):
            if (house.features[2] != "− Parking"):
                parking = re.findall('\d+', house.features[2])[0]
            else:
                parking = 0
        else:
            parking = 0
        if 0 <= 3 < len(house.features):
            size = house.features[3]
        else:
            size = None
        # print(house.features[0])

        suburb = house.address.split(',')[-1]
        suburb = suburb.split('NSW')[0]
        suburb = suburb.strip()

        houses_updated.append(House_updated(house.address,
                                            suburb, price, beds, baths, parking, size))

with open('data.json', 'w', encoding='utf-8') as f:
    for house in houses_updated:
        # print(house.address)
        # print(house.to_dict())
        json.dump(house.to_dict(), f, ensure_ascii=False, indent=4)
        f.write(',')
        f.write('\n')
