#!/bin/bash

rm faceModels.yml
python3 createMap.py knownFaces > map.csv
python3 trainModel.py map.csv