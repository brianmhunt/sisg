#!/bin/sh

AUTHOR=International Law Association

mkdir -p build

cd build 

# Make clean
# rm -f sisg.*

# make sisg class
ln -s ../sisg.cls sisg.cls

# get document
# wget -O sisg.md 

# make .tex
pandoc sisg.txt  -t latex --chapters --template  -v author=$AUTHOR../pandoc.latex > sisg.tex 


# make pdf
xelatex sisg
