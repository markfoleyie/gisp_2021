'''
Gettysburg Address

This is an exercise in file analysis. Fundamentally it is an exercise in the use of the basic collection objects in
Python such as strings, lists, tuples, dictionaries and sets.request

We are going to use Abraham Lincoln's Gettysburg address of 1863, This is famous for many things, including being a
short speech.

We are going to do some simple analysis on this.
1. Count the number of words in the speech. We will exclude from our analysis a number of 'stop words', in our example
these will be the definite and indefinite articles and some personal pronouns.
2. Count the unique words in the collection produced by 1 above.
3. Count the number of occurrences of each word.

Some hints
1. Import the string module. This gives string.whitespace, a string containing all of the whitespace characters
and string.punctuation, a string containing all of the punctuation characters.

'''

# Import:
# string gives us whitespace and punctuation lists
# utilities.read_from_file_and_net gives us generic functions for retrieving files from the internet and reading files
# from our computer
import string
from utilities.read_from_file_and_net import get_file_from_net as get_url


# Variables to hold file URLs
SPEECH_URL = "https://markfoley.info/pa1/gettysburg.txt"
STOPWORDS_URL = "https://markfoley.info/pa1/stopwords.txt"


def make_word_list(g_file, stop_words):
    """Create a list of words from the file while excluding stop words."""
    speech = []  # list of speech words: initialized to be empty

    for line_string in g_file:
        line_list = line_string.strip(
            string.whitespace).split()  # split each line into a list of words and strip whitespace
        for word in line_list:
            word = word.lower()  # make words lower case (we consider a word in lowercase and uppercase to be equivalent)
            word = word.strip(string.punctuation)  # strip off punctuation
            if (word not in stop_words) and (word not in string.punctuation):
                # if the word is not in the stop word list, add the word to the speech list
                speech.append(word)
    return speech


def count_words(speech):
    """Create a dictionary and count the occurrences of each word.
    If a word already exists in the dictionary, add 1 to its counter
    otherwise set a counter for to to an initial value of 1"""
    counts = {}
    for word in speech:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


def main():
    '''Process the speech once you can successfully open both the speech and the stop words files from the net.'''
    try:
        # Make a list of lines by splitting on the newline character.
        speech = get_url(SPEECH_URL)
        speech = speech.split('\n')

        # Make a tuple of all the stop words while losing the newline character
        stopwords = get_url(STOPWORDS_URL)
        stopwords = tuple(stopwords.split(','))

        # Make word list from speech while excluding stop words
        speech = make_word_list(speech, stopwords)

        # Make a set of words from speech which automatically assures that each entry is unique
        unique = set(word for word in speech)

        # Print the results
        print(f"Speech Length: {len(speech)}")
        print(f"Unique words: {len(unique)}")
        print("\nWord count")

        words = count_words(speech)

        print("-" * 50)
        for k,v in words.items():
            print(f"{k}: {v},", end=" ")
        print("\n")

    except Exception as e:
        print(f"{e}")


# Run if stand-alone
if __name__ == '__main__':
    main()