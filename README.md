# Wordle Solver

A simple Console program written in Python that helps you solve the game [Wordle](https://www.powerlanguage.co.uk/wordle/).

## About the game

The goal of the game is to find the word of the day. The solution always has exactly 5 characters, and you have 6 attempts to find it.

Every time you take a guess by introducing a new five-characters word, you receive feedback to help you refine your next guess. This feedback consists of the characters of your guess lighting up:

* *Green*: the character is in the solution in the exact same position.
* *Yellow*: the character is in the solution, but in a different position.
* *None*: the character is not in the solution at all.

## About this program

In the source code of the game, there are two lists of words: one with the accepted input words, and another one with all the potential solutions. Using these lists, it is easy to create an algorithm to determine the (statistically) best guess for each turn.

For example, you could prioritise different guesses depending on how often the characters of each one are found within the potential solutions. In addition, on top of counting the number of characters that match between each guess and all the potential solutions in order to give priority to one guess or another, you could also count the number of characters that match within the exact same position.

This simple program takes both of the criteria described above to calculate the next guess that is most likely to lead you to a victory.

## Demo

https://user-images.githubusercontent.com/2463287/149636634-85a28e0b-4143-4add-a3da-2e05b508c03f.mp4
