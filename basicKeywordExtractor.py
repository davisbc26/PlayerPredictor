# HR: GitHub: https://github.com/Sakil786/Domain-Specific-Keyword-Extraction-using-Spacy
# HR: ChatGPT: For the purposes of troubling the Spacy import. My version of Python was too new for the import to run, also chatGPT to auto comment for my teammates to read

# Author: Benjamin Davis

import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# These are the necessary downloads
nltk.download('punkt_tab')  # Downloads the punkt tokenizer models
nltk.download('stopwords')  # Downloads the stopwords data

# This is the model for NER (Named Entity Recognition)
nlp = spacy.load("en_core_web_sm")

def extract_keywords(query):
    """
    This function takes a user query (about basketball player prediction)
    and returns a list of extracted keywords by tokenizing the query and removing common stopwords.
    It also performs Named Entity Recognition (NER) to extract entities like player names and teams.
    """
    # Tokenize the query using NLTK
    tokens = word_tokenize(query)
    
    # Get the set of stopwords in English (These stopwords are hardcoded, so in the future we can change this)
    stop_words = set(stopwords.words('english'))
    
    # Filter out stopwords and return the remaining tokens as keywords
    keywords = [word for word in tokens if word.lower() not in stop_words and word.isalnum()]

    # Perform NER
    doc = nlp(query)
    
    # Extract entities related to basketball (players, teams, etc.) (We may not use entities, but I figured we may need them)
    entities = [ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG']]  # 'PERSON' for player names, 'ORG' for organizations/teams
    
    return keywords, entities

# Insert Query (This is for the Checkpoint 2 Presentation)
query = input("Enter your query about the basketball player stats prediction: ")
keywords, entities = extract_keywords(query)

print("Extracted Keywords:", keywords)
print("Extracted Entities (e.g., players, teams):", entities)