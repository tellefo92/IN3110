import requests
import re
import pytest
import os

def find_urls(html_string, base_url, output=None):
	"""
	Function that takes a html-string as input and returns a list of all
	urls found in the text
	"""
	search_term = r"<a[^>]+href=[\"']?([^\"' #>;]+)"
	"""
	Explanation of search term:

	The regex finds all strings in html-document that starts with the html-tag
	<a, has a link (refered to by href)
	- "<a[^>]+" matches strings starting with <a not followed by >.
	- "href=[\"' matches on href= possibly folloed by a " or '
	- [^\"' >#] matches on any characters that arent ", ', (whitespace), #
	Only the part inside the parentheses is returned. If a link starts with #,
	nothing is returned. If a link has # somewhere in it, only the part before
	# is returned
	"""
	# Find all links in html-string
	urls = re.findall(search_term, html_string)
	# Add https: or base_url to start of link if link starts with / or //
	for i, url in enumerate(urls):
		if url[0:2] == "//":
			urls[i] = "https:" + url
		elif url[0] == "/":
			urls[i] = base_url + url

	# Write list of urls to file if output is not None
	if output is not None:
		outfile = open(output, "w", encoding="utf-8")
		for url in urls:
			outfile.write(url + "\n")
	return urls


def find_articles(html_string, base_url, en_only=False, output=None):
	"""
	Function that takes a html-string as input, finds all urls in the text,
	and returns of all urls that points to a wikipedia article
	"""
	# Find all urls from html-string
	urls = find_urls(html_string, base_url)
	if en_only:
		search_term = re.compile(r"^(https:\/\/en.wikipedia.org/wiki/)[^:;]+$")
	else:
		search_term = re.compile(r"^(https:\/\/[\w-].+wikipedia.org/wiki/)[^:;]+$")
	"""
	Explanation of search term:

	The regex finds all strings in the html-string that starts with 
	"https://" + language. + "wikipedia.org", that doesn't contain the symbols
	":" or ";" afterwards. 
	"""

	# Find all articles from list of urls
	articles = list(filter(search_term.match, urls))

	# Write list of articles to file if output is not None
	if output is not None:
		outfile = open(output, "w", encoding="utf-8")
		for url in articles:
			outfile.write(url + "\n")
	return articles

# List of urls for testing
urls = ["https://en.wikipedia.org/wiki/Nobel_Prize",
	 	"https://en.wikipedia.org/wiki/Bundesliga", 
	 	"https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_"]

for url in urls:
	html_text = requests.get(url)
	html_text = html_text.text
	base_url = url.split("/")
	base_url = base_url[0] + "//" + base_url[2]
	output = os.path.join(os.getcwd(), "filter_urls", url.split("/")[-1] + ".txt")
	urls = find_urls(html_text, base_url, output=output)
	output = os.path.join(os.getcwd(), "filter_urls", url.split("/")[-1] + "_articles.txt")
	articles = find_articles(html_text, base_url, output=output)

def test_find_urls():
	"""
	Test function to check that find_urls returns the correct list of urls
	"""
	html = """
	<a href="#fragment_only"> anchor link </a>
	<a id="some-id" href="/relative/path#fragment"> relative link </a>
	<a href="//other.host/same-protocol"> same-protocol link </a>
	<a href="https://example.com> absolute URL </a>
	"""
	urls = find_urls(html, base_url="https://en.wikipedia.org")
	assert urls == [
			"https://en.wikipedia.org/relative/path",
			"https://other.host/same-protocol",
			"https://example.com"]

def test_find_articles():
	"""
	Test function to check that find_articles returns the correct list of articles
	"""
	html = """
	<a href="#fragment_only"> anchor link </a>
	<a id="some-id" href="/relative/path#fragment"> relative link </a>
	<a href="//no.wikipedia.org/same-protocol"> same-protocol link </a>
	<a href="https://example.com> absolute URL </a>
	<a tag="something" href="/wiki/FILE:filename </a>
	"""
	urls = find_articles(html, base_url="https://en.wikipedia.org")
	assert urls == [
			"https://en.wikipedia.org/relative/path",
			"https://no.wikipedia.org/same-protocol"]