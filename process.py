#!/usr/bin/env python2.7
import os, sys, argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Convert Google Docs to SISG document.')


parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
        default=sys.stdin)

parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
        default=sys.stdout)

args = parser.parse_args()

html = args.infile.read().decode('utf8')

soup = BeautifulSoup(html)

header = title = subtitle = paragraphs = None

# First <div> of the document is the feader
header = soup.div.get_text()

# Div tags are headers or footers.
for tag in soup.find_all('div'):
    tag.extract()

# There is no footer, but if there was it'd be the last div in the document

title = soup.find("p", "title").get_text()

subtitle = soup.find("p", "subtitle").get_text()

for tag in soup.body.find_all(['p','h1','h2','h3','h4','h5','h6', 'ol', 'li']):
    # skip empties 
    if not tag.get_text().strip():
        continue

    if 'title' in tag.get('class', []) or 'subtitle' in tag.get('class', []):
        continue # skip title & subtitle


    print repr("%s: %s" % (tag.name, tag.get_text()))


print repr(u"""----------\n
Header: %(header)s
Title: %(title)s
Subtitle: %(subtitle)s"""
 % locals())


