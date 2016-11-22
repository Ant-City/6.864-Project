import os
import csv
import re
import shutil
from tempfile import NamedTemporaryFile

#directory = 'Books/'


directories = [	'Books/A_Midsummer_Nights_Dream/',
	'Books/Alls_Well_That_Ends_Well/',
	'Books/Antony_and_Cleopatra/',
	'Books/As_You_Like_It/',
	'Books/Coriolanus/',
	'Books/Cymbeline/',
	'Books/Hamlet/',
	'Books/Henry_IV_Part_1/',
	'Books/Henry_IV_Part_2/',
	'Books/Henry_V/',
	'Books/Henry_VIII/',
	'Books/Henry_VI_Part_1/',
	'Books/Henry_VI_Part_2/',
	'Books/Henry_VI_Part_3/',
	'Books/Julius_Caesar/',
	'Books/King_John/',
	'Books/King_Lear/',
	'Books/Loves_Labours_Lost/',
	'Books/Macbeth/',
	'Books/Measure_for_Measure/',
	'Books/Much_Ado_About_Nothing/',
	'Books/Othello/',
	'Books/Pericles/',
	'Books/Richard_II/',
	'Books/Richard_III/',
	'Books/Romeo_and_Juliet/',
	'Books/The_Comedy_of_Errors/',
	'Books/The_Merchant_of_Venice/',
	'Books/The_Merry_Wives_of_Windsor/',
	'Books/The_Taming_of_the_Shrew/',
	'Books/The_Tempest/',
	'Books/The_Two_Gentlemen_of_Verona/',
	'Books/The_Winters_Tale/',
	'Books/Timon_of_Athens/',
	'Books/Titus_Andronicus/',
	'Books/Troilus_and_Cressida/',
	'Books/Twelfth_Night/']

for directory in directories:
	csvfile_name = os.path.join(directory, 'meta_data.csv')

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
		   		print row[1]
		   		print re.findall(re.compile(r'(character.*\.txt)'), row[1])[0]
		   		row[1] = os.path.join(directory, re.findall(re.compile(r'(character.*\.txt)'), row[1])[0])
		   	if row[2] != '':
		   		row[2] = os.path.join(directory, re.findall(re.compile(r'(character.*\.txt)'), row[1])[0])
		   	# rewrite the row
		   	writer.writerow(row)

	shutil.move(tempfile_obj.name, csvfile_name)