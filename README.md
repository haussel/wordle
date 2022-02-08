# wordle
A class to cheat at wordle :) 

## Installation
We use the 5 letter word list of D. Knuth available from his webpage: 
https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt

Download this file into the data/ directory

## Usage
This is a class to cheat at Wordle (https://www.powerlanguage.co.uk/wordle/)
A typical game goes like:
```
import wordle
w = wordle.Wordle()
w.next_guess() 
```
play the proposed word and add the information:
```
w.add_absent('ros')
w.add_present('a', 0)
w.add_present('e', 4)
w.next_guess()
```
play the word and so on...

In case the proposed word is not accepted by the wordle site (for example 'latin'...), more guesses sorted by the
frequency of their letters can be seen:
```
w.next_guess(show=3)
w.next_guess(showall=True)
```
To test whether a word could be a solution;
```
w.test(word)
```