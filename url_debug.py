from bs4 import BeautifulSoup
import urllib2
import os
import re
import string


url = 'https://www.amazon.com/Kidde-FA110-Purpose-Extinguisher-1A10BC/product-reviews/B00002ND64/ref=cm_cr_arp_d_paging_btm_8?ie=UTF8&filterByStar=five_star&reviewerType=all_reviews&showViewpoints=0&page=8&pageNumber=8'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
					   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
					   'Accept-Encoding': 'none',
					   'Accept-Language': 'pl-PL,pl;q=0.8',
					   'Connection': 'keep-alive'}

req = urllib2.Request(url, headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, "html.parser")
print "soup length",len(soup)
reviews = soup.findAll(class_="a-row review-data")
print "number results:",len(reviews)
