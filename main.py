import discord  # api wrapper for the discord api 
import os  # to work with environment variables
import requests  # make a http request to api
import json  # to process data returned from api
import random # for bot to choose message randomly

# create an instance of the client using methods from the discord.py library
# GENERAL STEP = (create a new object) using library func
client = discord.Client()

my_secret = os.environ['TOKEN']  # grab the token from environment variable

# words for bot to look out
sad_words = ["sad", "depressed", "unhappy", "anxious", "miserable", "worse", "depressing", "bad", "pissed", "unexceptable"]

# encouraging words for bot to reply when detects sad words
# its called initial because user will be able to add more encouragements to the bot in discord 
initial_encouragements = [
  "Cheer up!", 
  "Hang in there.",
  "You got this!"
]

# helper function 
def get_quote():
  # this function will be called to return an inspirational quote from an api

  # use the requests module to get the data from the api
  # this line makes a get request to the api 
  # GENERAL STEP: (create a new object) using library func
  response = requests.get("https://zenquotes.io/api/random")

  # convert response to json
  # GENERAL STEP: (create a new object) using library func
  json_data = json.loads(response.text)
  

  # access the specific quote from json object using specific KEY and save the value to the KEY to a new variable
  # GENERAL STEP: (create a new variable)
  quote = json_data[0]['q']

  # add author name to the quote 
  # which can be combined with line 28, but separate for learning sake
  # GENERAL STEP: (modify existing variable)
  quote += " -" + json_data[0]['a']

  return(quote)



# discord.py is an asynchronous library, so we need to work with callback
# callback = a function that is called when something else happens 

# we are writing callbacks below for the discord.py library to call 

# these function names are specifically form the discord.py library
# the library looks for different specific functions to know what to do when certain event happens

# use Client.event decorator to register an event 
@client.event 
async def on_ready():
  # this event happens (will be called) when the bot is ready to start being used 
  print('We have logged in as {0.user}'.format(client))

@client.event 
async def on_message(message):
  # we dont want this event to trigger if the message is from ourselves, the bot
  if message.author == client.user:
    return

  msg = message.content  # because we will use message.content many times so we create a variable for that value

  if msg.startswith('$hello'):
    # check to see if the message starts with a specific string (our command)
    # if true, the bot will response 'Hello!'
    await message.channel.send('Hello!')

  if msg.startswith('$inspire'):
    await message.channel.send(get_quote())

  # go through every `word` in `sad_words` and check if any of the current `word` is in the `msg`
  if any(word in msg for word in sad_words):
    # found a word in the sad_words list in the message
    await message.channel.send(random.choice(initial_encouragements))

# now we need to run the bot
# within the run method, we need to put our bot's token (password)
client.run(my_secret)

''' feature #1 
1. anyone should be able to add stuff for the bot to use 
2. the stuff that the user gives to the bot will be stored in a DATABASE, so those stuff will save even if you stop and start your bot!!!!!
'''
''' feature #2 
working with API 
1. import python modules: requests, json
2. add a get quote function
3. the bot will then call the function 

request module: allows our code to make a http request to get data from an api
json module: api returns a json, which this module will allow us to work with the json data returned by an api 
'''
''' feature #3
bot will recognize sad words that user typed and then reply with encouragement words
1. create a python list of sad words for the bot to look for
2. create a python list of encouragement words to reply 
3. (user will be able to add more encouragement words to the database)
4. when we receive a message, check the message to see if it contains sad words

'''

# by default, every project on repl.it is public so everyone will be able to see secrets like password
# so we need to hide these secrets using environment variable

# 1. create a new file called .env
# 2. create a variable like TOKEN and assign the token to the variable
# 3. import the .env file into the code file that you want to use isinstance
# code: `import os`
# 4. access the token 
# code: `os.getenv('VAR_NAME')