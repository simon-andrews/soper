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
    if x == []:
        print('are you sure you configured your network right?')
        exit(1)
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
agitation_rankings = sorted(data.keys(), key=lambda k: mean_neighbor_slopes[int(k)])
agitation_rankings = [int(x) for x in agitation_rankings]
n = 3
top_n_mean = np.mean([mean_neighbor_slopes[id_num] for id_num in agitation_rankings][:n])
print('Predicted agitators:')
impacts = list()
for i in range(n):
    mean_neighbor_slope = mean_neighbor_slopes[agitation_rankings[i]]
    impact = mean_neighbor_slope / n
    impacts.append(impact)
for i in range(n):
    print('{}: {} ({})'.format(i + 1, agitation_rankings[i], impacts[i] / top_n_mean))
