# import nltk
import pronouncing
import itertools

# try:
#     nltk.data.find("corpora\\cmudict")
# except LookupError:  # pragma: no cover
#     nltk.download("cmudict")

# arpabet = nltk.corpus.cmudict.dict()


def phonemes(word):
    """
    Break a word into phonemes.

    Raises a ``ValueError`` when the word is not present in the
    pronouncing dictionary so callers can surface a friendly error.
    """
    # return arpabet[word][0] # ['T', 'R', 'EY1', 'L']
    phones = pronouncing.phones_for_word(word) # ["T R EY1 L"]
    if not phones:
        raise ValueError(f"No pronunciation found for '{word}'.")
    return phones[0].split(' ')


def _first_stress_index(phones):
    """
    Locate the index of the first stressed vowel in a list of phonemes.
    """

    for idx, phone in enumerate(phones):
        if any(char.isdigit() for char in phone):
            return idx
    return 0


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
        phones = phonemes([word][0])
        for phone in phones:  # ['T', 'R', 'EY1', 'L']
            if any(char.isdigit() for char in phone):
                dic[word] = phones.index(phone)  # word:index of first stressed vowel {'trail': 2, 'snacks': 2}
                break  # stop after first stressed vowel

        print(word,phones)

    prefix0 = phonemes(text.split()[0])[:dic[text.split()[0]] ]  # ['T', 'R']
    suffix0 = phonemes(text.split()[0])[ dic[text.split()[0]]:]  # ['EY1', 'L']
    prefix1 = phonemes(text.split()[1])[:dic[text.split()[1]] ]  # ['S', 'N']
    suffix1 = phonemes(text.split()[1])[ dic[text.split()[1]]:]  # ['AE1', 'K', 'S']

    # If either word begins with a vowel sound, there's no leading consonant
    # cluster to swap, so no spoonerism is possible.
    if not prefix0 or not prefix1:
        return

    print(prefix0,suffix0,prefix1,suffix1)
    # print(rhymesdict[word])
    for word in text.split():  # ['trail', 'snacks']
        for rhyme in rhymesdict[word]:
            if r"'s" not in rhyme:  # exclude possessive nouns
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
                    if rhymePhones == prefix1 + suffix0:  # ['S', 'N'] + ['EY1', 'L']
                        spoons1.append(rhyme)
                        # break  # stop after first match
    if spoons0 and spoons1:
        return {text.split()[0]: spoons1, text.split()[1]: spoons0}
    else:
        return


def spoon_details(text):
    """
    Provide structured details about how a spoonerism is built for two words.

    The response includes the original phonemes, the swapped phoneme order,
    and any spoonerisms discovered by :func:`spoon`.
    """

    words = text.split()
    if len(words) != 2:
        raise ValueError("Provide exactly two words to swap sounds.")

    first, second = words
    first_phones = phonemes(first)
    second_phones = phonemes(second)

    first_stress = _first_stress_index(first_phones)
    second_stress = _first_stress_index(second_phones)

    prefix0 = first_phones[:first_stress]
    suffix0 = first_phones[first_stress:]
    prefix1 = second_phones[:second_stress]
    suffix1 = second_phones[second_stress:]

    swapped_phonemes = []
    if prefix0 and prefix1:
        swapped_phonemes = [prefix1 + suffix0, prefix0 + suffix1]

    spoon_results = spoon(text)

    sample_result = []
    if spoon_results:
        first_result = spoon_results.get(first, [])
        second_result = spoon_results.get(second, [])
        if first_result and second_result:
            sample_result = [first_result[0], second_result[0]]

    return {
        "original_words": [first, second],
        "phonemes": [first_phones, second_phones],
        "swapped_phonemes": swapped_phonemes,
        "spoonerisms": spoon_results or {},
        "sample_result": sample_result,
        "prefixes": [prefix0, prefix1],
    }


def sentence(sentence):

    """
    for each pair of words, get the spoonerism using spoon
    {'snacks': ['tracks', 'trax'], 'trail': ['snail']}

    for each combination in the result, regenerate the sentence

    """
    sentences = []
    for pair in list(itertools.combinations(sentence.split(), 2)):

        results = spoon(" ".join(map(str, pair)))
        # {'snacks': ['tracks', 'trax'], 'trail': ['snail']}

        if results:
            combos = [x for x in itertools.product(results[pair[0]], results[pair[1]])]
            pair_sentences = []
            for first, second in combos:
                words = sentence.split()
                for idx, word in enumerate(words):
                    if word == pair[0]:
                        words[idx] = first
                        break
                for idx, word in enumerate(words):
                    if word == pair[1]:
                        words[idx] = second
                        break
                pair_sentences.append(" ".join(words))
        else:
            continue  # pragma: no cover
        sentences.extend(sorted(pair_sentences))
    return sentences


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
#                 # print skipped lines i.e. "Chapter 1" & "Introduction"
#                 # print(line.replace('\n', ''))
#         sentences = text.replace("\n", "").split(".")
#     return sentences

# # here's a chapter of a book
# hhgttg = r"C:\Users\dann7982\Google Drive\The Hitch Hiker's Guide to the Galaxy\Chapter 1.txt"
# for sentence in readtext(hhgttg):
#     spoonsentence(sentence)
#     break  # stop after first sentence
