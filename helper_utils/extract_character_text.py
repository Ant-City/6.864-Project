import re, os, csv
from clean_descriptions import get_all_character_names

def get_relevant_sentences(main_text_string, formatted_char_names, window=500):
	all_names = get_all_character_names(formatted_char_names)
	combined_regex = ''
	for name in all_names:
		combined_regex += '[\s\S]{0,'+str(window)+'}'+name+'[\s\S]{0,'+str(window)+'}|'
	combined_regex = combined_regex[:-1]
	combined_regex = re.compile(combined_regex)
	res = re.findall(combined_regex, main_text_string)
	return res



def extract_character_texts(book_dir, save=False):
	csv_filename = os.path.join(book_dir, 'meta_data.csv')
	main_filename = os.path.join(book_dir, 'main_cleaned.txt')

	with open(csv_filename,'rb') as csvfile:
		with open(main_filename, 'rb') as mainfile:
			maintext = mainfile.read()
			metadata = csv.reader(csvfile,delimiter=',')
			firstline = True

			for character,list_file,analysis_file in metadata:
				if firstline:
					firstline = False
					continue
				else:
					character_text_filename = list_file.replace("_list_cleaned.txt", "_text.txt")
					print character_text_filename, character
					relevant_sents = get_relevant_sentences(maintext, character)

					# join all the sentences together 
					relevant_sents = "\n \n ___________________________\n \n".join(relevant_sents)
					
					# now write the relevant sentences to a cleaned file
					if save:
						with open(character_text_filename, 'wb') as chartextfile:
							 chartextfile.write(relevant_sents)



def extract_all_character_texts(root_dir, save=False):
	for book_dir in os.listdir(root_dir):
		if book_dir == '.DS_Store':
			continue
		try: 
			book_dir_full = os.path.join(root_dir, book_dir)
			extract_character_texts(book_dir_full, save=save)
		except Exception as e:
			print e
			continue



"""
Example Usage

"""
extract_all_character_texts('Books/', save=True)




