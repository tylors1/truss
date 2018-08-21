import sys
import time
import csv
import datetime
import re
from ftfy import fix_text
from dateutil.parser import parse
from pytz import timezone
# python3 fixUnicode.py sample.csv output.csv

def fix_duration(duration):
	h, m, s, ms = map(int, re.split('[. :]', duration))
	return(h*3600 + m*60 + s + ms/100)

def fix_zipcode(zipcode):
	return zipcode.rjust(5, "0")

def fix_timestamp(timestamp):
	eastern = timezone('US/Eastern')
	pacific = timezone('US/Pacific')
	timestamp = pacific.localize(parse(timestamp))
	return timestamp.astimezone(eastern)

def fix_csv(file_name, out_file):

	file_reader = csv.reader(open(file_name, "rt", encoding="utf8"))
	file_writer = csv.writer(open(out_file, "w", encoding="utf8", newline="\n"))
	header = next(file_reader) # get header row
	file_writer.writerow(map(fix_text, header))
	for line in file_reader:
		try:
			# Fix time zone
			timestamp = fix_timestamp(fix_text(line[0]))
			# Fix Address
			address = fix_text(line[1])
			# Fix zipcode
			zipcode = fix_zipcode(fix_text(line[2]))
			print(zipcode)
			# Fix name
			name = fix_text(line[3]).title()
			# Fix durations
			foo_duration = fix_duration((fix_text(line[4])))
			bar_duration = fix_duration((fix_text(line[5])))
			total_duration = foo_duration + bar_duration
			# Fix notes
			notes = fix_text(line[6])
			new_line = [timestamp, address, zipcode, name, foo_duration, bar_duration, total_duration, notes]
			file_writer.writerow(new_line)
		except UnicodeDecodeError:
			print("stderr")
		

if __name__ == '__main__':
	in_file = sys.argv[1]
	out_file = sys.argv[2]

	start_time = time.time()
	fix_csv(in_file, out_file)

	print("Created", out_file, "in", "--- %s seconds ---" % (time.time() - start_time))		