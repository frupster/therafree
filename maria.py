# Maria Chatbot Implementation
# This code implements a simple version of the Eliza chatbot, 
# which simulates a conversation by responding to user inputs with pre defined patterns and responses
# The chatbot uses pattern matching to identify keywords and generate appropriate replies
# uses regex

import re
import random

class Maria:
    def __init__(self):
        self.pronouns = {
            "i": "you",
            "me": "you",
            "my": "your",
            "am": "are",
            "you": "I",
            "your": "my",
            "yours": "mine",
            "mine": "yours",
            "he": "his",
            "him": "his",
            "his": "he"
        }

        self.patterns = [

            # Exit / quit
            (r'\b(quit|exit|bye)\b',
             ["Thank you for talking with me.",
              "Goodbye. It was nice talking to you."]),

            # Greeting
            (r'\b(hello|hi|hey)\b',
             ["Hello. I'm glad you could drop by today, what can I help you with?",
              "Hi there. How can I help you?"]),

            # "Why can't I ..."
            (r'why can\'?t i (.*)',
             ["Why do you think you can't {0}?",
              "What do you think is stopping you from {0}?",
              "Do you believe you might be able to {0} someday?"]),

            # "I need ..."
            (r'i need (.*)',
             ["Why do you need {0}?",
              "Would it really help you to get {0}?",
              "Are you sure you need {0}?"]),

            # "I want ..."
            (r'i want (.*)',
             ["Why do you want {0}?",
              "How would getting {0} help you?",
              "Do you really want {0}, or is something else going on?"]),

            # "I feel ..."
            (r'i feel (.*)',
             ["What makes you feel {0}?",
              "How long have you been feeling {0}?",
              "What do you usually do when you feel {0}?"]),

            # "I'm ..."
            (r'i\'?m (.*)',
             ["How long have you been {0}?",
              "Why do you say that you are {0}?",
              "How does being {0} affect you?"]),

            # "I can't ..."
            (r'i can\'?t (.*)',
             ["What makes it difficult for you to {0}?",
              "Have you tried to {0} before?",
              "What do you think would happen if you could {0}?"]),
            
            # "Because ..."
            (r'because (.*)',
             ["Is that the only reason?",
              "What other reasons might there be?",
              "How does that reason make you feel?"]),

            # "But ..."
            (r'\b(but|however)\b',
             ["What do you mean by {0}?",
              "Can you elaborate on that?",
              "How does that change your perspective?"]),
            
            # "I wish ..."
            (r'\b(i wish|i hope)\b',
             ["What do you wish for?",
              "Why do you hope for that?",
              "How would your life be different if you got what you wish for?"]),

            # "Yes" or "No"
            (r'\b(yes|no)\b',
             ["Why do you say {0}?",
              "Can you explain why you feel that way?",
              "What makes you so sure about that?"]),

            # Sadness (word spotting)
            (r'\b(sad|depressed|unhappy|down|blue|cry|crying|cried)\b',
             ["I'm sorry you're feeling sad.",
              "What do you think is causing your sadness?",
              "Would you like to talk about what's making you feel this way?"]),
            
            # Anger (word spotting)
            (r'\b(angry|mad|furious|irritated|frustrated|upset)\b',
             ["What is making you feel that way?",
              "How do you usually deal with those feelings?",
              "Do you think feeling that way is justified?"]),

            # Anxiety / stress (word spotting)
            (r'\b(anxious|anxiety|stressed|stress|worried|scared)\b',
             ["What usually triggers those feelings?",
              "How do you cope when you feel that way?",
              "Has this been affecting your daily life?"]),

            # Relationships / family (word spotting)
            (r'\b(mother|father|mom|dad|family|friend|partner|sibling|brother|sister|child|daughter|son|baby|boyfriend|girlfriend)\b',
             ["Tell me more about that relationship.",
              "How does that relationship affect you?",
              "Does this relationship cause you stress?"]),
            
            # Love / affection (word spotting)
            (r'\b(love|loving|loved|affection|affectionate|caring|care|romance|romantic)\b',
             ["Is that really love?",
              "What does love mean to you?"]),

            # Self esteem (word spotting)
            (r'\b(self esteem|self worth|confidence|proud|ashamed|embarrassed)\b',
             ["How do you feel about yourself right now?",
              "What do you think has influenced your self-esteem?",
              "Can you recall a time when you felt really confident?"]),

            # Uncertainty
            (r'i don\'?t know',
             ["What do you feel uncertain about?",
              "Not knowing can be uncomfortable. Can you tell me more?",
              "What do you think is making this hard to understand?"]),
            
            # Denial
            (r'\b(never|not at all|no way|impossible)\b',
             ["Why do you feel that way?",
              "What makes you so sure about that?",
              "Can you think of any exceptions to that?"]),
            
            # Happiness (word spotting)
            (r'\b(happy|joyful|content|pleased|excited|glad)\b',
             ["That's great to hear! What is making you feel happy?",
              "How do you usually celebrate your happiness?",
              "Would you like to share more about what's bringing you joy?"])
        ]

        self.backups = [
            "Please tell me more.",
            "I'm not sure I understand you fully. Please elaborate.",
            "How does that make you feel?"
        ]
        
        self.redirections = [

            # suicidal thoughts
            (r'\b(kill myself|kms|suicide|suicidal|end it all)\b',
             ["I'm really sorry to hear that you're feeling this way. Please reach out to the Suicide Prevention Lifeline at 1-800-273-8255 or text HOME to 741741 to connect with a crisis counselor. You're not alone, and there are people who want to help you."]),

            # sexual assault
            (r'\b(rape|raped|sexually assaulted|sexual assault|molest|molested)\b',
             ["I'm sorry to hear that you've experienced this. You can contact the Rape, Abuse & Incest National Network (RAINN) at 1-800-656-4673 for support and assistance."]),

            # addiction
            (r'\b(addict|addiction|substance abuse|alcoholism|alcohol|drugs|drug abuse|relapse|relapsed|relapsing)\b',
             ["If you're struggling with addiction, consider reaching out to the Substance Abuse and Mental Health Services Administration (SAMHSA) National Helpline at 1-800-662-HELP (4357) for confidential support."]),

            # abuse
            (r'\b(abuse|abused|abusive|abuses|hit|hits|beaten|beating|beat|beats|hitting)\b',
             ["It sounds like you're going through a tough time. Please recognize that this is abuse. You can reach out to the National Domestic Violence Hotline at 1-800-799-7233 for help."])
        ]

        # grammar aware pronoun switches
        def pronoun_reflection(phrase):
            words = phrase.split()
            reflected_words = []
            prev_word = None

            for w in words:
                key = w.lower()
                # keep third person pronouns alone
                if key in ["he", "she", "they"]:
                    reflected_words.append(w)
                # switch first/second person pronouns
                elif key in self.pronouns:
                    reflected_word = self.pronouns[key]
                    # fix simple "am/is/are" grammar
                    if reflected_word in ["are", "am", "is"] and prev_word in ["I", "you", "he", "she", "they"]:
                        if reflected_word == "am" and prev_word == "you":
                            reflected_word = "are"
                        elif reflected_word == "are" and prev_word == "I":
                            reflected_word = "am"
                    reflected_words.append(reflected_word)
                else:
                    reflected_words.append(w)
                prev_word = reflected_words[-1]

            # fix possessive pronouns for third person
            i = 0
            while i < len(reflected_words) - 2:
                if reflected_words[i].lower() in ["he", "she", "they"]:
                    if reflected_words[i+1].lower() == "is":
                        adj = reflected_words[i+2].lower()
                        possessive = ""
                        new_word = adj

                        # determine possessive form
                        if reflected_words[i].lower() == "he":
                            possessive = "his"
                        elif reflected_words[i].lower() == "she":
                            possessive = "her"
                        else:
                            possessive = "their"

                        # convert adjective to noun if necessary
                        if adj == "angry":
                            new_word = "anger"
                        elif adj == "sad":
                            new_word = "sadness"
                        elif adj == "happy":
                            new_word = "happiness"

                        # replace the adjective with possessive + noun
                        reflected_words[i+2] = possessive + " " + new_word
                i += 1

            return ' '.join(reflected_words)

        def respond(user_input):
            # Check redirections first (crisis situations)
            for pattern, responses in self.redirections:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    response = random.choice(responses)
                    captured = [pronoun_reflection(match.group(i + 1)) for i in range(len(match.groups()))]
                    return response.format(*captured)

            # Check regular patterns
            for pattern, responses in self.patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    response = random.choice(responses)
                    captured = [pronoun_reflection(match.group(i + 1)) for i in range(len(match.groups()))]
                    return response.format(*captured)

            # Default backup response
            return random.choice(self.backups)

        # Bind nested functions to self so they are accessible as bot.respond() etc.
        self.pronoun_reflection = pronoun_reflection
        self.respond = respond


def main():
    print("Maria: Hello! I'm Maria. How can I help you today? (Type 'quit' to exit)")
    bot = Maria()

    while True:
        user_input = input("You: ")
        if re.search(r'\b(quit|exit|bye)\b', user_input, re.IGNORECASE):
            print("Maria: Goodbye! Take care.")
            break
        response = bot.respond(user_input)
        print(f"Maria: {response}")


if __name__ == "__main__":
    main()