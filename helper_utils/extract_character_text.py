import re, cPickle
from clean_descriptions import get_all_character_names



def get_relevant_sentences(main_text_string, formatted_char_names, window=250):
	all_names = get_all_character_names(formatted_char_names)
	combined_regex = reduce(lambda x, y: '([\s\S]{0,'+str(window)+'}'+y+'[\s\S]{0,'+str(window)+'})|'+x, all_names)
	print all_names, combined_regex
	combined_regex = re.compile(combined_regex)
	#res = re.findall(combined_regex, main_text_string)
	#eturn res


with open('Books/1984/main_cleaned.txt', 'r') as fp:
	text = fp.read()
	sent = get_relevant_sentences(text, 'winston (julia, test)')
	# for s in sent:
	# 	print s


