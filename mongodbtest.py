from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
# %40 is @

# API key : 337cbe1c-328a-439b-8d9d-1db649b470ab
# conn_string : mongodb+srv://dlevi326:<password>@cluster0-owylp.mongodb.net/test?retryWrites=true&w=majority
conn_string = 'mongodb+srv://dlevi326:326%40Barr@cluster0-owylp.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(conn_string)
db=client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)