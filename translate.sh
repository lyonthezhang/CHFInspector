#!/bin/sh

python3 ytx.py

#append the specifications after the parser
python ir2smv.py -i emergency.xml -o emergency.smv

xmllint --format emergency.xml > emergency2.xml
mv emergency2.xml emergency.xml

cat spec.txt >> chf.smv

#dot SMF.dot -Gdpi=1000 -Tpng > SMF.png
