# Eliza Chatbot Implementation
# This code implements a simple version of the Eliza chatbot, 
# which simulates a conversation by responding to user inputs with pre defined patterns and responses
# The chatbot uses pattern matching to identify keywords and generate appropriate replies
# uses regex

import re
import random

class Maria:
    def __init__(self):
        self.patterns = [

            # Exit / quit
            (r'\b(quit|exit|bye)\b',
             ["Thank you for talking with me.",
              "Goodbye. It was nice talking to you."]),

            # Greeting
            (r'\b(hello|hi|hey)\b',
             ["Hello. I'm glad you could drop by today.",
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

            # "I am ..."
            (r'i am (.*)',
             ["How long have you been {0}?",
              "Why do you say that you are {0}?",
              "How does being {0} affect you?"]),

            # "I can't ..."
            (r'i can\'?t (.*)',
             ["What makes it difficult for you to {0}?",
              "Have you tried to {0} before?",
              "What do you think would happen if you could {0}?"]),

            # Sadness (word spotting)
            (r'\bsad\b',
             ["I'm sorry you're feeling sad.",
              "What do you think is causing your sadness?",
              "Would you like to talk about what's making you feel this way?"]),

            # Anxiety / stress (word spotting)
            (r'\b(anxious|anxiety|stressed|stress|worried)\b',
             ["What usually triggers those feelings?",
              "How do you cope when you feel that way?",
              "Has this been affecting your daily life?"]),

            # Relationships / family (word spotting)
            (r'\b(mother|father|mom|dad|family|friend|partner)\b',
             ["Tell me more about that relationship.",
              "How does that relationship affect you?",
              "Does this relationship cause you stress?"]),

            # Uncertainty
            (r'i don\'?t know',
             ["What do you feel uncertain about?",
              "Not knowing can be uncomfortable. Can you tell me more?",
              "What do you think is making this hard to understand?"]),
        ]

        self.backups = [
            "Please tell me more.",
            "I'm not sure I understand you fully. Please elaborate.",
            "How does that make you feel?"
        ]

    def respond(self, user_input):
        for pattern, responses in self.patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                response = random.choice(responses)
                return response.format(
                    *[match.group(i + 1) for i in range(len(match.groups()))]
                )
        return random.choice(self.backups)


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
