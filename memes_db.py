import os, sqlite3

connection = sqlite3.connect(os.getcwd() + "/memes.sqlite3")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
