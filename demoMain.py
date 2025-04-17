import basicKeywordExtractor
import espnBasicWebcrawler
import espnBasicRawDataCleanerAndPromptGenerator

query = input('Please enter your query about basketball player performace')

keywords, entities = basicKeywordExtractor.extract_keywords(query)

keywords.append(['Points', 'Rebounds', 'Assists', 'Steals', 'Blocks'])



'''

COA

1. build complete working demo
2. develop webcrawler that is not susceptible to IP-blocking (try using selenium, and less efficent is okay in this case)
    - for ESPN, Twitter, and Instagram
3. use AI to generate a prompt from the webcrawler
    - prompt need to have past information on the player
    - prompt then need the social media information of the player
4. build the file that uses the LLM to make a prediction

'''

