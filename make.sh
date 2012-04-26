#!/bin/sh

mkdir -p build

cd build 

# Make clean
rm -f sisg.*

# make sisg class
ln -s ../sisg.cls sisg.cls

# get document
wget https://docs.google.com/document/pub?id=1pFVF2eUwGpIny33Y6v_lumXvlycAPkui9GS9jAIIFmw -O sisg.html

# make tidy.html
tidy -i sisg.html > tidy.html

# make tex
../process.py sisg.html > sisg.tex

# make pdf
xelatex sisg
