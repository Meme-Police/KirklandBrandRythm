import json
import os
token = ""
try:
    # We can't include the contents of token.txt in the repository as it is private
     with open("token.txt") as file:
        token = file.read()
except FileNotFoundError as e:
    print(e)
