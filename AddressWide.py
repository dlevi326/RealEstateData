
import http.client 
import json
import pymongo
import time
import sys

conn = http.client.HTTPSConnection("api.gateway.attomdata.com") 
headers = { 
    'accept': "application/json", 
    'apikey': "ad59cc02e144aecc3c1e71338c751fcb", 
} 


try:
    conn_string = 'mongodb+srv://dlevi326:326%40Barr@cluster0-owylp.mongodb.net/test?retryWrites=true&w=majority'
    myclient = pymongo.MongoClient(conn_string)
    mydb = myclient["RealEstate"]
    mycol = mydb["AddressWideNew2"]
except Exception as e:
    print(e)

stateId = 'ST36' # New York
geoType = 'ZI' # Zip code



def get_addresses(conn, headers):
    # Got to page 40 (all pages)
    zipCode = ['11598','11096','11559']
    pageNumber = '1'
    pageSize = '100'
    totalPages = [4049,1847,2891]
    pageSection = [41,19,29]

    for z,p in zip(zipCode,pageSection):
        for i in range(p):
            print('Processing page: ',i,' out of ',p)
            try:
                query_string = 'https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/address?postalcode='+z+'&page='+str(i+1)+'&pagesize='+pageSize
                conn.request("GET", query_string, headers=headers) 
                res = conn.getresponse() 
                data = res.read() 

                results = json.loads(data.decode('utf-8'))['property']
            except Exception as e:
                print('Api error: ',e)
                break

            try:
                res = mycol.insert_many(results)
                print(res)
            
            except Exception as e:
                print('db error: ',e)
                if(str(e) != 'documents must be a non-empty list'):
                    break

            if(i%10==0):
                conn.close()
                print('sleeping...')
                sys.stdout.flush()
                time.sleep(65)
                conn = http.client.HTTPSConnection("api.gateway.attomdata.com") 

        


if __name__ == '__main__':
    get_addresses(conn,headers)
    print('done')