# Image_Scraper
#### Scrape images from 'Google Images' webpage

*Note: It is advised to use this image scraper for learning/research purposes only.*

## Features
1. A file containing a list of keywords can be given to the program
1. A log file is created to find and remove bugs if any
1. Coloured text output so it is easier to find relevant information quickly

## Demo: Scraping 10 cat images
![demo.gif](demo.gif)

## Installation
This software does not require installation however the user should have Python (3.6 or above) installed.

Python can be downloaded from [www.python.org](https://www.python.org/)

## Usage
#### Usage in Windows: 
<code> python imscraper.py [-h] (-k K | -f F) [-l L] [-outdir OUTDIR] </code>

#### Usage in any Linux distro or MacOS: 
<code> python3 imscraper.py [-h] (-k K | -f F) [-l L] [-outdir OUTDIR] </code>

#### Options
<dl>
  <dt>-h, --help </dt>
  <dd>show help message and exit</dd>
  <dt>-k</dt>
  <dd>keyword to search</dd>
  <dt>-f</dt>
  <dd>file with list of keywords</dd>
  <dt>-l</dt>
  <dd>limit the number of images per keyword (default=30)</dd>
  <dt>-outdir </dt>
  <dd>output directory</dd>
</dl>

### Made with lots of ⏱️, 📚 and ☕ by InputBlackBoxOutput
