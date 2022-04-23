In last week's lecture, we started by looking at the problem of flood fill, an operation on images where we filled in a region with a new color. Briefly at the end of that lecture, we made some modifications to that algorithm such that, rather than filling in a region, we were able to find a path between two points in an image.

This week's pre-lecture materials are presented in video form, as a portion of a lecture from the spring 2021 semester. The video builds on the ideas from last week's lecture and formalizes them a little bit, introducing an interesting category of algorithms called graph search algorithms, with a particular focus on path-finding.

In Monday's lecture, we'll continue to build on these ideas.

Please watch the video and answer the question below.

Which of the following statements are true?

- [ ]	In order to be a BFS, it's important that new paths are added to (and removed from) the front of the agenda, rather then the end of the agenda.

- []	If BFS finds a path, that path is guaranteed to be optimal (in terms of length).

[]	DFS might enter an infinite loop even if the search domain is finite.

[] It is possible that DFS and BFS could return the same path for some problem.
	
[] It is possible that DFS and BFS could return different paths for some problem.
	
[] BFS is guaranteed to find a path if one exists, even in an infinite domain.
