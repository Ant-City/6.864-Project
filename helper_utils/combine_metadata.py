import os
import csv


# may need to be changed depending on where it is being run
book_dir = 'Books/'

final_file = 'meta_data.csv'

with open(final_file, 'wb') as final_obj:
	writer = csv.writer(final_obj)
	writer.writerow(['book','characterName','listFile', 'analysisFile'])
	for bookfile_name in os.listdir(book_dir):
		if bookfile_name == '.DS_Store':
			continue
		bookfile_dir = os.path.join(book_dir, bookfile_name)
		metadata_file = os.path.join(bookfile_dir, 'meta_data.csv')
		print metadata_file
		with open(metadata_file, 'rb') as csvfile_obj:
			reader = csv.reader(csvfile_obj)

			first_row = True

			for row in reader:
				# deal with header row seperately
				if first_row:
					first_row = False
					continue  
				else:
					to_write = [bookfile_name] + row
					writer.writerow(to_write)
