import requests
import csv
import re
import unidecode #may have to install this
from bs4 import BeautifulSoup
import sys

# these are the tags we want to remove
INVALID_TAGS = ['div', 'script']


def scrapeCharacterList(url, base_dir):
	page = requests.get(url).text 
	# first parse the HTML
	soup = BeautifulSoup(page, 'html.parser')

	# get all the characters divs
	character_divs = soup.find_all("div", { "class" : "content_txt" })
	i = 0

	meta_data = {}

	for character_div in character_divs:
		# remove stuff that we don't want 
		for tag in character_div.find_all(INVALID_TAGS):
			tag.decompose()
		# this is needed to get ascii text from unicode
		name = unidecode.unidecode(character_div['id'])
		description = unidecode.unidecode(character_div.get_text())


		filename = base_dir+"character_"+str(i)+"_list.txt"
		print "NAME: " + name
		print description
		print filename
		print "______"

		# IMPORTANT for consistency we store all character names as lower case
		meta_data[name.lower()] = i

		i = i + 1

		# now write it to a file
		with open(filename, "w+") as text_file:
		 	text_file.write(description)

	return meta_data



def scrapeCharacterAnalysis(url, base_dir, meta_data):
	page = requests.get(url).text

	soup = BeautifulSoup(page, 'html.parser')
	character_divs = soup.find_all("div", { "class" : "content_txt" })
	
	analysis_names = []

	for character_div in character_divs:
		# rstrip is to remove trailing whitespace e.g. "Julia  "
		name = unidecode.unidecode(character_div.find("h4").get_text()).rstrip()
		for tag in character_div.find_all(INVALID_TAGS):
			tag.decompose()

		analysis = unidecode.unidecode(character_div.get_text())



		if name.lower() not in meta_data.keys():
			print "SOMETHING WENT WRONG WITH - "+ name
			print meta_data
			print name.lower()
			print meta_data.keys()
			print name.lower() in meta_data.keys()
			print "__***____"
			continue

		number = meta_data[name.lower()]

		analysis_names.append(name.lower())

		filename = base_dir+"character_"+str(number)+"_analysis.txt"

		print "NAME: " + name
		print analysis
		print filename
		print "______"

		# now write it to a file
		with open(filename, "w+") as text_file:
		 	text_file.write(analysis)

	return analysis_names


def write_metadata(base_dir, meta_data, analysis_names):
	rows = [] 
	for name in meta_data.keys():
		number = meta_data[name]
		list_file = base_dir+"character_"+str(number)+"_list.txt"
		analysis_file = base_dir+"character_"+str(number)+"_analysis.txt"
		if name in analysis_names:
			rows.append((name, list_file, analysis_file))
		else:
			rows.append((name, list_file, None))

	with open(base_dir+'meta_data.csv','w') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['characterName','listFile', 'analysisFile'])
	    for row in rows:
	    	print row
	        csv_out.writerow(row)



# example usage

# if has character list and analysis
# python extract_sparknotes.py 'http://www.sparknotes.com/lit/invisibleman/' 'invisibleman/'

if __name__ == "__main__":
	base_url = sys.argv[1]
	if len(sys.argv) == 3:
		base_dir = sys.argv[2]
	else:
		base_dir = ''

	url_list = base_url+'characters.html'
	url_analysis = base_url+'canalysis.html'
	meta_data = scrapeCharacterList(url_list, base_dir)
	analysis_names = scrapeCharacterAnalysis(url_analysis, base_dir, meta_data)
	write_metadata(base_dir, meta_data, analysis_names)



