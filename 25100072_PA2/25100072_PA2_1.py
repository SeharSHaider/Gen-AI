{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# PA2.1 - Building your first Chatbot: Aleeza\n",
    "\n",
    "### Introduction\n",
    "\n",
    "In this notebook, you will be implementing your own version of the first ever Chatbot, ELIZA.\n",
    "\n",
    "### Instructions\n",
    "\n",
    "- Follow along with the notebook, filling out the necessary code where instructed.\n",
    "\n",
    "- <span style=\"color: red;\">Read the Submission Instructions and Plagiarism Policy in the attached PDF.</span>\n",
    "\n",
    "- <span style=\"color: red;\">Make sure to run all cells for credit.</span>\n",
    "\n",
    "- <span style=\"color: red;\">Do not remove any pre-written code.</span> We will be using the `print` statements to grade your assignment.\n",
    "\n",
    "- <span style=\"color: red;\">You must attempt all parts.</span> Do not assume that because something is for 0 marks, you can leave it - it will definitely be used in later parts."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Background: ELIZA\n",
    "#### The first ever Chatbot.\n",
    "\n",
    "<div style=\"display: flex; justify-content: center;\">\n",
    "<img src=\"https://upload.wikimedia.org/wikipedia/commons/7/79/ELIZA_conversation.png\" width=\"400\" height=\"250\" alt=\"ELIZA Conversation\">\n",
    "</div>\n",
    "\n",
    "This Chatbot was released in 1966 (before the term Chatbot even existed) by Joseph Weizenbaum of MIT. This was a revolutionary program that allowed humans to converse with a computer. As you may have predicted, this was a retrieval-based system, very different from the \"language models\" of today. However, you may be surprised by how well it performed despite the simplicity of the system. Here is part of a conversation someone had with ELIZA, from the original paper (the capitalised sentences are ELIZA's responses):\n",
    "\\\n",
    "\\\n",
    "Men are all alike.\\\n",
    "IN WHAT WAY\\\n",
    "They're always bugging us about something or other.\\\n",
    "CAN YOU THINK OF A SPECIFIC EXAMPLE\\\n",
    "Well, my boyfriend made me come here.\\\n",
    "YOUR BOYFRIEND MADE YOU COME HERE\\\n",
    "He says i'm depressed much of the time.\\\n",
    "I AM SORRY TO HEAR YOU ARE DEPRESSED\\\n",
    "It's true. I am unhappy.\\\n",
    "DO YOU THINK COMING HERE WILL HELP YOU NOT TO BE UNHAPPY\\\n",
    "......\n",
    "\n",
    "The program used certain programmed rules to \"transform\" the input into the output. In order to do this, the program must first decompose the sentence based on certain criteria and then reassemble it based on the predefined assembly specifications. For example, if it is provided with the input sentence, \"It seems that you hate me\", it may be decomposed into:\n",
    "\n",
    "1) It seems that\n",
    "2) you\n",
    "3) hate\n",
    "4) me\n",
    "\n",
    "Of these, (2) and (4) are recognised as key words. The program can then use the remaining sections of the sentence based on pre-defined rules to construct an output. For example, it may be programmed with the rule:\n",
    "\n",
    "decomposition template:\\\n",
    "(0 YOU 0 ME)\\\n",
    "and the reassembly rule:\\\n",
    "(WHAT MAKES YOU THINK I 3 YOU).\n",
    "\n",
    "Here, the \"0\" represents any number of words, whereas the \"3\" represents the 3rd part of the sentence from before. Hopefully, this makes the implementation a little clearer. If not, don't worry as you'll understand how it works once you start implementing your own version!\n",
    "\n",
    "For more details on the original ELIZA implementation, [Click Here](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf).\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Specifications\n",
    "\n",
    "As described above, your task will be to first read in a user string, then modify it to provide an output (sometimes subtly, sometimes drastically, depending on the input string). This should be easy to do with the regex library, the specifics of which were discussed in class.\n",
    "\n",
    "\\\n",
    "Your program should be able to handle all 1st and 2nd person pronouns, all 1st and 2nd person subject-verb pairs with the verb be and all possible forms of the verb. If it is unclear what is meant by this, you might want to do some googling.\n",
    "\n",
    "\\\n",
    "An example is as follows:\n",
    "\n",
    "Regular Expression: I am (.*)\\\n",
    "Response: How long have you been %1?\n",
    "\n",
    "Example Input that matches: I am sad.\\\n",
    "Example Response: How long have you been sad?\n",
    "\n",
    "Please note that this is a simplified version of the chatbot, and the original bot had a much more complex algorithm behind it.\n",
    "\n",
    "You will have two tables to store all the logic of your bot:\n",
    "1. Reflection Table\n",
    "2. Response Table\n",
    "\n",
    "These will be described in detail in the cells below."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Imports\n",
    "\n",
    "These are the ONLY imports you can use for this part of the assignment."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "import re\n",
    "import random"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Tables\n",
    "\n",
    "These are your reflection and response tables."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Reflection Table\n",
    "\n",
    "This table serves to convert your pronouns from first person to second person and vice versa. You should list all forms of the pronouns and their corresponding \"reflection\". (eg. i : you)\\\n",
    "\\\n",
    "You should also do the same for all the forms of the verb \"be\". (eg. am : are)\\\n",
    "\\\n",
    "Note: You do not need to add plural pronouns such as \"we\".\\\n",
    "\\\n",
    "This table will be represented as a dictionary. (The first entry is listed as an example below)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [],
   "source": [
    "reflectionTable = {\n",
    "    \"i\": \"you\",\n",
    "    \"am\": \"are\",\n",
    "    \"my\": \"your\",\n",
    "    \"mine\": \"yours\",\n",
    "    \"me\": \"you\",\n",
    "    \"you\": \"I\",\n",
    "    \"are\": \"am\",\n",
    "    \"your\": \"my\",\n",
    "    \"yours\": \"mine\",\n",
    "    \"you're\": \"I'm\",\n",
    "    \"i'm\": \"you're\",\n",
    "    \"she\": \"her\",\n",
    "    \"he\" : \"him,\",\n",
    "    \"they\":\"them\"\n",
    "}\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Response Table\n",
    "\n",
    "This table is in the form of a nested list. Each entry is a list, with the first term being your regular expression and the second term being a list of possible responses. \"%n\" represents the nth match. You will need to handle this in your code later when replacing the relevant parts of the text.\n",
    "\n",
    "Since this is a fairly large table, you will fill out the regular expressions and the responses in a json file: \"responseTable.json\"\n",
    "\n",
    "\\\n",
    "In this table, you must include ALL subject-verb pairs for the verb \"be\". Do this for first, second and third person pronouns. (eg. I am ...) You must add at least 3 appropriate responses for each of these pairs. You need not account for the contracted versions of the pairs. But, DO include the corresponding question statements for each of these pairs. You can assume there will be no past-tense or future-tense inputs.\\\n",
    "\\\n",
    "Furthermore, in the case that you encounter no matches, you must have fallbacks. Due to this, you must also account for the following cases:\n",
    "1. (I feel ...), (I want ...), (I think ...)\n",
    "2. Subject with an unknown verb\n",
    "3. An unrecognised question\n",
    "4. Any string\n",
    "\n",
    "Include 4 or more responses for these cases as they will likely be encountered more often.\\\n",
    "\\\n",
    "Lastly, add at least 3 more subject-verb pairs, with at least 1 response each. These can be anything you like. Have fun with it (but keep it appropriate).\\\n",
    "\\\n",
    "For example:\n",
    "\n",
    "Regex: I voted for (.*)\n",
    "\n",
    "Response: How did voting for (.*) make you feel?\n",
    "\n",
    "Please ensure the correct order, as you will only be checking the first match later on.\\\n",
    "Once again, an example entry has been provided."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[{'regex': 'I am (.*)', 'responses': ['How long have you been %1?', 'What makes you %1?', 'Can you tell me more about being %1?']}, {'regex': 'you are (.*)', 'responses': ['Why do you think I am %1?', 'How does it feel to be %1?', 'Can you elaborate on why you think I am %1?']}, {'regex': 'he is (.*)', 'responses': ['What makes you say he is %1?', 'How do you feel about him being %1?', 'Can you provide more information about him being %1?']}, {'regex': 'she is (.*)', 'responses': ['Why do you believe she is %1?', 'How do you feel about her being %1?', 'Can you tell me more about her being %1?']}, {'regex': '(He|She|They|I) (.*) (the|a|an) (.*) (.*)', 'responses': ['Why do you think %1 %2 %3 %4 %5?', 'How does the %4 %5 affect %1?', 'Can you tell me more about why %1 %2 %3 %4 %5?']}, {'regex': 'I feel (.*)', 'responses': ['Why do you feel %1?', 'What caused you to feel %1?', 'How long have you been feeling %1?']}, {'regex': 'I want (.*)', 'responses': ['Why do you want %1?', 'How do you think %1 will benefit you?', 'Have you considered why you want %1?']}, {'regex': 'I think (.*)', 'responses': ['What leads you to think %1?', 'How long have you been thinking %1?', 'Have you considered other perspectives regarding %1?']}, {'regex': '(.*) is (.*),', 'responses': ['Why do you say %1 is %2?', 'How does %2 affect %1?', 'Can you provide more details about %1 being %2?']}, {'regex': '(.*) has (.*),', 'responses': ['Why do you think %1 has %2?', 'How does %2 impact %1?', 'Can you elaborate on %1 having %2?']}, {'regex': 'I like (.*)', 'responses': ['What do you like about %1?', 'How does %1 make you feel?', 'Can you explain why you like %1?']}, {'regex': 'I (.*) to (.*)', 'responses': ['What motivates you to %2?', 'How do you feel when you %2?', 'Have you considered the implications of %2?']}, {'regex': 'I (.*) (.*),', 'responses': ['Why do you %1 %2?', 'How does %2 affect you?', 'Can you tell me more about %1 %2?']}, {'regex': 'You (.*) (.*),', 'responses': ['Why do you think I %1 %2?', 'How does %2 make you feel?', 'Can you elaborate on why you think I %1 %2?']}, {'regex': '(.*) (?:feel|think|believe) (.*) about (.*)', 'responses': ['Why do you think %1 %2 about %3?', \"How does %3 affect %1's %2?\", \"Can you provide more details about %1's %2 about %3?\"]}, {'regex': '(.*) (?:feel|think|believe) (.*) (?:is|are) (.*)', 'responses': ['Why do you think %1 %2 %3?', \"How does %3 affect %1's %2?\", \"Can you provide more details about %1's %2 %3?\"]}, {'regex': 'How (.*) (?:feel|think|believe) (.*)', 'responses': ['Why are you interested in how %1 %2?', 'How does %2 affect %1?', 'Can you provide more details about how %1 %2?']}, {'regex': '(.*) is feeling (.*)', 'responses': ['Why do you think %1 is feeling %2?', 'How does %2 affect %1?', 'Can you tell me more about why %1 is feeling %2?']}, {'regex': 'you are (.*)', 'responses': ['Why do you think I am %1?', 'How does it feel to be %1?', 'Can you elaborate on why you think I am %1?']}, {'regex': 'Do you (like|not like|enjoy|dislike|prefer|hate) (.*)', 'responses': ['Why are you interested in whether I %1 %2?', 'How does %2 make you feel?', \"Can you elaborate on why you're asking if I %1 %2?\"]}, {'regex': 'do you (know|like|believe|think|dislike|hate) (he|she|they) (.*)', 'responses': ['Why are you interested in whether I %1 %2 %3?', 'How does %3 affect %2?', \"Can you elaborate on why you're asking if I %1 %2 %3?\"]}, {'regex': \"(I can't|I wasn't|I don't|I didn't|I haven't|I won't|I wouldn't|I couldn't) (.*)\", 'responses': [\"Why do you feel you can't %2?\", 'What prevented you from %2?', \"Can you tell me more about why you didn't %2?\"]}, {'regex': '.*', 'responses': [\"I'm not sure I understand. Can you provide more information?\", \"That's interesting. Tell me more about it\", \"I'm not familiar with that. Could you explain further?\"]}]\n"
     ]
    }
   ],
   "source": [
    "# Add entries in the JSON file\n",
    "\n",
    "responseTable = json.load(open('responseTable.json'))\n",
    "print(responseTable)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Helper Functions (Optional)\n",
    "\n",
    "If you wish to modularise your code to make your life simpler in the upcoming cells. Please define your helper functions here."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Code here"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Aleeza Class\n",
    "\n",
    "This is the class you will be implementing all of your bot's functionality in. As you will see, this is very straightforward and most of the actual work will be done while writing the response table. We will call our version Aleeza."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Aleeza:\n",
    "    def __init__(self, reflectionTable, responseTable):\n",
    "        \"\"\"\n",
    "        Initialize your bot by storing both the tables as instance variables.\n",
    "        You can store them any way you want. (Dictionary, List, etc.)\n",
    "        \"\"\"\n",
    "        self.reflectionTable = reflectionTable\n",
    "        self.responseTable = responseTable\n",
    "\n",
    "    def reflect(self, text):\n",
    "        \"\"\"\n",
    "        Take a string and \"reflect\" based on the reflectionTable.\n",
    "\n",
    "        Return the modified string.\n",
    "        \"\"\"\n",
    "        words = text.lower().split()\n",
    "        # switches words according to reflection Table if it exists\n",
    "        reflected_words = [self.reflectionTable[word] if word in self.reflectionTable else word for word in words]\n",
    "        return ' '.join(reflected_words)\n",
    "\n",
    "    def respond(self, text):\n",
    "        \"\"\"\n",
    "        Take a string, find a match, and return a randomly\n",
    "        chosen response from the corresponding list.\n",
    "\n",
    "        Do not forget to \"reflect\" appropriate parts of the string.\n",
    "\n",
    "        If there is no match, return None.\n",
    "        \"\"\"\n",
    "        text = text.lower()\n",
    "        \n",
    "        for entry in self.responseTable:\n",
    "            regex = entry['regex'].lower()\n",
    "            responses = entry['responses']\n",
    "            match = re.match(regex, text) # match regex string with text\n",
    "            if match:\n",
    "                groups = match.groups()\n",
    "                # Reflect the groups\n",
    "                reflected_groups = [self.reflect(group) for group in groups]\n",
    "                # Choose a random response\n",
    "                response = random.choice(responses)\n",
    "                # Replace %n in response with reflected groups\n",
    "                for i, reflected_group in enumerate(reflected_groups):\n",
    "                    response = response.replace(f\"%{i+1}\", reflected_group)\n",
    "                return response\n",
    "        return None\n",
    "\n",
    "    \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Test your Bot\n",
    "\n",
    "You can use this interface to manually check your bot's responses."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [],
   "source": [
    "def command_interface():\n",
    "    print('Aleeza\\n---------')\n",
    "    print('Talk to the program by typing in plain English.')\n",
    "    print('='*72)\n",
    "    print('Hello.  How are you feeling today?')\n",
    "\n",
    "    s = ''\n",
    "    therapist = Aleeza(reflectionTable, responseTable)\n",
    "    while s != 'quit':\n",
    "        try:\n",
    "            s = input('> ')\n",
    "        except EOFError:\n",
    "            s = 'quit'\n",
    "        print(s)\n",
    "        while s[-1] in '!.':\n",
    "            s = s[:-1]\n",
    "        print(therapist.respond(s))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Aleeza\n",
      "---------\n",
      "Talk to the program by typing in plain English.\n",
      "========================================================================\n",
      "Hello.  How are you feeling today?\n",
      "i feel happy\n",
      "How long have you been feeling happy?\n",
      "she likes oranges\n",
      "I'm not sure I understand. Can you provide more information?\n",
      "I like orages\n",
      "How does orages make you feel?\n",
      "quit\n",
      "I'm not sure I understand. Can you provide more information?\n"
     ]
    }
   ],
   "source": [
    "command_interface()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Test Sentences\n",
    "\n",
    "After testing your bot, you have likely seen that it does not work very well yet. This goes to show the immense amount of work that was put into the original ELIZA program.\\\n",
    "In any case, having concocted all of your (hopefully) appropriate responses, you now need to demonstrate your bot handling all the cases listed above. To do this, you must provide an example sentence handling each of the regular expressions you have listed in your response table."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [],
   "source": [
    "test_sentences = [\n",
    "    \"I am feeling happy today.\",\n",
    "    \"You are very kind.\",\n",
    "    \"He is a talented musician.\",\n",
    "    \"She is feeling sad about the news.\",\n",
    "    \"I like to read books.\",\n",
    "    \"You think he is a good friend.\",\n",
    "    \"Do you like pizza?\",\n",
    "    \"I don't think I can do it.\",\n",
    "    \"I wasn't expecting this outcome.\",\n",
    "    \"Can you help me with my homework?\",\n",
    "    \"I can't believe you said that.\",\n",
    "    \"I feel tired after work.\",\n",
    "    \"You know he likes to play basketball.\",\n",
    "    \"How do you feel about the weather?\",\n",
    "    \"What do you think about the new movie?\"\n",
    "]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_responses(sentence_list, bot):\n",
    "    \"\"\"\n",
    "    Get a response for each sentence from the list and return as a list.\n",
    "    \"\"\"\n",
    "    responses = []\n",
    "    for sentence in sentence_list:\n",
    "        response = bot.respond(sentence)\n",
    "        responses.append(response)\n",
    "    return responses\n",
    "\n",
    "    # Code here"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "========================================================================\n",
      "I am feeling happy today.\n",
      "How long have you been feeling happy today.?\n",
      "========================================================================\n",
      "You are very kind.\n",
      "Why do you think I am very kind.?\n",
      "========================================================================\n",
      "He is a talented musician.\n",
      "What makes you say he is a talented musician.?\n",
      "========================================================================\n",
      "She is feeling sad about the news.\n",
      "Can you tell me more about her being feeling sad about the news.?\n",
      "========================================================================\n",
      "I like to read books.\n",
      "What do you like about to read books.?\n",
      "========================================================================\n",
      "You think he is a good friend.\n",
      "How does a good friend. affect I's him,?\n",
      "========================================================================\n",
      "Do you like pizza?\n",
      "Can you elaborate on why you're asking if I like pizza??\n",
      "========================================================================\n",
      "I don't think I can do it.\n",
      "Why do you feel you can't think you can do it.?\n",
      "========================================================================\n",
      "I wasn't expecting this outcome.\n",
      "What prevented you from expecting this outcome.?\n",
      "========================================================================\n",
      "Can you help me with my homework?\n",
      "I'm not sure I understand. Can you provide more information?\n",
      "========================================================================\n",
      "I can't believe you said that.\n",
      "Can you tell me more about why you didn't believe I said that.?\n",
      "========================================================================\n",
      "I feel tired after work.\n",
      "Why do you feel tired after work.?\n",
      "========================================================================\n",
      "You know he likes to play basketball.\n",
      "I'm not sure I understand. Can you provide more information?\n",
      "========================================================================\n",
      "How do you feel about the weather?\n",
      "How does about the weather? affect do I?\n",
      "========================================================================\n",
      "What do you think about the new movie?\n",
      "That's interesting. Tell me more about it\n"
     ]
    }
   ],
   "source": [
    "therapist = Aleeza(reflectionTable, responseTable)\n",
    "\n",
    "for pair in zip(test_sentences, get_responses(test_sentences, therapist)):\n",
    "    print('='*72)\n",
    "    print(pair[0])\n",
    "    print(pair[1])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Giving Aleeza Emotional Intelligence\n",
    "\n",
    "In the next part of the assignment, you will be giving your chatbot some emotional intelligence. This will be done by training a simple emotion classification model. You will then use this model to classify the sentiment of the user's input and respond accordingly.\\\n",
    "\\\n",
    "How our logic will work is as follows:\n",
    "1. If there is a match in the response table, we will use the response from the table.\n",
    "2. If there is no match, we will classify the emotion of the input and respond accordingly.\n",
    "\n",
    "The model we will use is a simple Naive Bayes Classifier. This is a simple model that works well with text data. You will be using the `scikit-learn` library to train the model, and the huggingface `datasets` library to get the data."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Imports\n",
    "\n",
    "These are the ONLY imports you can use for this part of the assignment."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {},
   "outputs": [],
   "source": [
    "import datasets\n",
    "import sklearn\n",
    "from sklearn.feature_extraction.text import CountVectorizer\n",
    "from sklearn.naive_bayes import MultinomialNB\n",
    "from sklearn.pipeline import make_pipeline\n",
    "from sklearn.metrics import classification_report"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Dataset\n",
    "\n",
    "We will be using the `emotion` dataset from the `datasets` library. This dataset contains text data and the corresponding emotion. You will use this data to train your model. Load this dataset using the `load_dataset` function from the `datasets` library.\n",
    "\n",
    "Next, split the dataset into training and testings sets.\\\n",
    "(HINT: This has already been done for you in the dataset you loaded)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DatasetDict({\n",
       "    train: Dataset({\n",
       "        features: ['text', 'label'],\n",
       "        num_rows: 16000\n",
       "    })\n",
       "    validation: Dataset({\n",
       "        features: ['text', 'label'],\n",
       "        num_rows: 2000\n",
       "    })\n",
       "    test: Dataset({\n",
       "        features: ['text', 'label'],\n",
       "        num_rows: 2000\n",
       "    })\n",
       "})"
      ]
     },
     "execution_count": 39,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\"\"\"\n",
    "Load the emotion dataset from Hugging Face\n",
    "\"\"\"\n",
    "import pandas as pd \n",
    "from datasets import load_dataset\n",
    "\n",
    "dataset = load_dataset(\"dair-ai/emotion\", trust_remote_code=True)\n",
    "\n",
    "dataset"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Train DataFrame:\n",
      "                                                text  label\n",
      "0                            i didnt feel humiliated      0\n",
      "1  i can go from feeling so hopeless to so damned...      0\n",
      "2   im grabbing a minute to post i feel greedy wrong      3\n",
      "3  i am ever feeling nostalgic about the fireplac...      2\n",
      "4                               i am feeling grouchy      3\n",
      "\n",
      "Test DataFrame:\n",
      "                                                text  label\n",
      "0  im feeling rather rotten so im not very ambiti...      0\n",
      "1          im updating my blog because i feel shitty      0\n",
      "2  i never make her separate from me because i do...      0\n",
      "3  i left with my bouquet of red and yellow tulip...      1\n",
      "4    i was feeling a little vain when i did this one      0\n"
     ]
    }
   ],
   "source": [
    "\"\"\"\n",
    "Split the dataset into training and testing sets\n",
    "\"\"\"\n",
    "\n",
    "# Load train split into a pandas DataFrame\n",
    "train_df = pd.DataFrame(dataset['train'])\n",
    "print(\"Train DataFrame:\")\n",
    "print(train_df.head())\n",
    "\n",
    "# Load test split into a pandas DataFrame\n",
    "test_df = pd.DataFrame(dataset['test'])\n",
    "print(\"\\nTest DataFrame:\")\n",
    "print(test_df.head())\n",
    "\n",
    "\n",
    "# Code below\n",
    "train_data = train_df['text']\n",
    "train_labels = train_df['label']\n",
    "test_data = test_df['text']\n",
    "test_labels = test_df['label']"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Training the Model\n",
    "\n",
    "Just like in your previous assignment, you will now train the model and evaluate it."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       0.77      0.93      0.84       581\n",
      "           1       0.77      0.96      0.86       695\n",
      "           2       0.87      0.33      0.48       159\n",
      "           3       0.92      0.66      0.77       275\n",
      "           4       0.85      0.64      0.73       224\n",
      "           5       1.00      0.08      0.14        66\n",
      "\n",
      "    accuracy                           0.79      2000\n",
      "   macro avg       0.86      0.60      0.64      2000\n",
      "weighted avg       0.81      0.79      0.77      2000\n",
      "\n"
     ]
    }
   ],
   "source": [
    "\"\"\"\n",
    "Vectorise the data and train the model\n",
    "\"\"\"\n",
    "vectorizer = CountVectorizer(stop_words='english')\n",
    "train_data = vectorizer.fit_transform(train_data)\n",
    "test_data = vectorizer.transform(test_data)\n",
    "\n",
    "# Initialize and fit the Multinomial Naive Bayes model\n",
    "nb_model_sklearn = MultinomialNB()\n",
    "nb_model_sklearn.fit(train_data, train_labels)\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "Predict on the test set\n",
    "\"\"\"\n",
    "\n",
    "predicted_labels =  nb_model_sklearn.predict(test_data)\n",
    "\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "Print classification report\n",
    "\"\"\"\n",
    "print(classification_report(test_labels, predicted_labels))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Putting it all together\n",
    "\n",
    "Now that we have our classification model, we can modify our chatbot to use it.\n",
    "\n",
    "First, we will remove the fallback responses from our response table, i.e. the following cases:\n",
    "1. (I feel ...), (I want ...), (I think ...)\n",
    "2. Subject with an unknown verb\n",
    "3. An unrecognised question\n",
    "4. Any string\n",
    "\n",
    "Remove these and save your response table as \"responseTable2.json\"."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Make a new file \"responseTable2.json\" and add your modified table to it\n",
    "\n",
    "responseTable = json.load(open('responseTable2.json'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Emotion Response Table\n",
    "\n",
    "This table will be a dictionary with the emotions as keys and a list of possible responses as values. You should include at least 2 responses for each emotion."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [],
   "source": [
    "emotionTable = {\n",
    "    0: [ # sadness\n",
    "        \"I'm sorry to hear that. Is there anything specific that's making you feel sad?\",\n",
    "        \"It's okay to feel sad sometimes. Would you like to talk about what's on your mind?\"\n",
    "    ], \n",
    "    1: [ # joy\n",
    "        \"That's wonderful! What's bringing you joy today?\",\n",
    "        \"I'm glad to hear you're feeling joyful. What's making you happy?\"\n",
    "    ],\n",
    "    2: [ # love\n",
    "        \"Love is a beautiful thing. Who or what are you feeling love towards?\",\n",
    "        \"Feeling love is amazing. What's making you feel this way?\"\n",
    "    ],\n",
    "    3: [ # anger\n",
    "        \"It sounds like you're feeling angry. Would you like to talk about what's bothering you?\",\n",
    "        \"Anger is a powerful emotion. What's causing you to feel this way?\"\n",
    "    ],\n",
    "    4: [ # fear\n",
    "        \"I understand feeling afraid. Is there something specific that's causing you fear?\",\n",
    "        \"Fear can be overwhelming. Would you like to explore what's triggering your fear?\"\n",
    "    ],\n",
    "    5: [ # surprise\n",
    "        \"That's unexpected! What surprised you?\",\n",
    "        \"Surprises can be exciting. What caught you off guard?\"\n",
    "    ]\n",
    "}\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Modifying your Chatbot\n",
    "\n",
    "You will now modify your chatbot to use the emotion classifier. If there is a match in the response table, we will use the response from the table. If there is no match, we will classify the emotion of the input and respond accordingly."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {},
   "outputs": [],
   "source": [
    "class IntelligentAleeza(Aleeza):\n",
    "    def __init__(self, reflectionTable, responseTable, emotionTable, classifier):\n",
    "        \"\"\"\n",
    "        Initialise your bot by calling the parent class's __init__ method,\n",
    "        and then storing the emotionTable as an instance variable.\n",
    "\n",
    "        Next, store the classification model as an instance variable.\n",
    "        \"\"\"\n",
    "        super().__init__(reflectionTable, responseTable)\n",
    "        self.emotionTable = emotionTable\n",
    "        self.classifier = classifier\n",
    "        # Code here\n",
    "\n",
    "    def smart_respond(self, text):\n",
    "        \"\"\"\n",
    "        Take a string, call the parent class's respond method.\n",
    "        If the response is None, then respond based on the emotion.\n",
    "        \"\"\"\n",
    "        \n",
    "        response = super().respond(text)\n",
    "        # print(f'TEXT-- {text}')\n",
    "        if response is None:\n",
    "                \n",
    "            # Transform the text using the vectorizer\n",
    "            text_vectorized = vectorizer.transform([text])[0]\n",
    "            # print(\"Original Text:\", text)\n",
    "            # print(\"Vectorized Text:\", text_vectorized)\n",
    "            \n",
    "            # Predict the emotion using the classifier\n",
    "            emotion = self.classifier.predict(text_vectorized)\n",
    "            emotion = emotion[0]\n",
    "            # print(\"Predicted Emotion:\", emotion)\n",
    "            # print()\n",
    "\n",
    "            if emotion in self.emotionTable:\n",
    "                response = random.choice(self.emotionTable[emotion])\n",
    "        return response\n",
    "        # Code here"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Test your New Bot\n",
    "\n",
    "Randomly select 5 sentences from the test set and test your bot. You should see that it now responds with an appropriate message based on the emotion detected in the input (when there is no match)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_responses(sentence_list, bot):\n",
    "    \"\"\"\n",
    "    Get a response for each sentence from the list and return as a list.\n",
    "    Use your new smart_respond method.\n",
    "    \"\"\"\n",
    "    responses = []\n",
    "    for sentence in sentence_list:\n",
    "        response = bot.smart_respond(sentence)\n",
    "        responses.append(response)\n",
    "    return responses\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "========================================================================\n",
      "i was having an awful year racing and was feeling exhausted all the time\n",
      "It's okay to feel sad sometimes. Would you like to talk about what's on your mind?\n",
      "========================================================================\n",
      "i feel like my sweet company is finally coming together\n",
      "That's wonderful! What's bringing you joy today?\n",
      "========================================================================\n",
      "i forgive myself that i have accepted and allowed myself to think that as i am writing this blog that someone will feel sorry for me give me some sympathy and tell me i am right\n",
      "I'm glad to hear you're feeling joyful. What's making you happy?\n",
      "========================================================================\n",
      "i know its easy to feel a little envious of me and i cant tell you that you shouldnt\n",
      "It sounds like you're feeling angry. Would you like to talk about what's bothering you?\n",
      "========================================================================\n",
      "i got home and told peter how i was feeling he wasnt shocked at all by what i was telling him\n",
      "I'm glad to hear you're feeling joyful. What's making you happy?\n"
     ]
    }
   ],
   "source": [
    "\"\"\"\n",
    "Create an instance of the IntelligentAleeza class\n",
    "\"\"\"\n",
    "intelligent_therapist = IntelligentAleeza(reflectionTable, responseTable, emotionTable, nb_model_sklearn)\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "Get 5 random test instances from the test data\n",
    "\"\"\"\n",
    "\n",
    "# Code here\n",
    "test_instances = test_df['text'].sample(5).values\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\"\"\" \n",
    "Get responses from the intelligent_therapist \n",
    "\"\"\"\n",
    "\n",
    "responses = get_responses(test_instances, intelligent_therapist)\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "Print the test instances and the responses\n",
    "\"\"\"\n",
    "for pair in zip(test_instances, responses):\n",
    "    print('='*72)\n",
    "    print(pair[0])\n",
    "    print(pair[1])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Fin."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
