import discord  # api wrapper for the discord api 
import os  # to work with environment variables
import requests  # make a http request to api
import json  # to process data returned from api
import random # for bot to choose message randomly
from replit import db
from keep_alive import keep_alive # import the keep_alive function from the keep_alive.py file

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

# determine if bot will be responding to sad words 
if "responding" not in db.keys():
  db["responding"] = True

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

# before we add another command for the bot, let's add two helpful functions: add_helpful_message and del_helpful_message 
def add_encouragement(encouraging_message):
  # check if encouragements key is in database
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements  # save the updated list back to db
  else:
    db["encouragements"] = encouraging_message # create a new key value pair in db

def delete_encouragement(index):
  encouragements = db["encouragements"]
  # check if index is valid
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements  # update db 



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

  options = initial_encouragements
  # check to see if database has additional user added encouragements
  if "encouragements" in db.keys():
    options = options + list(db["encouragements"])  # concatenating two lists; repl.it stores list as ObservedList, so we need to cast it to list in order to use list concatenation

  if db["responding"]:
    # go through every `word` in `sad_words` and check if any of the current `word` is in the `msg`
    if any(word in msg for word in sad_words):
      # found a word in the sad_words list in the message
      await message.channel.send(random.choice(options))  # respond an encouraging message

  # detects to see if user wants to add a message 
  if msg.startswith('$add'):
    # parse msg so we don't add the command $new into our db
    # encouraging_message = msg.split(" ")[1:]
    encouraging_message = msg.split("$add ",1)[1] # a better approach that above
    # encouraging_message has a ObservedList type
    add_encouragement(encouraging_message) # this msg is added to the list of all encouraging message
    await message.channel.send("New encouraging message added.") # return message so user knows that the message is added 

  # check if user wants to delete a message, ex: $del 0
  if msg.startswith('$del'):
    # user passed in the index of the message it wants to delete
    encouragements = []  # this list will be returned to the user
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])  # get index user input; no need include space after command because we convert it to an integer
      delete_encouragement(index)
      encouragements = list(db["encouragements"])  # get the updated encouragements list to return to user
    await message.channel.send(encouragements)

  # check if user wants to list all encouragements
  if msg.startswith("$list"):
    encouragements = []  # because db could contain no encouragement 
    if "encouragements" in db.keys():
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)

  # check if user wants the bot to respond to sad words or not
  if msg.startswith("$responding"):
    # user input: $responding true / $responding false
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False  # if user enters anything but true set bot to not responding
      await message.channel.send("Responding is off.")

keep_alive()

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
3. when we receive a message, check the message to see if it contains sad words
4. use a database to store user submitted messages so user will be able to add more encouragement words for bot to display
5. repl uses a key-value store 
'''

# by default, every project on repl.it is public so everyone will be able to see secrets like password
# so we need to hide these secrets using environment variable

# 1. create a new file called .env
# 2. create a variable like TOKEN and assign the token to the variable
# 3. import the .env file into the code file that you want to use isinstance
# code: `import os`
# 4. access the token 
# code: `os.getenv('VAR_NAME')

# if the repl browser window is closed, the bot will stop running. 
# so, we have to setup a web server in repl, which will continue running even after the tab is 
# however, repl.it will only run the web server for an hour before sleeping if it receives no request.
# so a workaround is to use another app called UptimeRobot to ping the web server every say 5 minutes so repl will not sleep the web server

# 1. create another .py file and add flask code 
# 2. import the web server.py file into our bot's main.py file
# 3. run the function in the web server file to setup the web server
# 4. once the web server is running, get the url to the server
# 5. ping the url with UptimeRobot