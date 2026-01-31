# Maria Chatbot Implementation
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
        self.redirections = [

            # suicidal thoughts
            (r'\b(kill myself|kms|suicide|end it all)\b',)
            ["I'm really sorry to hear that you're feeling this way. Please reach out to the Suicide Prevention Lifeline at 1-800-273-8255 or text HOME to 741741 to connect with a crisis counselor. You're not alone, and there are people who want to help you."]

            # sexual assault
            (r'\b(rape|raped|sexually assaulted|sexual assault|molest|molested)\b',)
            ["I'm sorry to hear that you've experienced this. You can contact the Rape, Abuse & Incest National Network (RAINN) at 1-800-656-4673 for support and assistance."]

            # addiction
            (r'\b(addict|addiction|substance abuse|alcoholism|alcohol|drugs|drug abuse)\b',)
            ["If you're struggling with addiction, consider reaching out to the Substance Abuse and Mental Health Services Administration (SAMHSA) National Helpline at 1-800-662-HELP (4357) for confidential support."]

            # abuse
            (r'\b(abuse|abused|abusive)\b',)
            ["It sounds like you're going through a tough time. Please recognize that this is abuse. You can reach out to the National Domestic Violence Hotline at 1-800-799-7233 for help."]
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
