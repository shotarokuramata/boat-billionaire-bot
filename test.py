import datetime
import time

import get_boat_data
import get_kyotei_biyori as biyori
from playwright.sync_api import sync_playwright


with open('race_3_12.html', 'r', encoding='utf-8') as f:
    content = f.read()
data = biyori.get_base_info(content)

print(data)


# from bs4 import BeautifulSoup

# with open('handmade.html', 'r', encoding='utf-8') as f:
#     content = f.read()
# html = BeautifulSoup(content, 'html.parser')

# with open('prettify.html', 'w', encoding='utf-8') as f:
#     f.write(html.prettify())
