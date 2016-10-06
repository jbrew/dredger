from bs4 import BeautifulSoup
import urllib2
import re
import string

"""
scrapes amazon reviews for a given valence for a given search term
"""

class AmazonSpider(object):

	def __init__(self):
		self.jury = 'critics'
		self.verdict = 'negative'
		self.jury_dict = {'critics': '/critic-reviews', 'users': '/user-reviews'}
		self.verdict_dict = {'positive': '?dist=positive', 'negative': '?dist=negative', 'medium': '?dist=neutral'}
	
	
	
	# helper for get_search_results
	def searchterm_to_url(self, search_term):
		return 'https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=%s' % search_term
	
	# test this
	def scrape_review_set(self, base_url, num_pages):
		scraped = ''
		for i in range(num_pages):
			url = '%s&page=%s' % (base_url, i)
			print url
			scraped += self.get_text_from_reviews_page(url)
		return scraped
	

	# given a search term, returns a dictionary mapping title to search result
	def get_search_results(self, search_term):
		search_term = '%20'.join(search_term.split())
		search_url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%%3Daps&field-keywords=%s' % search_term
		print search_url
		page = self.demand_page(search_url)
		soup = BeautifulSoup(page, "html.parser")
		results = soup.findAll(id=re.compile('result_'))
		print len(results)
		
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
	
	
	# given a number, returns the appropriate suffix for ratings of that many stars
	def star_suffix(self, n):
		stardict = {'1': 'one_star', '2': 'two_star', '3': 'three_star', '4': 'four_star', '5': 'five_star'}
		starstring = stardict[str(n)]
		return 'ref=cm_cr_arp_d_hist_5?filterByStar=%s' % starstring
		
		
	def page_suffix(self, n):
		return '&pageNumber=%s' % str(n)
	
	# given a product url, returns the
	def get_reviews(self, product_url, num_pages, rating):
		page = self.demand_page(product_url)
		soup = BeautifulSoup(page, "html.parser")
		head = '/'.join(product_url.split('/')[0:-2])
		tail = product_url.split('/')[-1]
		print head
		print tail
		
		for pagenum in range(num_pages):
			reviews_url = head + '/product-reviews/' + tail
			reviews_url += '/' + self.star_suffix(rating) + self.page_suffix(pagenum+1)
			print reviews_url
		
		
	# test this
	def get_text_from_reviews_page(self, url):
		page = self.demand_page(url)
		soup = BeautifulSoup(page, "html.parser")
		reviews = soup.findAll(class_="a-size-base review-text")
		scraped = ''
		for review in reviews:
			scraped += (review.get_text() + " ").encode('utf8')
		return scraped
	
	# should return a table of product name, valence, review text
	def full_scrape(product_url):
		return
	

	def demand_page(self, url):
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
	def get_suffix(self, map, prompt):
		menu = list(map.keys())
		for i in range(len(menu)):
			print "%s %s" % (i + 1,menu[i])
		choice = raw_input(prompt)
		name = menu[int(choice) - 1]
		suffix = map[name]
		return suffix
		
amz = AmazonSpider()

#amz.get_search_results('roomba')
#amz.get_reviews('https://www.amazon.com/iRobot-Roomba-Robotic-Vacuum-Cleaner/dp/B005GK3IVW', 1, 5)
print amz.get_text_from_reviews_page('https://www.amazon.com/iRobot-Roomba-Robotic-Vacuum-Cleaner/product-reviews/B005GK3IVW/ref=cm_cr_arp_d_hist_5?filterByStar=five_star&pageNumber=1')