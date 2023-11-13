#!/bin/bash

IFS=''

for itemID in $1

do

  grep -Eo '\/resource\/.*\/' $1 

done;
