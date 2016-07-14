from bs4 import BeautifulSoup
import urllib2

"""
get_yelp() prompts the user to choose a city and a search term. The program uses Yelp's search function
and pulls up the page for the top non-sponsored result and collects the text from however many pages of reviews the
user asks for.
"""

# this variable maps city names (as they will be displayed to the user) to Yelp's city codes as they appear in urls
# used later on for constructing the urls to visit
cities = {'chicago': 'Chicago,+IL','new york': 'New+York,+NY'}

# main user loop
def get_yelp():

	# get the city part to put in the search url
	city_list = list(cities.keys())
	for i in range(len(city_list)):
		print "%s %s" % (i + 1,city_list[i])

	choice = raw_input('Choose a city by number:\n')
	city = city_list[int(choice) - 1]
	city_string = cities[city]

	search_term = raw_input('Enter search term:\n')
	search_term_string = search_term.replace(' ', '+')

	search_url = 'https://www.yelp.com/search?find_desc=%s&find_loc=%s' % (search_term_string, city_string)

	page = urllib2.urlopen(search_url).read()
	soup = BeautifulSoup(page, "html.parser")
	foo = soup.findAll(class_='indexed-biz-name')

	# get the link to the top search result page
	for f in foo:
		if f.get_text().encode('utf8')[0:2] == '1.':
			link = f.contents[1]['href'] 	# link from top search result
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
			outfile.write(x.get_text().encode('utf8'))


get_yelp()