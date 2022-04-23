# 6.009 lecture 6

# in this lecture, we'll look at data about the paintings produced on bob
# ross's show, "the joy of painting."

# there is a small amount of code below, but hopefully a large amount of
# utility

# we expect that for many of you, operations of this form (loading data from
# files, then combining and manipulating those data) will be a common
# occurrence in the future (whether for a career, hobby projects, UROPs, work
# in other classes, etc).

# let's start by looking at the data, which are spread across three files:
#
#   episodes.json: contains a unique identifier for each episode, as well as
#   information about the season number, episode number, and title of each
#   episode
#
#   features.csv: contains a representation of which features exist in each
#   episode's painting
#
#   guest_host_episodes.txt: contains a list of episodes (one per line,
#   represented as SxxEyy) that were guest hosted by bob's son steve, in case
#   we want to compare them


# let's start by looking at data/features.csv.  you can try opening it in a
# text editor or in a spreadsheet program, but we can also read it using Python.

# let's start by looking at a couple of different ways we can get data out of a
# file, starting with maybe the most straightforward:
#
# f = open('data/features.csv')
# alltext = f.read()  # read _all_ of the text from the given file into a string
# f.close()
#
#
# but a spiffy way with context manager helps avoid some pitfalls (most
# notably, forgetting to close the file, particularly on error)
#
#  with open('data/features.csv') as f:
#      alltext = f.read() # read the whole file into a string
#
#  with open('data/features.csv') as f:
#      firstchar = f.read(1)  # read a single character into a string
#
#  with open('data/features.csv') as f:
#      oneline = f.readline()
#      # what happens if we call readline again within this block?
#      # what if we do it inside of a second block instead?
#
#  with open('data/features.csv') as f:
#      for line in f:
#          print(line)  # note the blank line here!  try printing repr(line) to explain
#          print('hello')
#


# ok, now we've seen something about opening files, but let's think about using
# the particular data we have available here.

# to start, let's consider the question: what fraction of paintings have at
# least one tree in them?
#    -> want to look at the tree column
#    -> but maybe let's think if there's a nicer representation that would let
#       us answer not only this, but also similar questions of the same form.
#       -> maybe a dictionary id: {set of features (identified by column header)}
#          or something else if a student suggests.
#          how can we do this?  need to know which index maps to each header?
#       -> maybe try looking at the file again, see any structure we can exploit?

painting_features = {}
with open('data/features.csv') as f:
    # below: .strip() removes whitespace (spaces, tabs, newlines) from the
    # start and the end of a string; .lower() converts to lowercase (bob ross
    # wouldn't yell!), and .split(',') gives us a list of substrings that were
    # separated by commas in the original string.
    # all told, this gives us a list containing the headers (names of the
    # columns), one after the other
    headers = f.readline().strip().lower().split(',')
    for line in f:
        # each line (after the first) represents one episode, with an ID,
        # followed by some number of True/False values, one corresponding to
        # each possible feature in the associated painting

        # separate this line into a list, like we did above (note .strip() to
        # remove the trailing \n)
        vals = line.strip().split(',')

        # there are many different ways we could do the following piece, but we
        # would like to construct a set containing the names of the features
        # present in this episode.  we'll use a happy little set comprehension:
        this_features = {header for header, val in zip(headers, vals) if val == 'True'}
        # note a potential bug here: "if val" on its own would not have worked;
        # why?

        # now, let's associate this set of features with this episode's ID in
        # the dictionary
        painting_features[vals[0]] = this_features


# Some good questions to ask yourself (or the data!)
#  * how many total paintings are represented?  (403)
#  * what fraction of these contain at least one tree? (~89.5%)
#  * more than one tree? (~83.6%)
#  * what about a (prominently featured) cloud or more? (~44.4%)


# we could ask other things here, too: what is the most common feature?  what
# is the least common feature?  etc.  let's try building a second structure to
# keep track of this:
feature_episodes = {}
for episode_id, features in painting_features.items():
    for feature in features:
        feature_episodes.setdefault(feature, set()).add(episode_id)

# and a happy little dictionary comprehension:
feature_count = {k: len(v) for k,v in feature_episodes.items()}

# some trial-and-error in getting a sorted list by feature count... which of
# the following will work to answer these questions?
#
# sorted(feature_count)
# sorted(feature_count.values())
# sorted(feature_count.items())
# sorted(feature_count.items(), key = lambda kv:kv[1])


# maybe now we'd like to break things down by season or something like that,
# but features.csv doesn't have that information.  so let's read some more
# data!
#
# let's take a look at data/episodes.json.  it's in a format called JSON, which
# is commonly used when we want to store complex data on disk.  JSON has
# representations for dictionaries, strings, lists, numbers, Booleans, etc; and
# most programming languages (including Python) have nice ways to load and save
# JSON files.
#
# hopefully at this point in the semester, you feel confident that you could
# write a parser for the JSON language, given enough time.  but for now, since
# we've almost graduated from 6.009, we can use an import instead :)

# for more information, see https://docs.python.org/3/library/json.html
import json

with open('data/episodes.json') as f:
    episodes = json.load(f)


# let's try to answer some questions about these data (forgetting the features
# temporarily):
#
# * how many seasons? (31)
# * how many episodes in each season? (13)


# now let's try answering some more complicated questions.  for example, did
# the fraction of paintings containing clouds vary much from season to season?
#
# this is a complicated question that requires combining data from our two
# sources!  how can we do this?

# note that here we make a structure starting with the information from
# episodes.json, but we include the painting features from features.csv in this
# representation as well (maybe try printing some of these things after running
# this)
episode_features = {}
for info in episodes:
    myinfo = info.copy()
    id_ = myinfo.pop('id')
    episode_features[id_] = myinfo
    episode_features[id_]['features'] = painting_features[id_]


# now let's try separating this into a different representation instead, a
# list-of-lists, where the Nth inner list contains all episodes from season N.
episodes_by_season = [
    [i for i in episode_features.values() if i['season'] == season]
    for season in range(1, 32)
]

# alternatively, we could have used map and filter:
# episodes_by_season = list(map(lambda season: list(filter(lambda ep: ep['season'] == season, episode_features.values())), range(1, 32)))

# try some checks here: how many episodes are in each season?  etc.

# now let's try to figure out the fraction of episodes that feature clouds
# _within each season_, with another happy little list comprehension:

clouds_by_season = [
    (sum('clouds' in ep['features'] for ep in season)/len(season))
    for season in episodes_by_season
]

# try printing these data.  it's unfortunately a little difficult to see!
# let's try generating a plot to see if that illuminates anything.  here, we
# use a module called matplotlib ("pip install matplotlib" if you don't have it
# installed) to generate a little plot:

import matplotlib.pyplot as plt
plt.plot(clouds_by_season)
plt.ylim(0, 1)
plt.show()

# this is actually kind of surprising, maybe, if you're a fan of bob ross.  it
# seems that the happy little clouds were more prevalent in the first (or
# middle) several seasons, compared to the last few.  we can run the same
# analysis with trees:

tree_by_season = [(sum('tree' in ep['features'] for ep in season)/len(season)) for season in episodes_by_season]

# (also, if we are going to be repeatedly looking up things like this, it would
# probably be good to write a helper function to avoid repeating code (like
# that on lines 191-194 and on line 211); but let's take a look at our plot
# anyway)

plt.plot(tree_by_season)
plt.ylim(0, 1)
plt.show()

# trees are more constant!  also, if we remove the first plt.show() above, we
# can plot these on the same axes to see if clouds ever overtook trees, for
# example (they didn't).

# here's a more fully-featured example, showing some more of the things we can
# do to make a nice plot using some of the neat features of matplotlib:

plt.plot(clouds_by_season, label='clouds')
plt.plot(tree_by_season, label='trees')
plt.ylim(0, 1)
plt.legend()
plt.grid()
plt.xlabel('season number')
plt.ylabel('fraction of episodes containing this feature')
plt.show()



# one more hitch, some of the episodes were not hosted by bob ross, but rather
# by his son steve (or someone else)!  if we're trying to characterize bob's
# paintings, we should probably filter out the episodes that steve hosted.
# luckily, we have those data, in data/guest_host_episodes.txt.  maybe we can
# also see if there are any big differences in style between the two? (though
# we need to be careful since N will be so different between the two cases)

# anyway, let's look at the file, it's in a weird format.  how can we get
# something out of that that's useful?  let's try pulling out the relevant
# information in a format that we can work with:

non_bob_eps = set()
with open('data/guest_host_episodes.txt') as f:
    for line in f:
        non_bob_eps.add((int(line[1:3]), int(line[4:6])))

# one thing to be careful of here is that it may be tempting to do
# int(line[-2:]) for the episode number, but that won't work as written!
# because of the newline character

# now with the above, we can filter out episodes that bob ross didn't host:

bob_episodes = [
    i for i in episode_features.values()
    if (i['season'], i['episode']) not in non_bob_eps
]

# question to try to answer:
#   * how does bob's fraction of trees compare to the overall average?
#   * are there other places where things differ substantially between bob and
#     his guest hosts?

# hopefully this has been both useful and fun!  of course, there are many other
# kinds of things that you could try asking about these data (or with data of
# your own), so have fun :)
