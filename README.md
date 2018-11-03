
![Soper header](soper_header.png)

# Soper

Soper is a proof-of-concept of a tool for tracking the spread of sentiments and rumors through social networks. It works by detecting changes in the sentiments of the posts of your friends. The more dramatically your friends' views shift over time, the more suspicious you are to Soper.

Soper was _heavily_ inspired by [a talk](https://www.cics.umass.edu/event/spread-contagions-presence-latent-spreaders-identifying-hidden-culprits-and-learning) from [Maggie Makar](https://mymakar.github.io/).

Soper is named for George Soper, who discovered Mary Mallon ("Typhoid Mary") as the first asymptomatic carrier of typhoid fever in the United States. It was created in 24 hours for [HackHolyoke](http://www.hackholyoke.com/) 2018.

## Terminology
I kinda just sort of made up my own words for stuff as I went along. Let's go through them!

 * Person: one member of the social network: Has three properties:
   * Hostility: how the person feels about Elbonians, with -1 being the most negative and 1 being the most positive.
   * Gullibility: likelihood of letting a post they see on the internet affect their hostility from 0 to 1 with 0 being no chance at all and 1 being complete faith in everything.
   * Activity level: the probability a person will make a post on a given day.
 * Friend group: a group of people that all know each other, probably because they have some shared common interest (school, work, hobby, etc.).
 * Social network: a group of people, formed by merging a few friend groups and adding some connections randomly between them.
 * Agitator: a member of a social network that's _very_ dedicated to spreading some specific message (the idea is that they're some sort of paid troll).

## How it works
Soper analyzes the rate of change of the sentiments of each person's friends. Specifically, it generates a least-squares regression for each friend's post sentiment vs. time, then computes the mean regression slope for all of a person's friends. People with unusually negative slopes are more likely to be agitators, because they bombard their friends with propaganda.

The scenario for the simulation this repository is a massive influx of [Elbonian](http://dilbert.wikia.com/wiki/Elbonia) refugees, and a single agitator dedicated to spreading anti-Elbonian sentiment.

## Technology
I started working on this project by experimenting in [Jupyter](https://jupyter.org/) notebooks, then moved to just working with regular source code files once I got a decent thing going.

Soper is written in [Python 3](https://www.python.org/) and uses:
 * [NLTK](http://www.nltk.org/) for natural language processing.
 * [NetworkX](https://networkx.github.io/) for network modeling.
 * [Numpy](http://www.numpy.org/) for miscellaneous math stuff.
 * [Matplotlib](https://matplotlib.org/) for plotting pretty graphs.

For sentiment analysis, Soper uses [VADER](https://github.com/cjhutto/vaderSentiment), a sentiment analyzer tuned specifically for social media posts.

## Image attributions
 * The magnifying glass is by ernes on [openclipart.org](https://openclipart.org/detail/5218/lente-magnifying-glass).
 * The social network image is by [Martin Grandjean](https://commons.wikimedia.org/wiki/File:Social_Network_Analysis_Visualization.png).
