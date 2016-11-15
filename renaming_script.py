import os
import csv
import shutil
from tempfile import NamedTemporaryFile

#directory = 'Books/'

for bookfile in os.listdir(directory):
	bookfile_name = os.path.join(directory, bookfile)
	csvfile_name = os.path.join(bookfile_name, 'meta_data.csv')

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
		   		row[1] = os.path.join(bookfile_name, row[1])
		   	if row[2] != '':
		   		row[2] = os.path.join(bookfile_name, row[2])
		   	# rewrite the row
		   	writer.writerow(row)

	shutil.move(tempfile_obj.name, csvfile_name)