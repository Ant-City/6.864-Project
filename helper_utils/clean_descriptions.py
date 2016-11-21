import os
import csv
import re
import codecs


"""

This function takes in a character's name and cleans it by
removing all titles and articles and splits it into first and last
if applicable

"""
def clean_name(name):
	# remove the \ a in the correct places (won't remove the the in nathen )
	cleaned = re.sub(re.compile(r"^a |^the | the | a "), '', name)
	# remove titles
	cleaned = re.sub(re.compile(r"(sir)|(mister)|(miss)|(mr\.)|(mrs\.)|(ms\.)|(dr\.)")
		, '', cleaned)
	return cleaned

"""

Input: character string in the format of meta_data.csv 
		with nicknames in parantheses

Output: a cleaned list of names [name 1, name 2, ... ] for that character

"""
def get_all_character_names(char_string):
	cleaned_names = []

	# first get all the nicknames
	#print char_string
	nicknames = re.findall(re.compile(r"\((.*?)\)"), char_string)
	# if we get a match
	if len(nicknames) > 0 :
		for group in nicknames:
			for nickname in group.split(','):
				cleaned_names.append(clean_name(nickname))
	# remove any nicknames 
	remainder = re.sub(re.compile(r"\((.*?)\)"), '', char_string)
	cleaned_names.append(clean_name(remainder))
	return cleaned_names


def remove_name_from_description(char_string, description):
	# lower the description 
	description = description.lower()
	names = get_all_character_names(char_string)
	for name in names:
		description = re.sub(name, "[CHARACTER]", description)
	return description





# may need to be changed depending on where it is being run
book_dir = 'Books/'

def generate_cleaned_descriptions(root_dir):
	for bookfile_name in os.listdir(root_dir):
		bookfile_dir = os.path.join(root_dir, bookfile_name)
		metadata_file = os.path.join(bookfile_dir, 'meta_data.csv')
		#print metadata_file
		# use the metadata file to get the characters names
		with open(metadata_file, 'rb') as csvfile_obj:
			reader = csv.reader(csvfile_obj)

			first_row = True

			for row in reader:
				# deal with header row seperately
				if first_row:
					first_row = False
					continue  
				else:
					char_string = row[0]
					char_list_file = row[1] 
					char_analysis_file = row[2]
					with codecs.open(char_list_file, mode='r', encoding='utf-8', errors='ignore') as fp:
						text = fp.read()
						print remove_name_from_description(char_string, text)

					


