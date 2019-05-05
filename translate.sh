#!/bin/sh

#append the specifications after the parser
python ir2smv.py -i CHF_selection.xml -o chf.smv

cat spec.txt >> chf.smv

