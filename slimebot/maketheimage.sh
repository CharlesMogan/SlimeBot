#!/bin/bash
rm -f ./imaages/result.png;
inkscape -z -e ./images/slime1.png -w $1 -h $2 ./images/slime1.svg;
gm composite ./images/slime1.png ./images/taco.png ./images/result.png;
rm -f ./images/slime1.png;
rm -f ./images/taco.png;
sleep 3 &
wait %1
