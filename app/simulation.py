#!/usr/bin/env python3

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from termcolor import cprint
import itertools
import json
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import sys
import time

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
    return min(all_posts, key=lambda p: abs(target_sentiment - p[0]))[1]

class Person(object):
    def __init__(self, id_number):
        self.id_number = id_number
        # https://homepage.stat.uiowa.edu/~mbognar/applets/normal.html
        self.gullibility = np.random.normal(loc=0.5, scale=0.1) # mean=loc,stdev=scale
        self.hostility = np.random.normal(loc=0, scale=0.2); self.hostility_temp = None
        self.activity_level = np.random.chisquare(3) / 15
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
            'neighbors': list(),
        }
        person.feed = list()

initial_state = dict()
for person in all_people:
    initial_state[person.id_number] = person.attitude()

for step in range(simulation_step_count):
    for group in friend_groups:
        for person in group:
            if random.random() < person.activity_level:
                data = person.post(step, data)
                time.sleep(0.0005)
                print('@{}:\t{}'.format(person.id_number, data[person.id_number]['feed'][-1][1]))
                for viewer in social_network.neighbors(person):
                    if random.random() < viewer.gullibility:
                        viewer.hostility += person.hostility / 500

            # update tracked data
            data[person.id_number]['feed_length'].append(len(data[person.id_number]['feed']))
            data[person.id_number]['hostility'].append(person.hostility)

for person in all_people:
    neighbor_ids = [n.id_number for n in social_network.neighbors(person)]
    data[person.id_number]['neighbors'] = neighbor_ids

j = json.dumps(data)
try:
    outfile = sys.argv[1]
except IndexError:
    outfile = '/tmp/out.json'
with open(outfile, 'w') as f:
    f.write(j)
print('#' * 80)
print('changes')
changes = dict()
for initial in ['pos', 'neu', 'neg']:
    for final in ['pos', 'neu', 'neg']:
        changes[initial + ' -> ' + final] = 0
for person in all_people:
    initial = initial_state[person.id_number]
    final = person.attitude()
    if final != initial:
        changes[initial + ' -> ' + final] = changes[initial + ' -> ' + final] + 1
for key in changes.keys():
    if changes[key] != 0:
        print(key + ': ' + str(changes[key]))

print('#' * 80)
print('group count:\t'   + str(friend_group_count))
print('friends/group:\t' + str(friends_per_group))
print('person count:\t'  + str(len(all_people)))
print('sim days:\t'      + str(simulation_step_count))
print('total posts:\t'   + str(sum([len(data[id_num]['feed']) for id_num in data.keys()])))
cprint('agitator:\t'     + str(agitator), 'red')
print()
while True:
    print('your options:')
    print(' - view [n]etwork')
    print(' - view [h]ostility over time')
    print(' - view [f]it info')
    print(' - [e]xit')
    command = input('what now? ')
    if command == 'n':
        group_color_map = list()
        for index, group in enumerate(friend_groups):
            for _ in range(len(group)):
                group_color_map.append(index / len(friend_groups))
        plt.title('The full social network')
        nx.draw(social_network, with_labels=True, node_color=group_color_map)
        plt.show()
    elif command == 'h':
        id_number = int(input('for whom? '))
        person = all_people[id_number]
        plt.title('Hostility')
        plt.ylim(-1, 1)
        plt.ylabel('Hostility (-1 to 1)')
        plt.xlabel('Simulation step number')
        plt.axhspan(0.25,1,alpha=0.2,color='green')
        plt.axhspan(-1,-0.25,alpha=0.2,color='red')
        plt.plot(data[person.id_number]['hostility'])
        plt.show()
    elif command == 'f':
        id_number = int(input('for whom? '))
        person = all_people[id_number]
        x = [post[0] for post in data[person.id_number]['feed']]
        y = [post[1][0] for post in data[person.id_number]['feed']]

        fit = np.polyfit(x, y, 1)
        slope = fit[0]
        fit_fn = np.poly1d(fit)

        #plt.plot(x, y)
        plt.title('Regression slope: ' + str(slope))
        plt.xlabel('Simulation step')
        plt.ylabel('Post sentiment')
        plt.plot(x, y, 'o', x, fit_fn(x))
        plt.show()
    elif command == 'e':
        exit(0)
    else:
        print('not sure what you meant by that...')
