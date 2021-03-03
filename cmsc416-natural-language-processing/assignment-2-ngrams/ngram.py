# Author: Deniz Erdag
# Course: CMSC 416 - Natural Language Processing
# Assignment: Programming Assignment 2 - N-gram language model
# Submission Date: 3/2/2021
#
# Description:
# 
#   ngram.py generates 'm' number of sentences given an arbitrary number of text files by learning an n-gram language model." 
#   Sentences are generated semi-randomly by recording frequencies of n-token phrases, calculating relative probabilities of the last token occuring, given it's n-1 preceeding context.
#   Sentence generation continues until an ending token is seen.
#
# Algorithm:
#   
#   The ngram model is implemented here with a dictionary, storing context tokens as keys, with the value being a list of all tokens, with repitition, seen after the context.
#
# Usage Instrutions / Example Input & Output:
# 
# > python ngram.py 4 5 our_square.txt lost_fruits_of_waterloo.txt america_and_the_world_war.txt
#
# 1: of course i am speaking of the thing and not the army itself, that developed militarism and brought other unhappy effects.
# 2: they are trained to regard war as a means of organizing the international state.
# 3: unquestionably under this clause belgium has committed no hostile act.
# 4: are you still sculping me.
# 5: complete tolerance was to exist for the three forms, catholicism, lutheranism, and calvinism.

from collections import defaultdict, Counter
from sys import argv
import random
import re

n = int(argv[1])
m = int(argv[2])
files = argv[3:]
total_counts = Counter()
dictionary = defaultdict(list)
sentence_list = []

print("Author > Deniz Erdag")
print("")
print("Description > ngram.py generates 'm' number of sentences given an arbitrary number of text files by learning an n-gram language model.")
print("              Sentences are generated semi-randomly by calculating probabilities of tokens given n-1 preceeding context tokens.")
print("")
print("Arguments Supplied >", "n:", n, "m:", m, "files:", files)
print("")

# parse input files
for file in files:
    with open(file, "r") as f:
        text = f.read().lower()
        text = re.sub(r"[\n]", " ", text)  # remove new lines
        text = re.sub(r"[^a-z0-9\s,.!?]", "", text)  # select text, numbers, whitespace, and ,.!?
        text = re.sub(r",", " ,", text)  # seperate commas from preceding word
        
        # split text into sentences, delimited by .!?. removing empty last sentence
        sentence_list += re.split(r"[.!?]", text)[:-1]  

# store frequencies of ngrams into dictionary for all sentences
for sentence in sentence_list:
    sentence = (
        " ".join(["<start>" for _ in range(n)])  # add n "<start>" tokens
        + " "
        + sentence.strip()
        + " <end>"  # add "<end>" token
    )
    tokenized_sentence = re.split(r"\s", sentence.strip())  # split sentence into tokens

    # only select sentences that are greater than length n. -(n+1) to account for start and end tokens that we added
    if len(tokenized_sentence) - (n + 1) > n:
        total_counts += Counter(tokenized_sentence)

        # create list of n-grams from tokenized sentence
        ngrams = [tokenized_sentence[i : i + n] for i in range(len(tokenized_sentence))]

        # add ngrams to dictionary, supplying 0 to n-1 tokens as key, appending last token to the list of tokens matching the same key
        for ngram in ngrams:
            dictionary[tuple(ngram[:-1])].append(ngram[-1])


# generate m sentences based on model
for i in range(m):  
    temp_sentence = ["<start>" for _ in range(n)]  # add n <start> tags to supply initial context to sentence generation

    while "<end>" not in temp_sentence: # continue generating sentence until <end> token is seen

        total = 0
        random_num = random.uniform(0, 1)

        # TODO: perhaps consolidate this if statement, using only one dictionary to hold ngrams to avoid repeated code
        if n == 1: # 
            for key in total_counts: # semi-random token selection given probabilities
                probability = total_counts[key] / sum(total_counts.values())
                total += probability

                if random_num < total: 
                    temp_sentence.append(key)
                    break

        else: # for all other 'n' grams
            context = temp_sentence[-(n - 1) :] # grab context needed to determine next token
            options = dictionary[tuple(context)] # fetch list of all tokens seen after context in given text, including repitition
            counts = Counter(options) # count possible options
            for key in counts:
                probability = counts[key] / len(options)
                total += probability

                if random_num < total:
                    temp_sentence.append(key)
                    break

    # cleanup and print output sentence
    output = " ".join(temp_sentence)
    output = re.sub(r"<start>", "", output)
    output = re.sub(r"<end>", ".", output)
    output = re.sub(r" , ", ", ", output)
    output = re.sub(r" \.", ".", output)
    output = re.sub(r"\s+", " ", output)
    print(str(i + 1) + ": " + output.strip())
