"""spooner"""

__version__ = '0.1'

import nltk
import pronouncing
import itertools
import random

try:
    nltk.data.find("corpora\\cmudict")
except LookupError: # pragma: no cover
    nltk.download("cmudict")

arpabet = nltk.corpus.cmudict.dict()


def phonemes(word):
    """
    breaks a word into syllables
    """
    return arpabet[word][0]

print(phonemes("trail"))


def spoon(text):
    """
    switches the first sound in two words and checks for valid results

    credits:
    https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word/4103234#4103234
    https://stackoverflow.com/questions/33666557/get-phonemes-from-any-word-in-python-nltk-or-other-modules
    :param text: 
    :return a list of matches for each word: 
    """

    dic = {}
    rhymesdict = {}

    spoons0, spoons1 = [], []
    for word in text.split():  # ['trail', 'snacks']
        rhymesdict[word] = pronouncing.rhymes(word)
        #try:
        phones = phonemes([word][0])
        for phone in phones:  # ['T', 'R', 'EY1', 'L']
            if any(char.isdigit() for char in phone):
                firstStress = phones.index(phone)  # 'EY1'
                dic[word] = firstStress  # {'trail': 2, 'snacks': 2}
                break  # stop after first stressed vowel
        # except KeyError:
        #     # print(word, "not in CMU Pronunciation Dictionary")
        #     # break
        #     pass
    for word in text.split(): 
        try:
            prefix0 = arpabet[text.split()[0]][0][:dic[text.split()[0]]]  # ['T', 'R']
            suffix0 = arpabet[text.split()[0]][0][dic[text.split()[0]]:]  # ['EY1', 'L']
            prefix1 = arpabet[text.split()[1]][0][:dic[text.split()[1]]]  # ['S', 'N']
            suffix1 = arpabet[text.split()[1]][0][dic[text.split()[1]]:]  # ['AE1', 'K', 'S']
        except KeyError: # pragma: no cover
            prefix0 = []
            suffix0 = []
            prefix1 = []
            suffix1 = []
            
        for rhyme in rhymesdict[word]:
            if (
                r"'s" not in rhyme
            ):  # exclude possessive nouns
                try:
                    rhymePhones = phonemes([rhyme][0])
                except KeyError:
                    rhymePhones = []
                    # print("word is missing from the pronouncing dictionary")
                # print(rhymePhones)
                if prefix0 != prefix1:
                    if (
                        rhymePhones == prefix0 + suffix1
                    ):  # ['T', 'R'] + ['AE1', 'K', 'S']
                        spoons0.append(rhyme)
                        # break  # stop after first match
                    if (
                        rhymePhones == prefix1 + suffix0
                    ):  # ['S', 'N'] + ['EY1', 'L']
                        spoons1.append(rhyme)
                        # break  # stop after first match
    if spoons0 and spoons1:
        return [spoons1, spoons0]
    else:
        return


def spoonsentence(sentence):
    for pair in list(
        itertools.combinations(sentence.split(), 2)
    ):
        results = spoon(" ".join(map(str, pair)))
        if results:
            subbedSentence0 = " ".join(
                [
                    random.choice(results[0])
                    if x == pair[0]
                    else x
                    for x in sentence.split()
                ]
            )
            subbedSentence1 = " ".join(
                [
                    random.choice(results[1])
                    if x == pair[1]
                    else x
                    for x in subbedSentence0.split()
                ]
            )
    return subbedSentence1

# scan longer text file for spoonerisms

# def readtext(source):
#     text = ""
#     with open(source) as corpus:
#         for line in corpus:
#             if (
#                 len(line.split()) > 2
#             ):  # skip very short lines
#                 text += line
#             elif (
#                 "." in line
#             ):  # include very short lines that include "."
#                 text += line
#             else:
#                 pass
#                 # print(line.replace('\n', ''))  # print skipped lines i.e. "Chapter 1" & "Introduction"
#         sentences = text.replace("\n", "").split(".")
#     return sentences

# # here's a chapter of a book
# hhgttg = r"C:\Users\dann7982\Google Drive\The Hitch Hiker's Guide to the Galaxy\Chapter 1.txt"
# for sentence in readtext(hhgttg):
#     spoonsentence(sentence)
#     break  # stop after first sentence
