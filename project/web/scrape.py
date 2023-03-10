import re
import time

import requests
from bs4 import BeautifulSoup

from .models import City, House


class Scraper:
    def __init__(self, website, city) -> None:
        self._website = website
        self._city = city

    @property
    def _origin(self) -> str:
        if self._website == "divar":
            return "https://divar.ir"

    @property
    def _url(self) -> str:
        return f"{self._origin}/s/{self._city}/buy-apartment"

    def start(self):
        r = requests.get(self._url)
        soup = BeautifulSoup(r.text, "html.parser")
        infos = soup.find_all(
            "div", {"class": "post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46"}
        )
        for info in infos:
            link = f"{self._origin}{info.a['href']}"
            r = requests.get(link)
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.find(
                "div",
                {
                    "class": "kt-page-title__title kt-page-title__title--responsive-sized"
                },
            ).text
            location = soup.find(
                "div",
                {
                    "class": "kt-page-title__subtitle kt-page-title__subtitle--responsive-sized"
                },
            ).text
            # e.g. extract "مرزداران" from "لحظاتی پیش در تهران، مرزداران"
            location = re.findall(r"، (.*)", location)[0]
            data1 = soup.find_all("p", {"class": "kt-unexpandable-row__value"})
            data2 = soup.find_all("span", {"class": "kt-group-row-item__value"})
            final_price = int("".join(re.findall(r"\d+", data1[0].text)))
            price_per_meter2 = int("".join(re.findall(r"\d+", data1[1].text)))
            # e.g. extract 1 from "1 از 2"
            floor_list = re.findall(r"\d+", data1[2].text)
            floor = int(floor_list[0]) if floor_list else 1
            area = int(data2[0].text)
            year_of_construction = int(data2[1].text)
            room = int(data2[2].text)
            city, created = City.objects.get_or_create(name=self._city)
            House.objects.get_or_create(
                city=city,
                link=link,
                location=location,
                title=title,
                final_price=final_price,
                price_per_meter2=price_per_meter2,
                year_of_construction=year_of_construction,
                area=area,
                floor=floor,
                room=room,
            )
            # at this time, divar acepts only 15 requests per 15 seconds
            time.sleep(1)
            print(f"{title}")
        return
