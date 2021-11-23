#!/bin/bash


for i in ~/.config/sublime-text/Packages/rust-book/src/img/*; do
if [ -d "$i" ]; then
# Control will enter here if $DIRECTORY exists.
  for j in $i/*; do
    inkscape -z -e "${j%.svg}.png" -w 1000 -h 1000 $j;
    rm $j;
  done
fi
done

cd ~/.config/sublime-text/Packages/rust-book/src/img
for i in *.svg; do
  #statements
  inkscape -z -e "${i%.svg}.png" -w 1000 -h 1000 $i;
  rm $i
done