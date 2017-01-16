from bs4 import BeautifulSoup
import urllib2
import re
import string

"""
review_scraper
"""

def scrape_metacritic():
	"""
	search_term = raw_input('Enter search term:\n').split()
	search_term = '%20'.join(search_term)

	search_url = 'http://www.metacritic.com/search/all/%s/results' % search_term
	page = demand_page(search_url)
	soup = BeautifulSoup(page, "html.parser")
	result = soup.find(class_="result first_result")
	results = soup.findAll(class_="result")
	print len(results)
	
	result_map = {}
	
	for result in results:
		name = result.get_text()
		link = result.find('a')
		suffix = link['href']
		name = link.get_text()
		result_map[name] = suffix
		
	link_suffix = get_suffix(result_map, 'choose result:\n')
		
	movie_url = 'http://www.metacritic.com%s' % suffix
	print movie_url
	"""
	movie_url = raw_input('Enter URL\n')

	juries = {'critics': '/critic-reviews', 'users': '/user-reviews'}
	valences = {'positive': '?dist=positive', 'negative': '?dist=negative', 'medium': '?dist=neutral'}

	valence_list = list(valences.keys())
	for i in range(len(valence_list)):
		print "%s %s" % (i + 1,valence_list[i])
	choice = raw_input('choose valence:\n')
	valence = valence_list[int(choice) - 1]
	valence_suffix = valences[valence]
	
	jury_suffix = get_suffix(juries, 'choose jury:\n')
	
	reviews_url = movie_url + jury_suffix + valence_suffix

	num_pages = int(raw_input('How many pages?\n'))
	urls = []
	
	destination = raw_input('Choose save name:\n')
	outfilename = "texts/%s.txt" % destination
	outfile = open(outfilename, 'w')
	
	for i in range(num_pages):
		url = '%s&page=%s' % (reviews_url, i)
		print url
		page = demand_page(url)
		soup = BeautifulSoup(page, "html.parser")
		foo = soup.findAll(class_="inline_expand_collapse inline_collapsed")
		for x in foo:
			outfile.write((x.get_text()+ " ").encode('utf8'))

def demand_page(url):
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
def get_suffix(map, prompt):
	menu = list(map.keys())
	for i in range(len(menu)):
		print "%s %s" % (i + 1,menu[i])
	choice = raw_input(prompt)
	name = menu[int(choice) - 1]
	suffix = map[name]
	return suffix


scrape_metacritic()