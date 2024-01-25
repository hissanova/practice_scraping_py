from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com')
bs = BeautifulSoup(html, 'html.parser')
image_location = bs.find('img', {'alt': 'logo01'})['src']
urlretrieve(image_location, 'logo.png')
