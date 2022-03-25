### Something of Your Own
I did not bother researching for this lab because I am so looking forwards to later ones. So I just 
implement a contrast filter, which does not even involve any correlation(and neither do `brightness`, by inferrence). The result is mushroom_constrast.png. I chose to make the poisonous mushroom to look more poisonous. The formula I referenced comes from [here](https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/) 

### Pedagogical reflection
The concept and computation of correlation is quite mind-refreshing(?). I can never imagine by myself that translating an image actually needs a correlation kernel! Fresh technical literacy for me. The first part of the lab is not hard conceptually but takes time to think. Plus, it has been a while since I am required to write comments and invent my own test. Those labor takes longer than I thought.

The last part(9~11) provides plenty of opportunities for practicing `closure`, which I have understood conceptually from Javascript textbooks but never got a chance to really use it. Now finally I got a sense of it and began to appreciate its power when building "general-use" functions, though I think its usage can be boiled down to just one short sentence: *hold* variables for inner functions to use.


### About output files
One-off scripts for creating output files as required by the lab 1 write up resides in the `if __main__` part of `lab.py`. All files are stored in the same level in directory as this markdown.

### Administrivia
This labs took me about 10 hours to finish. Also, because I didn't understand what a 'checkoff' means in the first place, I did not put down my thinkings during implementation on a memo or anything. Hence, for this week, no written answers to the checkoff questions are provided, neither for Check Yourself. Both will be included from next lab on. 