# import only the classes/function you need
from flask import Flask
from threading import Thread  # the server will run on a separate thread from our bot

app = Flask('')

@app.route('/')
def home():
  return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)  # creating a new thread to run our server so both our bot and the server can be running at the same time
  t.start()