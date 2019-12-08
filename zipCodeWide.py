
import http.client 
import json
import pymongo

conn = http.client.HTTPSConnection("api.gateway.attomdata.com") 
headers = { 
    'accept': "application/json", 
    'apikey': "ad59cc02e144aecc3c1e71338c751fcb", 
} 


try:
    conn_string = 'mongodb+srv://dlevi326:326%40Barr@cluster0-owylp.mongodb.net/test?retryWrites=true&w=majority'
    myclient = pymongo.MongoClient(conn_string)
    mydb = myclient["RealEstate"]
    mycol = mydb["CountyWide"]
except Exception as e:
    print(e)

stateId = 'ST36' # New York



def get_counties():

    mydb = myclient['RealEstate']
    mycol = mydb['CountyWide']

    query_string = 'https://api.gateway.attomdata.com/areaapi/v2.0.0/county/lookup?StateId='+stateId
    conn.request("GET", query_string, headers=headers) 
    res = conn.getresponse() 
    data = res.read() 

    results = json.loads(data.decode('utf-8'))['response']['result']['package']['item']
    res = mycol.insert_many(results)
    print(res)


if __name__ == '__main__':
    get_counties()