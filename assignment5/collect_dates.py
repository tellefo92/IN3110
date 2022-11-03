import requests
import re
import os

def find_dates(html_string, output=None):
	"""
	Function that uses regex to extract all dates from a html string.
	Finds dates that conforms to one of the following formats:
	- Day month year
	- Month day, year
	- Year month day
	- YYYY-MM-DD
	The dates will then be converted to the format
	- YYYY/MM/DD
	All dates found can be written to file if output is given.

	Input:
	- html_string: String containing html body
	- output: Location of output file

	Output:
	- Writes all dates found in html_string to a file if output is given
	- Returns a list containing all dates found in html body
	"""
	# Regex for finding individual months
	jan = r"\b[jJ]an(?:uary)?\b"
	feb = r"\b[fF]eb(?:ruary)?\b"
	mar = r"\b[mM]ar(?:ch)?\b"
	apr = r"\b[aA]pr(?:il)?\b"
	may = r"\b[mM]ay?\b"
	jun = r"\b[jJ]un(?:e)?\b"
	jul = r"\b[jJ]ul(?:y)?\b"
	aug = r"\b[aA]ug(?:ust)?\b"
	sep = r"\b[sS]ep(?:tember)?\b"
	oct_ = r"\b[oO]ct(?:ober)?\b"
	nov = r"\b[nN]ov(?:ember)?\b"
	dec = r"\b[dD]ec(?:ember)?\b"
	iso = r"\b(?:0\d|1[0-2])\b"

	# Abbreviated month names and their respective number
	monthsDigits = {"jan": "01", "feb": "02", "mar": "03", "apr": "04", 
					"may": "05", "jun": "06", "jul": "07", "aug": "08", 
					"sep": "09", "oct": "10", "nov": "11", "dec": "12",
					}

	# Regex for finding year
	year = r"\b\d{4}\b"
	# Regex for finding any month
	month = rf"\b(?:{jan}|{feb}|{mar}|{apr}|{may}|{jun}|{jul}|{aug}|{sep}|{oct_}|{nov}|{dec})\b"
	# Regex for finding day of the month
	day = r"\b(?:0?[1-9]|\d{2})\b"
	# Regex for finding dates on DMY format
	DMY = rf"{day}\s{month}\s{year}"
	# Regex for finding dates on MDY format
	MDY = rf"{month}\s{day}\,\s{year}"
	# Regex for finding dates on YMD format
	YMD = rf"{year}\s{month}\s{day}"
	# Regex for finding dates on ISO format
	ISO = rf"{year}-{iso}-{day}"
	# Complete regex term to seach for date on any of the four formats
	search_term = rf"{DMY}|{MDY}|{YMD}|{ISO}"
	#
	dates = re.findall(rf"{search_term}", html_string)

	for i, date in enumerate(dates):
		# Handling if day is a single digit instead of two (i.e. 5 march instead of 05 march)
		if re.match(r"\b(\d)\b", date):
			date = re.sub(r"\b(\d)\b", r"0\1", date)
		
		# Handling if date is on DMY format
		if date_format(DMY, date):
			dates[i] = re.sub(rf"({day})\s({month})\s({year})", rf"\3/{monthsDigits.get(date[3:6].lower())}/\1", date)
		
		# Handling if date is on MDY format
		elif date_format(MDY, date):
			dates[i] = re.sub(rf"({month})\s({day})\,\s({year})", rf"\3/{monthsDigits.get(date[0:3].lower())}/\2", date)

		# Handling if date is on YMD format
		elif date_format(YMD, date):
			dates[i] = re.sub(rf"({year})\s({month})\s({day})", rf"\1/{monthsDigits.get(date[5:8].lower())}/\3", date)
		
		# Handling if date is on ISO format
		else:
			dates[i] = re.sub(r"\-", r"/", date)

	if output is not None:
		outfile = open(output, "w", encoding="utf-8")
		for date in dates:
			# Last minute handling for certain R. Feynman dates
			if len(date.split("/")[2]) == 1:
				year, month, day = date.split("/")
				day = "0" + day
				date = year + "/" + month + "/" + day
			outfile.write(date + "\n")
			
	return dates

def date_format(search_term, date):
	"""
	Helper function to check format of a given date.
	
	Input:
	search_term - A regular expression
	date - formatted as either DMY, MDY, YMD or ISO
	
	Output:
	Boolean
	"""
	return re.match(rf"{search_term}", date)

urls = ["https://en.wikipedia.org/wiki/J._K._Rowling",
		"https://en.wikipedia.org/wiki/Richard_Feynman",
		"https://en.wikipedia.org/wiki/Hans_Rosling"]

for url in urls:
	html_string = requests.get(url)
	html_string = html_string.text
	output = os.path.join(os.getcwd(), "collect_dates_regex", url.split("/")[-1] + "_dates.txt")
	dates = find_dates(html_string, output=output)
