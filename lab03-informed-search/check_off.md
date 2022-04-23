- Discuss your choice for the data structure that build_internal_representation. What other possibile choices could you have made instead, and why did you choose this representation? Did your representation change at all as you encountered new sections of the labs?

  3.2) Auxiliary Data Structures
  > The ultimate goal of this structure is to be able to answer questions quickly about the data that we'll need to answer repeatedly (without looping over the whole dataset). We set things up this way so that we can build these structures once and then use them multiple times to compute various results. As such, it is OK for this function to be a bit slow, so long as it saves time during the actual search process.

However, it may not be possible to store all of the nodes or all of the ways in memory (so if there are nodes and/or ways that you know will be irrelevant, you should not store them in memory).

- Imagine using a BFS (as discussed in recitation 3) to find shortest paths, instead of this method. What would we expect to be different about the paths returned from BFS, versus the paths we're returning here? Try this experiment. What were the results? Do they match your expectations?

- How did the heuristic affect the speed of the search? How many nodes were expanded with and without the heuristic?

- How does your implementation of find_fast_path differ from find_short_path?
- Test your code running in the UI by finding both the shortest and fastest paths from Waltham, MA (west of Cambridge on the map) to Salem, MA (north and east of Cambridge) using the cambridge data set. What differentiates these paths? Why do they look the way they do?