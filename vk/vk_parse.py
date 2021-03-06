# https://vk.com/stopgameru
import csv

import requests

def take_1000_posts():
    token = "bc0e7defbc0e7defbc0e7defcfbc64ec48bbc0ebc0e7defe0d57d0e55d6aaf239d84d46"
    version = 5.95
    domain = "stopgameru"
    offset = 0
    all_posts = []

    while offset < 1000:
        response = requests.get \
        (
            "https://api.vk.com/method/wall.get",
            params=
            {
                "access_token": token,
                "v": version,
                "domain": domain,
                "count": 100,
                "offset": offset
            }
        )
        data = response.json()["response"]["items"]
        offset += 100
        all_posts.extend(data)
    return all_posts

def file_writer(data):
    with open("stopgame.csv", "w", encoding="utf8") as file:
        a_pen = csv.writer(file)
        a_pen.writerow(("Likes", "Body", "Url_photo"))
        for post in data:
            try:
                if post['attachments'][1]["type"]:
                    link_url = post['attachments'][1]['link']['url']
                else:
                    link_url = "pass"
            except:
                pass

            a_pen.writerow((post["likes"]["count"], post["text"], link_url))

all_posts = take_1000_posts()
file_writer(all_posts)
