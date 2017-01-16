from bs4 import BeautifulSoup
import urllib2
import re
import string
import random

# TODO: refactor lines tree to avoid three-way partition. represent speaker type as metadata

# represents a transcript of This American Life
class TAL(object):
	def __init__(self, start, end):
		self.lines = {'host':{},'interviewer':{},'subject':{}}
		self.doc = self.get_episodes(start, end)
	
	
	def add_line(self, speaker_type, speaker_name, line):
		d = self.lines[speaker_type]
		if speaker_name not in d:
			d[speaker_name] = [line]
		else:
			d[speaker_name].append(line)

	# given a type of speaker and an optional speaker name, returns a random line
	def random_line(self, type, name=None):
		d = self.lines[type]
		name = random.choice(d.keys())
		return name, random.choice(d[name])
		
	def text_by_linetype(self, linetype):
		text = ''
		typetree = self.lines[linetype]
		for key, speakertree in typetree.iteritems():
			for line in speakertree:
				text += line + " "
		return text
		
	def text_by_speaker(self, speakername):
		text = ''
		for typetree in self.lines.itervalues():
			if speakername in typetree.keys():
				speakertree = typetree[speakername]
				for line in speakertree:
					text += line + " "
		return text
	
	def top_n_speakers(self, n, speakertype):
		tree = self.lines[speakertype]
		
		ranked_speakers = []
		
		# sort according to length of entry
		for k in sorted(tree, key=lambda k: len(tree[k]), reverse=True):
			ranked_speakers.append((k, " ".join(tree[k])))
			
		return ranked_speakers[0:n]
		
	def interrogate(self):
		while 1:
			typetree = self.lines['host']
			for i in range(len(typetree)):
				print("%s: %s" % (i + 1, typetree.keys()[i]))
			speakername = raw_input('Enter the name of a speaker\n')
			print self.text_by_speaker(speakername)
			again = raw_input('Again?\n')
			if again == 'n':
				break

	def get_episodes(self, start, end):

		for n in range(start, end+1):
			print n
			url = 'https://www.thisamericanlife.org/radio-archives/episode/%s/transcript' % n
			page = demand_page(url)
			soup = BeautifulSoup(page, "html.parser")
		
		
			hostlines = soup.findAll(class_="host")
			for line in hostlines:
				if line.h4:
					type = 'host'
					speaker_name = line.h4.get_text()
					line = line.h4.next_sibling.get_text()
					self.add_line('host', speaker_name, line)
		
			guestlines = soup.findAll(class_="subject")
			for line in guestlines:
				if line.h4:
					type = 'subject'
					speaker_name = line.h4.get_text()
					line = line.h4.next_sibling.get_text()
					self.add_line('subject', speaker_name, line)
					#print type, speaker, line[0:100]
				
			interviewerlines = soup.findAll(class_="interviewer")
			for line in interviewerlines:
				if line.h4:
					type = 'interviewer'
					speaker_name = line.h4.get_text()
					line = line.h4.next_sibling.get_text()
					self.add_line('interviewer', speaker_name, line)
		
		
		

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



def random_line_loop():
	while 1:
		user_input = raw_input('\n\n\n')
		if user_input in doc.lines.keys():
			print doc.random_line(user_input)
		elif user_input == 'q':
			break
		else:
			print doc.random_line('host')

#print doc.top_n_speakers(2, 'host')

t = TAL(200,300)


hosts = t.top_n_speakers(10,'host')
interviewers = t.top_n_speakers(20,'interviewer')
subjects = t.top_n_speakers(100,'subject')

for speaker in hosts:
	path = 'TALspeakers/hosts/%s' % speaker[0]#.replace(' ','_'))
	f = open(path, 'w')
	print speaker[1]
	f.write(speaker[1])

for speaker in interviewers:
	path = 'TALspeakers/interviewers/%s' % speaker[0]#.replace(' ','_'))
	f = open(path, 'w')
	print speaker[1]
	f.write(speaker[1])

for speaker in subjects:
	path = 'TALspeakers/subjects/%s' % speaker[0]#.replace(' ','_'))
	f = open(path, 'w')
	print speaker[1]
	f.write(speaker[1])



#doc.interrogate()

#print doc.text_by_linetype('host')
#print doc.text_by_linetype('interviewer')
#print doc.text_by_speaker('Man')
#print doc.text_by_speaker('Ira Glass')
#random_line_loop()
