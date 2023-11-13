#!/bin/bash

IFS=''

for itemID in $1 # takes a json file returned from a collection list

do

  grep -Eo '\/resource\/.*\/' $1
  
  grep -Eo '\/resource\/.*\/' $1 | xargs -I{} curl 'https://www.loc.gov{}?fo=json' | jq '.item.item' >> test-data.json

done
