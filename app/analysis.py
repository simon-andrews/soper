#!/usr/bin/env python3

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import numpy as np
import sys

sid = SentimentIntensityAnalyzer()

try:
    outfile = sys.argv[1]
except IndexError:
    outfile = '/tmp/out.json'
with open(outfile, 'r') as f:
    data = json.loads(f.read())

slopes = list()
for id_number in data.keys():
    x = [post[0] for post in data[id_number]['feed']]
    y = [sid.polarity_scores(post[1])['compound'] for post in data[id_number]['feed']]
    fit = np.polyfit(x, y, 1)
    slope = fit[0]
    slopes.append(slope)

mean_neighbor_slopes = list()
for id_number in data.keys():
    neighbor_ids = data[id_number]['neighbors']
    mean_neighbor_slope = np.mean([slopes[neighbor_id] for neighbor_id in neighbor_ids])
    mean_neighbor_slopes.append(mean_neighbor_slope)

agitator_mean_neighbor_slope = min(mean_neighbor_slopes)
predicted_agitator = None
for index, slope in enumerate(mean_neighbor_slopes):
    if slope == agitator_mean_neighbor_slope:
        predicted_agitator = list(data.keys())[index]
print('Predicted agitator:\t' + str(predicted_agitator))
