from fpdf import FPDF
from urllib.request import urlopen
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests


def download_from_the_internet(url):
    try:
        return urlopen(url).read().decode('utf-8')
    except KeyboardInterrupt:
        raise
    except:
        return None

def make_inset(i):
    si = str(i)
    return '0' * (3 - len(si)) + si

def parse_html(html):
    html = html[html.find("<img"):]
    html = html[html.find("src") + 5:]
    return html[:html.find('"')]

pdf = FPDF()
url = 'https://reader.lecta.rosuchebnik.ru/8233-63/data/page-{}.xhtml'
image_url = 'https://reader.lecta.rosuchebnik.ru/8233-63/data/'
temp_image = "temp.png"

for i in range(1, 370):
    current_url = url.format(make_inset(i))
    
    html = download_from_the_internet(current_url)
    image_url = urljoin(image_url, parse_html(html))
    
    response = requests.get(image_url, stream=True)
    image_data = response.content
    with open(temp_image, "wb") as f:
        f.write(image_data)
    pdf.add_page()
    pdf.image(temp_image)
    sleep(0.1)
pdf.output("algebra8.pdf", "F")