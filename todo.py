#!/usr/bin/env pipenv run python

import sys
from pyfancy.pyfancy import pyfancy
from flata import Flata, where
from flata.storages import JSONStorage
db = Flata('db.json', storage=JSONStorage)
db.table('todos')

args = sys.argv

# usage represents the help guide
def usage():
  usageText = """
  todo helps you manage your todo tasks

  usage:
    todo <command>

  commands can be:

  new:      used to create a new todo
  get:      used to retrieve your todos
  complete: used to mark a todo as complete
  help:     used to print the usage guide
  """

  print(usageText)

# used to log errors to the console in red color
def errorLog(error):
  print(pyfancy().red(error).get())

def newTodo():
  print(pyfancy().blue("Type in your todo\n").get())
  for line in sys.stdin:
    db.get('todos').insert({
        'title': line.rstrip(),
        'complete': False
      })
    break

def getTodos():
  todos = db.get('todos')
  for todo in todos:
    todoText = str(todo["id"]) + ". " + todo["title"]
    if todo["complete"] == True:
      print(pyfancy().dim(todoText + ' ✔').get()) # add a check mark
    else:
      print(pyfancy().green(todoText).get())

def completeTodo():
  # check that length
  if len(args) != 3:
    errorLog("invalid number of arguments passed for complete command")
  else:
    try:

      # check if the value is a number
      n = int(args[2])
      todosLength = len(db.get('todos'))

      # check if the correct length of values has been passed
      if (n > todosLength):
        errorLog("invalid number passed for complete command")
      else:

        # update the todo item marked as complete
        db.get('todos').update({'complete': True}, where('id') == n)
    except ValueError:
      errorLog("please provide a valid number for complete command")

# we make sure the length of the arguments is exactly two
if len(args) > 2 and args[1] != "complete":
  errorLog("only one argument can be accepted")
  usage()
else:
  # check that the passed in command is one we recognize
  if len(args) > 1:
    arg = args[1]
    if arg == "help":
      usage()
    elif arg == "new":
      newTodo()
    elif arg == "get":
      getTodos()
    elif arg == "complete":
      completeTodo()
    else:
      errorLog("invalid command passed")
      usage()
