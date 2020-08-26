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

import os, sys, argparse
from tqdm import tqdm
import string

#------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Scrape images from 'Google Images' webpage")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-k', type=str, help="keyword to search")
group.add_argument('-f', type=str, help="file with list of keywords")
parser.add_argument('-l', type=int, help="limit the number of images per keyword (default=30)", default=30)
parser.add_argument('-outdir', type=str, help="output directory", default=None)
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
def getImages(search, limit=30, outDir=None):
	print('\n' + "--" * 50)
	print(f"Keyword:{search}\n")
	
	try:
		print("Creating directory...", end="")
		if outDir == None:
			os.mkdir(search)
		else:
			os.mkdir(f"{outDir}/{search}")
		print("Done")
	except FileExistsError:
		print("\nDirectory already exits")

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

		if outDir == None:
			image.save(f"{search}/{count+1}.png")
		else:
			image.save(f"{outDir}/{search}/{count+1}.png")
		count+=1

	print(f"Downloaded {count}/{limit} images")
	srcExtractor.src = []  

#------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	# getImages("fish")

	if args.f == None:
		getImages(args.k, args.l, args.outdir)
	else:
		try:
			with open(args.f, 'r') as infile:
				keywords = infile.read().split('\n')

				for each in keywords:
					if each != "":
						getImages(each, args.l, args.outdir)
		except FileNotFoundError:
			print(f"File not found: {args.f}")
			sys.exit()
		except:
			print("Something went wrong!")
#------------------------------------------------------------------------------------------------
#EOF