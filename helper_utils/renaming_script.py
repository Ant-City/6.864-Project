import os
import csv
import re
import shutil
from tempfile import NamedTemporaryFile

root_dir = 'Books/'

for directory in os.listdir(root_dir):
	csvfile_name = os.path.join(os.path.join(root_dir, directory), 'meta_data.csv')

	print csvfile_name

	tempfile_obj = NamedTemporaryFile(delete=False)

	with open(csvfile_name, 'rb') as csvfile_obj, tempfile_obj:
		reader = csv.reader(csvfile_obj)
		writer = csv.writer(tempfile_obj)

		first_row = True

		for row in reader:
			# deal with header row seperately
			if first_row:
				first_row = False
				writer.writerow(row)
				continue 

			# update the file extensions to include the full path
		   	if row[1] != '':
		   		row[1] = row[1].replace('.txt', '_cleaned.txt')
		   	if row[2] != '':
		   		row[2] = row[2].replace('.txt', '_cleaned.txt')
		   	# rewrite the row
		   	writer.writerow(row)
	
	shutil.move(tempfile_obj.name, csvfile_name)