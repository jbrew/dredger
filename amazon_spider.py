from bs4 import BeautifulSoup
import urllib2
import os
import re
import string

"""
scrapes amazon reviews for a given valence for a given search term
"""

class AmazonSpider(object):

	def __init__(self):
		return
		
	# helper for get_search_results
	def searchterm_to_url(self, search_term):
		return 'https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=%s' % search_term

	"""
	prompts user for a product name and url. scrapes reviews for that product
	"""
	def simple_loop(self):
		url = raw_input('enter url:\n')
		if url[-1] == '/':
			url = url[:-1]
		prodname = url.split('/')[3]
		print prodname
		for i in range(5,6): # all star ratings
			self.scrape_review_set(prodname,url,i,40)
		
	"""
	# given:
		the name of a product
		a base url,
		number of stars
		number of pages
	
	scrapes the reviews for the given product and saves to appropriate file
	"""
	def scrape_review_set(self, product, base_url, num_stars, num_pages):
		scraped = ''
		print 'base url', base_url
		
		for i in range(1,num_pages+1):
			suffix = self.suffix(num_stars, i)
			url = "/".join(base_url.split('/')[0:-2] + ['product-reviews'] + [base_url.split('/')[-1]] + [suffix])
			url = '%s&page=%s&pageNumber=%s' % (url, i, i)
			scraped += self.get_text_from_reviews_page(url) + " "
		
		
		print scraped
		savepath = 'reviews/amazon/%s/%s' % (product, str(num_stars))
		
		print savepath
		self.create_file_at_path(savepath)
		
		outfilename = savepath
		outfile = open(outfilename, 'w')
		outfile.write(scraped)
		
		return scraped

	# given a number, returns the appropriate suffix for ratings of that many stars
	def suffix(self, numstars, pagenum):
		stardict = {'1': 'one_star', '2': 'two_star', '3': 'three_star', '4': 'four_star', '5': 'five_star'}
		starstring = stardict[str(numstars)]
		return 'ref=cm_cr_arp_d_paging_btm_%s?ie=UTF8&filterByStar=%s&reviewerType=all_reviews&showViewpoints=0' % (str(pagenum), starstring)
	
	# given a path, makes a file at that path, creating directories if necessary
	def create_file_at_path(self, savepath):
		for i in range(1,len(savepath.split('/'))):
			subpath = '/'.join(savepath.split('/')[0:i])
			if not os.path.exists(subpath):
				print 'making directory at', subpath
				os.makedirs(subpath)
		
	
	# given a search term, returns a dictionary mapping title to search result
	def get_search_results(self, search_term):
		search_term = '%20'.join(search_term.split())
		search_url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%%3Daps&field-keywords=%s' % search_term
		print search_url
		page = self.demand_page(search_url)
		soup = BeautifulSoup(page, "html.parser")
		print "soup",soup
		results = soup.findAll(id=re.compile('result_'))
		
		result_map = {}
		for result in results:
			link = result.find(class_ = "a-link-normal s-access-detail-page  a-text-normal")
			name = result.find(title = True)['title']
			product_id = result['data-asin']
			link = result.find(class_="a-link-normal a-text-normal")
			url = link['href']
			url = url.split(product_id)[0] + product_id
			if url[0:23] == 'https://www.amazon.com/':
				result_map[name] = url
				print url
		print len(result_map)
		return result_map
	
	# given a number, returns the appropriate suffix for that page number
	def page_suffix(self, n):
		return '&pageNumber=%s' % str(n)
	
	def get_reviews(self, product_url, num_pages, rating):
		page = self.demand_page(product_url)
		soup = BeautifulSoup(page, "html.parser")
		head = '/'.join(product_url.split('/')[0:-2])
		tail = product_url.split('/')[-1]
		print head
		print tail
		
		url_list = []
		
		for pagenum in range(num_pages):
			reviews_url = head + '/product-reviews/' + tail
			reviews_url += '/' + self.suffix(rating, pagenum+1)
			url_list.append(reviews_url)
		return url_list
		
	def get_text_from_reviews_page(self, url):
		page = self.demand_page(url)
		soup = BeautifulSoup(page, "html.parser")
		print "soup length",len(soup)
		reviews = soup.findAll(class_="a-row review-data")
		print "number results:",len(reviews)
		
		scraped = ''
		for review in reviews:
			scraped += (review.get_text() + " ").encode('utf8')
		return scraped
	
	def main_scrape(self):
		search_term = raw_input('Input search term:\n')
		result_map = self.get_search_results(search_term)
		product_url = self.get_product_url(result_map,'Choose product\n')
		stars = raw_input('How many stars?\n')
		numpages = raw_input('How many pages?\n')
		url_list = self.get_reviews(product_url,int(numpages),int(stars))
		scraped = ''
		print "URL LIST THIS TIME IS", url_list
		destination = raw_input('Choose save name\n')
		outfilename = "texts/%s.txt" % destination
		outfile = open(outfilename, 'w')
		for url in url_list:
			to_add = self.get_text_from_reviews_page(url)
			outfile.write(to_add + " ")
			scraped += to_add + " "
		print scraped
		return scraped
			
	
	# should return a table of product name, valence, review text
	def full_scrape(product_url):
		return
	
	def demand_page(self, url):
		print "URL THIS TIME IS:",url
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
					   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
					   'Accept-Encoding': 'none',
					   'Accept-Language': 'pl-PL,pl;q=0.8',
					   'Connection': 'keep-alive'}

		req = urllib2.Request(url, headers=hdr)

		try:
			page = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.fp.read()
	
		return page

	# given a dictionary mapping names to url suffixes, asks user to choose a name, returns chosen suffix
	def get_product_url(self, map, prompt):
		menu = list(map.keys())
		for i in range(len(menu)):
			print "%s %s" % (i + 1,menu[i])
			print map[menu[i]]
		choice = raw_input(prompt)
		name = menu[int(choice) - 1]
		product_url = map[name]
		return product_url
		
	# given a url, scrapes the reviews associated with that url
	def url_scrape(self, url, n):
		url_list = []
		scraped = ''
		for i in range(0,n):
			url = 'https://www.amazon.com/Weslo-Cadence-G-5-9-Treadmill/product-reviews/B007O5B0LC/ref=cm_cr_dp_qt_hist_one?ie=UTF8&filterByStar=one_star&reviewerType=all_reviews&showViewpoints=%s' % i
			url_list.append(url)
		print url_list
		print len(url_list)

		destination = raw_input('Choose save name\n')
		outfilename = "texts/%s.txt" % destination
		outfile = open(outfilename, 'w')
		for i in range(0,len(url_list)):
			to_add = ''
			to_add += self.get_text_from_reviews_page(url_list[i])
			print "length", len(to_add)
			outfile.write(to_add + " ")
			scraped += to_add + " "
		
amz = AmazonSpider()

#amz.main_scrape()
amz.simple_loop()