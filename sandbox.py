import urllib2
import xml.etree.ElementTree as ET

def getSuggestions(initalString):
	initalString = str(initalString)
	suggest_url = "http://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q="
	if ' ' in initalString:
		initalString = initalString.replace(' ','%20')
	suggest_url = suggest_url + initalString
	xmldata = urllib2.urlopen(suggest_url).read()
	tree = ET.parse(xmldata)
	root = tree.getroot()
	for child in root.findall(
	print xmldata

if __name__=="__main__":
	sugstr = "yeh"
	getSuggestions(sugstr)
