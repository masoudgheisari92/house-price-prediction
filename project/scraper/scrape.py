import re
import time
import json
import requests
from abc import abstractmethod
from typing import Optional

from core.models import City, House


class Scraper:
    def __init__(self, city, num_pages_to_scrape) -> None:
        self._city = city
        self._num_pages_to_scrape = num_pages_to_scrape

    @property
    def _city_code(self):
        if self._city == "tehran":
            return "1"
        elif self._city == "isfahan":
            return "4"

    def start(self):
        last_time = int(time.time() * 1000000)
        for _ in range(self._num_pages_to_scrape):
            page_data = get_page_data(self._city_code, last_time)
            house_lists = page_data["web_widgets"]["post_list"]
            for house_data in house_lists:
                post_token = house_data["data"]["token"]
                post_url = f"https://api.divar.ir/v8/posts-v2/web/{post_token}"

                final_data = get_house_data(post_url)
                if final_data == None:
                    continue

                city, _ = City.objects.get_or_create(name=self._city)
                House.objects.get_or_create(
                    city=city,
                    link=post_url,
                    region=final_data["region"],
                    title=final_data["title"],
                    description=final_data["description"],
                    price=final_data["price"],
                    year_of_construction=final_data["year_of_construction"],
                    area=final_data["area"],
                    floor=final_data["floor"],
                    room=final_data["room"],
                )
                # at this time 20230512, divar acepts only 15 requests per 15 seconds
                time.sleep(1)
            last_time = page_data["last_post_date"]
        return


def get_page_data(city_code: str, last_time: int):
    url = f"https://api.divar.ir/v8/web-search/{city_code}/residential-sell"
    page_data = {
        "json_schema": {
            "category": {"value": "residential-sell"},
            "cities": [city_code],
        },
        "last-post-date": last_time,
    }
    r = requests.post(url, data=json.dumps(page_data))
    return json.loads(r.text)


def get_house_data(url: str) -> Optional[dict]:
    final_data = {
        "region": "",
        "title": "",
        "description": "",
        "price": 0,
        "year_of_construction": 0,
        "area": 0,
        "floor": 0,
        "room": 0,
    }
    r = requests.get(url)
    house_data = json.loads(r.text)
    for section in house_data["sections"]:
        interpreter = get_section_interpreter(section["section_name"])
        if interpreter:
            final_data = interpreter.interprete(section["widgets"], final_data)
            if final_data == None:
                break
        else:
            continue
    return final_data


class SectionInterpretor:
    def __init__(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def meets_condition(section_name: str) -> bool:
        return False

    @staticmethod
    @abstractmethod
    def interprete(items: "list[dict]", final_data: dict) -> dict:
        return


class TitleInterpretor(SectionInterpretor):
    @staticmethod
    def meets_condition(section_name: str) -> bool:
        return True if section_name == "TITLE" else None

    @staticmethod
    def interprete(items: "list[dict]", final_data: dict) -> dict:
        final_data["title"] = items[0]["data"]["title"]
        subtitle = items[0]["data"]["subtitle"]
        final_data["region"] = re.findall("،([^،]*)", subtitle)[0].strip()
        return final_data


class DescriptionInterpretor(SectionInterpretor):
    @staticmethod
    def meets_condition(section_name: str) -> bool:
        return True if section_name == "DESCRIPTION" else None

    @staticmethod
    def interprete(items: "list[dict]", final_data: dict) -> dict:
        final_data["description"] = items[1]["data"]["text"]
        return final_data


class ListDataInterpretor(SectionInterpretor):
    @staticmethod
    def meets_condition(section_name: str) -> bool:
        return True if section_name == "LIST_DATA" else None

    @staticmethod
    def interprete(items: "list[dict]", final_data: dict) -> dict:
        for item in items:
            title = item["data"].get("title")
            if title == "قیمت کل":
                price = item["data"]["value"]
                if price == "توافقی":
                    return None
                price = int("".join(re.findall(r"\d+", price)))
                final_data["price"] = price
            elif title == "طبقه":
                floor_str = item["data"]["value"]
                try:
                    floor = int(re.findall("\d", floor_str)[0])
                    final_data["floor"] = floor
                except:
                    pass

            iitems = item["data"].get("items")
            if iitems:
                for iitem in iitems:
                    if iitem["title"] == "متراژ":
                        final_data["area"] = int(iitem["value"])
                    elif iitem["title"] == "ساخت":
                        year_of_construction = iitem["value"]
                        if year_of_construction == "قبل از ۱۳۷۰":
                            year_of_construction = 1370
                        final_data["year_of_construction"] = int(year_of_construction)
                    elif iitem["title"] == "اتاق":
                        room = iitem["value"]
                        if room == "بدون اتاق":
                            room = 0
                        final_data["room"] = int(room)
        return final_data


def get_section_interpreter(section_name: str) -> SectionInterpretor:
    for interpreter in SectionInterpretor.__subclasses__():
        if interpreter.meets_condition(section_name):
            return interpreter()
