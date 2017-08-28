#!/bin/sh
echo "Running Detector Task"
cd detector
python main.py -f $1 -s $2
echo "Complete Detector Task"