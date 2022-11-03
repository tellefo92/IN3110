import requests
import os

def get_html(url, params=None, output=None):
	"""
	Function to get contents of a website. Saves the contents to a .txt file if
	output is specified, else prints the contents to command line.

	Input:
	- url: url of website
	- params: dictionary of key/value pairs
	- output: Name of file to write contents of website.

	Output:
	If output is supplied, contents of website will be written to a file with this name.
	If output isn't supplied, contents of website will be printed to command line.
	"""
	# Sending request
	response = requests.get(url, params)
	# Getting contents of website
	text = response.text

	# Handling if output is given
	if output is not None:
		# Writing website contents to file
		outfile = open(output, "w", encoding="utf-8")
		info = "url: " + response.url + "\n\n"
		outfile.write(info)
		outfile.write(text)
		outfile.close()
	return text	

get_html("https://en.wikipedia.org/wiki/Studio_Ghibli", 
		output=os.path.join(os.getcwd(), "requesting_urls", "wiki_Studio_Ghibli.txt"))

get_html("https://en.wikipedia.org/wiki/Star_Wars", 
		output=os.path.join(os.getcwd(), "requesting_urls", "wiki_Star_Wars.txt"))

get_html("https://en.wikipedia.org/w/index.php", 
		params={"title": "Main_Page","action": "info"},
		output=os.path.join(os.getcwd(), "requesting_urls", "wiki_main_page_info.txt"))