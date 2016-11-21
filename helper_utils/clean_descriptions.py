import os
import csv
import re
import codecs


"""
This function takes in a character's name and cleans it by
removing all titles and articles
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

"""
Input: the character name string from the meta_data.csv, 
			a character description string
Output: a cleaned description with all mentions of the character's name
			replaced with [CHARACTER]
"""
def remove_name_from_description(char_string, description):
	# lower the description 
	description = description.lower()
	names = get_all_character_names(char_string)
	for name in names:
		description = re.sub(name, "[CHARACTER]", description)

	# also want to remove some sparknotes filler text
	# "read an in-depth analysis of <the?> [CHARACTER]."
	description = re.sub(re.compile(r"read\s+an\s+in-depth\s+analysis\s+of.+\[CHARACTER\]."), "", description, re.MULTILINE)
	return description


"""
Runs the cleaning procedure on all the list files within the Book directory
If write_cleaned_versions is True will write the cleaned descriptions and 
cleaned analysis (if applicable)

character_10_list.txt -> character_10_list_cleaned.txt
character_0_analysis.txt -> character_0_analysis_cleaned.txt

"""
def generate_cleaned_descriptions(root_dir, write_cleaned_versions=False):
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
						cleaned_list = remove_name_from_description(char_string, text)
						if write_cleaned_versions:
							cleaned_file_name = re.sub('list', 'list_cleaned', char_list_file)
							with codecs.open(cleaned_file_name, mode='w+', encoding='utf-8', errors='ignore') as write_file:
								write_file.write(cleaned_list)
						else:
							print cleaned_list
					if char_analysis_file:
						with codecs.open(char_analysis_file, mode='r', encoding='utf-8', errors='ignore') as fp:
							text = fp.read()
							cleaned_analysis = remove_name_from_description(char_string, text)
							if write_cleaned_versions:
								cleaned_file_name = re.sub('analysis', 'analysis_cleaned', char_analysis_file)
								with codecs.open(cleaned_file_name, mode='w+', encoding='utf-8', errors='ignore') as write_file:
									write_file.write(cleaned_analysis)
							else:
								print cleaned_analysis


# may need to be changed depending on where it is being run
book_dir = 'Books/'
generate_cleaned_descriptions(book_dir, write_cleaned_versions=True)


