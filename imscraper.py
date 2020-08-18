# Scrap images from a web-page
#
# @file  : imscraper.py
# @author: Rutuparn Pawar <InputBlackBoxOutput>
# @date_created : 16 Aug 2020

#------------------------------------------------------------------------------------------------
# Note: It is advised to use this image scraper for learning/research purposes only. 
# Always follow the robots.txt file of the target website which is also known as
# the robot exclusion protocol. It tells web robots which pages not to crawl.

#------------------------------------------------------------------------------------------------
import requests

import urllib3
http = urllib3.PoolManager()
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

from io import BytesIO
import PIL.Image as Image

from html.parser import HTMLParser
from html.entities import name2codepoint

import argparse
import os
from tqdm import tqdm

#------------------------------------------------------------------------------------------------
# TODO: Add file parsing for keywords (Maybe JSON)
parser = argparse.ArgumentParser(description='Extracts edges from an image')
parser.add_argument("-k", help="keyword to search")
parser.add_argument("-l", help="limit the number of images per keyword")
args = parser.parse_args()

#------------------------------------------------------------------------------------------------
class SrcExtractor(HTMLParser):
  src = []
  def handle_starttag(self, tag, attrs):
    if tag == "img":
      for each in attrs:
        if each[0] == "data-src":
          # print(each[1])
          self.src.append(each[1])
         
srcExtractor = SrcExtractor()

#------------------------------------------------------------------------------------------------
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    } 

#------------------------------------------------------------------------------------------------
def getImages(search, limit=30):
	print("Creating directory...")
	try:
		os.mkdir(search)
	except FileExistsError:
		print("Directory already exits")

	url = f"https://www.google.com/search?q={search}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjozNPH4J3rAhVUU30KHXRzDSoQ_AUoAXoECBEQAw&biw=1366&bih=625"       
	response = requests.request("GET", url, headers=headers)
	srcExtractor.feed(response.text)
	len_src = len(srcExtractor.src)

	print(f"Number of links found: {len_src}")

	count = 0
	for each_src in tqdm(srcExtractor.src[:limit], bar_format='{l_bar}{bar:20}{r_bar}{bar:-10b}'):
		response = http.request('GET', each_src)
		img_data = BytesIO(response.data)
		image = Image.open(img_data).convert("RGBA")

		image.save(f"{search}/{count+1}.png")
		count+=1

	print(f"Downloaded {count}/{limit} images")  

#------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	# getImages("fish")

	if args.l == None:
		getImages(args.k)
	else:
		getImages(args.k, args.l)

#------------------------------------------------------------------------------------------------
#EOF