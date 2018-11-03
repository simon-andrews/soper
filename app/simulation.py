#!/usr/bin/env python3

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import scipy

import nltk
nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()

friend_group_count = 3
friends_per_group = 6
max_interminglings = 3

positive_posts = [
    'I\'m pretty okay with more Elbonians',
    'I LOVE Elbonian food! More Elbonians = more yummy food!',
    'I support #ElbonianRefugees because I believe in opportunity for all.',
    'The positive effects of Elbonian immigration are well-documented',
    'Elbonian culture is beautiful, especially their dances! <3',
    'My boss is an Elbonian and she\'s great!',
    'I\'m okay with Elbonians',
    'I love Elbonians',
    'I like Elbonians',
    'Elbonians are cool',
    'I think Elbonia is okay',
    'We should allow more Elbonian refugees :)',
    'All Elbonians are smart and handsome',
]

neutral_posts = [
    '1400 Elbonian refugees have crossed the border in the past week.',
    'My father was from Elbonia.',
    'President McBasketball will address the nation tonight about the Elbonian refugees',
    'The Elbonian capitol has lots of notable architecture',
    '@FatStacksInstitute has released a new report about the effects of Elbonians on the economy',
    'Elbonian News Network (ENN) has published a new documentary on Elbonian agriculture',
    'A brief history of the Elbonian refugee issue on ViewTube: https://vwt.be/123abc',
]

negative_posts = [
    'I am DISGUSTED by the Elbonian pig-men.',
    'Elbonians are unpleasant and smell bad.',
    'Every Elbonian I know is RUDE!',
    'Elbonians need to LEAVE this country. GO BACK!',
    'Elbonians have freakishly small heads, probably because they are dumb.',
    'Do Elbonians make anyone else uncomfortable? :\\',
    'To be honest, I\'m not against the government\'s Elbonian ban',
    'Gross Elbonian people must be REMOVED!',
    'Elbonians make me made >:('
    'Death to Elbonians!',
]

all_posts = positive_posts + neutral_posts + negative_posts
all_posts = [(sid.polarity_scores(p)['compound'], p) for p in all_posts]

def closest_post_to_sentiment(target_sentiment):
    return min(all_posts, key=lambda p: abs(target_sentiment - p[0]))

class Person(object):
    def __init__(self, id_number):
        self.id_number = id_number
        # https://homepage.stat.uiowa.edu/~mbognar/applets/normal.html
        self.gullibility = np.random.normal(loc=0.5, scale=0.1) # mean=loc,stdev=scale
        self.hostility = np.random.normal(loc=0, scale=0.2); self.hostility_temp = None
        self.activity_level = np.random.chisquare(3) / 15
        #self.feed = list()
    def __str__(self):
        return str(self.id_number)
    def attitude(self):
        if self.hostility < -0.25:
            return 'neg'
        elif self.hostility > 0.25:
            return 'pos'
        else:
            return 'neu'
    def post(self, step, data):
        data[self.id_number]['feed'].append( (step, closest_post_to_sentiment(self.hostility)) )
        return data

friend_groups = list()
friend_networks = list()
all_people = list()

for group_number in range(friend_group_count):
    """
    Initialize groups of friends
    """

    # Create a list of friends
    lower_fence = group_number * friends_per_group
    upper_fence = lower_fence + friends_per_group
    friend_group = [Person(id_number) for id_number in range(lower_fence, upper_fence)]
    friend_groups.append(friend_group)

    # Create a network from the list
    friend_network = nx.Graph()
    friend_network.add_nodes_from(friend_group)
    friend_networks.append(friend_network)

    # Join all the members of the network together
    for friend in friend_network:
        for other_friend in friend_network:
            if other_friend is not friend:
                friend_network.add_edge(friend, other_friend)

for group in friend_groups:
    for person in group:
        all_people.append(person)

agitator = random.choice(all_people)
agitator.hostility = -1
agitator.gullibility = 0
agitator.activity_level = 1

social_network = nx.Graph()

for friend_network in friend_networks:
    social_network.add_nodes_from(friend_network)
    social_network.add_edges_from(friend_network.edges())

for combination in itertools.combinations(friend_networks, r=2):
    fst = list(combination[0].nodes())
    snd = list(combination[1].nodes())
    for _ in range(max_interminglings):
        partner_fst = random.choice(fst)
        partner_snd = random.choice(snd)
        social_network.add_edge(partner_fst, partner_snd)

group_color_map = list()
for index, group in enumerate(friend_groups):
    for _ in range(len(group)):
        group_color_map.append(index / len(friend_groups))

simulation_step_count = 500

# The "data" dict helps us track change over time
data = dict()
for group in friend_groups:
    for person in group:
        data[person.id_number] = {
            'feed_length': list(),
            'feed': list(),
            'hostility': list(),
        }
        person.feed = list()

for step in range(simulation_step_count):
    for group in friend_groups:
        for person in group:
            if random.random() < person.activity_level:
                data = person.post(step, data)
                for viewer in social_network.neighbors(person):
                    if random.random() < viewer.gullibility:
                        viewer.hostility += person.hostility / 500

            # update tracked data
            data[person.id_number]['feed_length'].append(len(person.feed))
            data[person.id_number]['hostility'].append(person.hostility)

slopes = list()
for person in all_people:
    x = [post[0] for post in data[person.id_number]['feed']]
    y = [post[1][0] for post in data[person.id_number]['feed']]
    fit = np.polyfit(x, y, 1)
    slope = fit[0]
    slopes.append(slope)

mean_neighbor_slopes = list()
for person in all_people:
    neighbors = social_network.neighbors(person)
    mean_neighbor_slope = np.mean([slopes[n.id_number] for n in neighbors])
    mean_neighbor_slopes.append(mean_neighbor_slope)

agitator_mean_neighbor_slope = min(mean_neighbor_slopes)
predicted_agitator = None
for index, slope in enumerate(mean_neighbor_slopes):
    if slope == agitator_mean_neighbor_slope:
        predicted_agitator = all_people[index]
print('Predicted agitator:\t' + str(predicted_agitator))
print('Actual agitator:\t' + str(agitator))
