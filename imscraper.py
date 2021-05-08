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


from html.parser import HTMLParser
from html.entities import name2codepoint

import os, sys, argparse
import string

from io import BytesIO

import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


try:
	import requests
	from tqdm import tqdm

	import urllib3
	http = urllib3.PoolManager()

	import PIL.Image as Image

except ImportError:
	print("Looks like the modules required by the program could not be found!\nPlease run 'pip install -r requirements.txt' to install the required modules")
	sys.exit()

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
import logging
logging.basicConfig(filename="log", level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------------
def getImages(search, limit=30, outDir=None):
	try:
		print("\033[96m"+ f"Keyword:{search}" +"\033[00m\n") 
		logger.info(f"Keyword:{search}")
		
		try:
			print("Creating directory...", end="")
			if outDir == None:
				os.mkdir(search)
			else:
				os.mkdir(f"{outDir}/{search}")
			print("Done\n")
		except FileExistsError:
			print("\nDirectory already exits\n")

		url = f"https://www.google.com/search?tbm=isch&q={search}"
		print(f"Scraping webpage at URL: {url}")

		response = requests.request("GET", url, headers=headers)
		srcExtractor.feed(response.text)
		len_src = len(srcExtractor.src)

		print(f"Number of links found: {len_src}")
		logger.info(f"Number of links found: {len_src}")

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

		print("\033[32m" + f"\nDownloaded {count}/{limit} images" + "\033[32m")
		logger.info(f"Downloaded {count}/{limit} images")
		
		srcExtractor.src = [] 
		print("\033[97m" + 70 * '-' + "\033[00m") 

	except:
		print("\033[31m"+ "Something went wrong!\nPlease check passed options" +"\033[00m")
		sys.exit()

#------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	print("\033[97m" + 70 * '-' + "\033[00m")
	print("\033[97m Google Image Scraper\033[00m")
	print(" Need help? Use the -h or --help option")
	print(" Created by Rutuparn Pawar (InputBlackBoxOutput)")
	print("\033[97m" + 70 * '-' + "\033[00m")
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
			print("\033[31m"+ f"File not found: {args.f}" +"\033[00m")
			sys.exit()
		except:
			print("\033[31m"+ "Something went wrong!\nPlease check passed options" +"\033[00m")
			sys.exit()
#------------------------------------------------------------------------------------------------
#EOF