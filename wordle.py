import numpy as np
import collections
import string
import os


class Wordle:
    """
    A class to cheat at wordle...

    """
    def __init__(self):
        basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'data/')
        wordfile = os.path.join(basedir, 'sgb-words.txt')
        if not os.path.exists(wordfile):
            raise IOError('Dictionary file sgb-words.txt not found')
        with open(wordfile, 'r') as f:
            self.words = np.array(f.read().splitlines())
        self.freq = collections.Counter()
        self.absent = []
        self.correct = [None, None, None, None, None]
        self.present = None
        for w in self.words:
            self.freq.update(w)
        self.letters = [string.ascii_lowercase, string.ascii_lowercase,
                        string.ascii_lowercase, string.ascii_lowercase, string.ascii_lowercase]

    def add_absent(self, letters):
        """
        Add letters that are not in the word (grey in wordle).

        :param letters: string with the grey letters
        :return: None
        """
        for l in letters:
            if l not in self.absent:
                self.absent.append(l)
                for i in range(5):
                    self.letters[i] = self.letters[i].replace(l, '')

    def add_correct(self, letter, position):
        """
        Add one letter where correct position is known (green in wordle)

        :param letter: char: the letter
        :param position: int: position counted from 0
        :return: None
        """
        if not self.correct[position]:
            self.correct[position] = letter
            self.letters[position] = letter

    def add_present(self, letter, notpos):
        """
        Add letter in the word, but not at the correct place (yellow letters in wordle)
        :param letter: char: the letter
        :param notpos: int: the position where the letter is not, counted from90
        :return: None
        """
        if self.present is not None:
            if letter in self.present.keys():
                self.present[letter].append(notpos)
            else:
                self.present[letter] = [notpos]
        else:
            self.present = {letter: [notpos]}
        self.letters[notpos] = self.letters[notpos].replace(letter, '')

    def test(self, w):
        """
        Test whether a word can be the solution
        :param w: string: word
        :return: bool
        """
        keep = True
        for i in range(5):
            if w[i] not in self.letters[i]:
                print('{} not in {}'.format(w[i], self.letters[i]))
                keep = False
        if self.present is not None:
            for l in self.present.keys():
                if l not in w:
                    keep = False
                    print('{} not in {}'.format(l, w))
        return keep

    def next_guess(self, showall=False, show=2):
        """
        returns the best next guesses, sorted by their likelihood computed from the relative
        frequencies of their letters

        :param showall: bool: if True, returns all the matching words, defaulted to False
        :param show: int: number of guesses to return. Defaulted to 2.
        :return: the guesses, from the least likely to the more likely
        """
        guess = []
        score = []
        for w in self.words:
            keep = True
            used = []
            s = 0
            for i in range(5):
                if w[i] not in self.letters[i]:
                    keep = False
                else:
                    if w[i] not in used:
                        s = s + self.freq[w[i]]
                        used.append(w[i])
            if self.present is not None:
                for l in self.present.keys(): 
                    if l not in w:
                        keep = False
            if keep:
                guess.append(w)
                score.append(s)
        guess = np.array(guess)
        score = np.array(score)
        osc = np.argsort(score)
        if showall:
            return guess[osc]
        else:
            return guess[osc[-show:]]
