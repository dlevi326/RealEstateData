
import http.client 
import json
import pymongo

conn = http.client.HTTPSConnection("api.gateway.attomdata.com") 
headers = { 
    'accept': "application/json", 
    'apikey': "ad59cc02e144aecc3c1e71338c751fcb", 
} 



conn_string = 'mongodb+srv://dlevi326:326%40Barr@cluster0-owylp.mongodb.net/test?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(conn_string)
mydb = myclient["RealEstate"]
mycol = mydb["test"]
#mydict = {'test':1,'test2':'hi'}
#x = mycol.insert_one(mydict)
#print(x)




def get_states():
    return
    mydb = myclient['RealEstate']
    mycol = mydb['StateWide']

    query_string = 'https://api.gateway.attomdata.com/areaapi/v2.0.0/state/lookup'
    conn.request("GET", query_string, headers=headers) 
    res = conn.getresponse() 
    data = res.read() 

    results = json.loads(data.decode('utf-8'))['response']['result']['package']['item']

    for state in results:
        res = mycol.insert_one(state)
        print(res)

if __name__ == '__main__':
    get_states()