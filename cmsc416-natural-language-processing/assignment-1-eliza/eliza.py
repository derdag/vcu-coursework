# Author: Deniz Erdag
# Course: CMSC 416 - Natural Language Processing
# Assignment: Programming Assignment 1 - Eliza Psychotherapist
# Submission Date: 2/16/2021
#
# Description:
#   Eliza.py is a rogerian chatbot therapist that provokes a user to continue talking about
#   themselves and how they feel by turning their statements into questions.
#
# Usage Instrutions:
#   1. enter 'python eliza.py' in terminal to begin program.
#   2. Eliza will prompt for user name and then begin conversation (enter ONLY name in terminal, no punctuation).
#   3. User enters input in response to Eliza in terminal, this can contain punctuation.
#   4. Eliza will generate a response based on keywords in user input, and will print to terminal.
#   5. Enter 'quit' as user input at anytime (or any other word in quit_words) to end conversation with Eliza.
#
# Example Conversation:
#   [Eliza] Hi, I'm Eliza, a psychotherapist. What is your name?
#   => Deniz
#   [Eliza] Hi Deniz, what is on your mind?
#   => I feel very stressed
#   [Eliza] How long have you felt that way?
#   => Always
#   [Eliza] Are you sure about that?
#   => I guess not
#   [Eliza] Go on...
#   => quit
#   [Eliza] Goodbye :)


import re, random

# words that end the conversation with eliza
quit_words = ["goodbye", "bye", "quit", "stop"]

# default responses
default_responses = [
    "Tell me more...",
    "Go on...",
    "I don't think I understand, could you rephrase?",
    "Interesting, can you elaborate?",
    "How do you feel about that?",
]

# script dicitionary which holds regex keywords/phrases that are to be identified in user inputs along with potential responses. Can consider adding weights to keys.
script = {
    r"i am (.*)": [  # Identify user stating 'I am' something. 'Am' is a a definite word, provoke user to think if they are sure.
        r"why do you think you are?",
        r"do you wish you weren't?",
        r"would you change that if you could?",
    ],
    r"i would (.*)": [  # Identify user stating they 'would' something, they might not necessarily actually feel this way, so question the thought process.
        r"how would it make you feel if you did?",
        r"do you think that is in your control?",
    ],
    r"i (like|love|miss|wish|hope|feel) (.*)": [  # Identify words that indicate user is expressing some type of emotion/feeling. This seems to come up often.
        r"have you always felt that way?",
        r"do you wish you didn't feel that way?",
        r"why do you say that?",
    ],
    r"(.*)?my (.*)": [  # Identify 'my' indicating user is claiming something is their own.
        r"is that important to you?"
    ],
    r"i cant (.*)": [  # Identify user thinking they 'can't' do something. Thinking "I can't" can be harmful.
        r"why do you think you can't?",
        r"do you wish you could?",
        r"do you think you could in the future?",
    ],
    r"i want (.*)": [  # Identify user 'wanting' something. They might not necessarily actually want that thing.
        r"why do you think you want that?",
        r"have you always wanted that?",
        r"are you sure that you want that?",
    ],
    r"(yes|no)": [  # Identify response including 'yes' or 'no' anywhere in their statement, since users might often respond with this simple answer.
        r"you seem quite sure, can you elaborate?",
        r"why are you so sure?",
        r"are you sure?",
    ],
    r"(.*)?hate (.*)?": [  # Identify user hating. Provoke further thought into why they hate since this is a strong feeling.
        r"hate is a strong word. Why do you feel that way?",
        r"do you really think so?",
    ],
    r"(why|where|who|how|when) (.*)": [  # Identify user asking Eliza 'why', 'who', 'where', 'how', and 'when'.
        r"do you often wonder \g<1>?",
        r"why do you wonder that?",
        r"do you wish you didn't wonder \g<1>?",
    ],
    r"(.*)?(he|she|they|theyre|they are) (.*)": [  # Identify pronouns. User is stating something about another person.
        r"how does that make you feel?",
        r"do you think they would agree?",
    ],
    r"(.*)?(sorry|apologize)(.*)": [  # Identify user apologizing to Eliza. An apology shouldn't be necessary.
        r"there is no need to apologize!",
        r"why do you feel the need to apologize?",
        r"how do you feel when you apologize?",
    ],
    r"(.*)?(always|never)(.*)": [  # Identify user using 'always' & 'never'. These seem to often be extremes in conversation and may not be factually correct.
        r"are you sure about that?",
        r"do you think others would agree?",
    ],
    r"(.*)?(same|alike|different)(.*)": [  # Identify user comparing things using 'same', 'alike', or 'different'. Since user comparison may not be correct or is an opinion.
        r"how so?",
        r"in what way?",
        r"would you change that?",
    ],
    r"(.*)?(every|no)(one|body)(.*)": [  # Identify 'everyone', 'noone', 'everybody', 'nobody'. Similar to 'always' & 'never', these can be extremes in conversation.
        r"do you really think that is?",
        r"have you always had this thought?",
    ],
    r"(.*)?because (.*)?": [  # Identify user explaining their reasoining using keyword 'because' and provoke further thought.
        r"do you truly believe that?",
        r"could there be another reason?",
        r"is that the only reason?",
    ],
    r"(.*)?(mother|father|brother|sister|wife|husband|mom|dad)(.*)": [  # Identify user mentioning specifically family members which can be an important topic to discuss.
        r"tell me more about your family...",
        r"do you have a good relationship with your family?",
        r"do you miss your family?",
    ],
}


# Initiate Conversation, retrieve user name
print("[Eliza] Hi, I'm Eliza, a psychotherapist. What is your name?")
name = input("=> ").strip()
print("[Eliza] Hi " + name + ", what is on your mind?")


# Ongoing conversation loop
while True:

    # retrieve user input, strip whitespace and convert to lowercase.
    user_input = input("=> ").strip().lower()

    # end conversation if user_input is a quit_word
    if user_input in quit_words:
        print("[Eliza] Goodbye :)")
        break

    # removes non-word and non-whitespace characters from input
    user_input = re.sub(r"[^\w\s]", "", user_input)

    matches = []  # list to track keyword matches that exist in user input

    # for each keyword in script dictionary, if there is a match, append to matches list
    for key in script:
        out = re.search(key, user_input)
        if out is not None:
            matches.append(key)

    # if there are no matches, respond with a generic response from default_responses
    if not matches:
        print(random.choice(default_responses))
        continue

    # select random key from list of matches
    key = random.choice(matches)

    # select random response from list of responses corresponding to selected key
    eliza_response = random.choice(script[key])

    # print elizas response, substituting groups (if there are any)
    if "\g" in eliza_response:
        print(name + ", " + re.sub(key, eliza_response, user_input))
    else:
        print(name + ", " + eliza_response)
