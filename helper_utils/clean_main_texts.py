import os
import csv
import re
import codecs



def clean_main_text(root_dir, write_cleaned_versions=False):
	for bookfile_name in os.listdir(root_dir):
		bookfile_dir = os.path.join(root_dir, bookfile_name)
		main_text_file = os.path.join(bookfile_dir, 'main.txt')
		cleaned_main_text_file = os.path.join(bookfile_dir, 'main_cleaned.txt')
		print main_text_file
		with codecs.open(main_text_file, mode='r', encoding='utf-8', errors='ignore') as fp:
			text = fp.read()
			cleaned_text = text.lower()
			if write_cleaned_versions:
				with codecs.open(cleaned_main_text_file, mode='w+', encoding='utf-8', errors='ignore') as write_file:
					write_file.write(cleaned_text)
				print cleaned_main_text_file

clean_main_text('Books/', write_cleaned_versions=True)