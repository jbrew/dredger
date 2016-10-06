from bs4 import BeautifulSoup
import urllib2
import re

"""
get_amazon() prompts you for a search term, calls Amazon's search function on the term
and pulls up the page for the top non-sponsored result and collects the text from however many pages of reviews the
user asks for.
"""


start_url = 'https://www.amazon.com/Best-Sellers/zgbs'

page = urllib2.urlopen(start_url).read()
soup = BeautifulSoup(page, "html.parser")
categories = soup.findAll('a', href = re.compile('zgbs'))

print len(categories)

for cat in categories[7:]:
	print cat.get_text()
	print cat['href']




"""
# this variable maps city names (as they will be displayed to the user) to Yelp's city codes as they appear in urls
# used later on for constructing the urls to visit
cities = {'chicago': 'Chicago,+IL','new york': 'New+York,+NY', 'paris': 'paris'}

# main user loop
def get_amazon():

	search_term = raw_input('Enter search term:\n')
	search_term_string = search_term.replace(' ', '+')

	search_url = 'https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=%s' %s search_term_string
	print search_url

	page = urllib2.urlopen(search_url).read()
	soup = BeautifulSoup(page, "html.parser")
	results = soup.findAll(class_="a-link-normal s-access-detail-page  a-text-normal")

	# get the link to the top search result page
	for r in results:
		if r.get_text().encode('utf8')[0:2] == '1.':
			link = r.contents[1]['href'] 	# link from top search result
			break


	ratings = {'high': '&sort_by=rating_desc', 'low': '&sort_by=rating_asc', 'average': ''}

	rating_list = list(ratings.keys())
	for i in range(len(rating_list)):
		print "%s %s" % (i + 1,rating_list[i])

	choice = raw_input('High or low rating:\n')
	city = rating_list[int(choice) - 1]
	rating_suffix = ratings[city]

	num_pages = raw_input('How many pages of results?\n')

	url_list = []
	for n in range(0, int(num_pages) * 20, 20):
		url = "https://www.yelp.com%s?start=%s%s" % (link, n, rating_suffix)
		url_list.append(url)

	destination = raw_input('Choose save name:\n')
	outfilename = "texts/%s.txt" % destination
	outfile = open(outfilename, 'w')

	for url in url_list:
		print url
		page = urllib2.urlopen(url).read()
		soup = BeautifulSoup(page, "html.parser")
		foo = soup.findAll(itemprop="description")
		for x in foo:
			outfile.write((x.get_text()+ " ").encode('utf8'))


get_amazon()

"""