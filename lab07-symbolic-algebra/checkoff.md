- Briefly describe your implementation of parenthesization. How did you use inheritance to avoid repetitious code and to avoid explicitly checking the type of any of the objects?

Parenthesization is implemented in `BinOP.__str__`. \\
I defined a class variable called `precedence` for all 6 "instance class" and utilized it in  `BinOP.__str__` to determine whether parentesization is necessary.


- Describe your implementation of the eval method. How does your code handle the case where not all of the necessary variables are specified?

- Describe your process for adding the Pow class. What pieces of your code needed to change to make this addition?

- Briefly describe why we wanted to avoid explicitly checking types throughout the lab.

- Demonstrate using your code to simulate some symbolic algebra problems of your own choosing that demonstrate all of the functionality in the lab.