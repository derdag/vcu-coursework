# Author: Deniz Erdag
# Course: CMSC 416 - Natural Language Processing
# Assignment: Programming Assignment 1 - Eliza Psychotherapist
# Submission Date: 2/16/2021
#
# Description:
#
# Usage Instrutions:
#
# Example:

import re

quit_words = ["goodbye", "bye", "quit"]

# Dictionary of translations. ex: my -> your,
translations = {
    "my": "your",
    "myself": "yourself",
    "yourself": "myself",
    "you": "me",  # maybe 'me' instead of 'i'
    "i": "you",  # ? maybe
    "am": "are",
    "your": "my",
    "me": "you",
}

# User inputs a statement ( or proposition? nah probably just statements)

# change this to a dictionary instead of list
temp_script = [
    [
        r"I am (.*)",  # key
        10,  # weight
        [r"Why do you think you are \g<1>?", "", ""],  # replacement string list
    ]
]

# generic responses
generic = ["Tell me more..", "test", "another generic"]

script = {
    r"I am (.*)": [r"Why do you think you are \g<1>?", "", ""],
    r"I think (.*)": [r"Why do you think you are \g<1>?", "", ""],
    r"(.*) always (.*)": [r""],
    r"(.*) because (.*)": [r""],
}


# sorry/apologize
# always/never
# i was
# i am
# i cant
# i will
# i wish/hope
# i need/want
# because
# i think
# yes/no
# i dont
# i like
# i feel/ im feeling
# i love
# i have
# because
# i would
# why do i/ why cant i
# when can i/ when will i
# why
# i remember
# i believe
# i think
# my
# your/you
# i remember
# i forget
# why cant i
# everyone/everybody/nobody/noone
# alike/different
# theyre/ they are
# sad/happy/depressed/sick
# she/he/they

# mother/father/brother/sister/girlfriend/boyfriend/wife/husband/mom/dad

# response when no matches occur:
# - Tell me more
#

# end script words: goodbye, bye


# Initiate Conversation, retrieve user name
print("[Eliza] Hi, I'm Eliza, a psychotherapist. What is your name?")
name = input("=> ")
print("[Eliza] Hi " + name + ", what is on your mind?")


# print(re.sub(script[0][0], script[0][2][0], "I am tired of my girlfriend"))


# Loop
while True:
    user_input = input("=> ")
    print("Recieved Input:", user_input)
    if user_input in quit_words:
        print("[Eliza] Have a good day :)")
        break
