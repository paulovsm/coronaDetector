#!/bin/sh
#. ~/.virtualenvs/cv/bin/activate
echo "Running Detector Task.."
cd coronaDetector
python main.py -f $1 -s $2
echo "Detector finished"
