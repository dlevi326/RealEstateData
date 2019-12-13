
import http.client 
import json
import pymongo
import time
import sys


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass  

conn = http.client.HTTPSConnection("api.gateway.attomdata.com") 
headers = { 
    'accept': "application/json", 
    'apikey': "ad59cc02e144aecc3c1e71338c751fcb", 
} 


try:
    conn_string = 'mongodb+srv://dlevi326:326%40Barr@cluster0-owylp.mongodb.net/test?retryWrites=true&w=majority'
    myclient = pymongo.MongoClient(conn_string)
    mydb = myclient["RealEstate"]
    mycol = mydb["AddressWide"]
except Exception as e:
    print(e)

stateId = 'ST36' # New York
geoType = 'ZI' # Zip code

# 11598 - Woodmere Ny
# 11096 - Inwood ny
# 11559 - Lawrence ny


def get_addresses(conn,headers):
    # Got to page 999 (all pages)
    zipCode = ['11598','11096','11559']
    pageNumber = '1'
    pageSize = '100'
    totalPages = [4049,1847,2891]

    
    oldColName = 'AddressWideNew2'
    mycol = mydb[oldColName]
    addresses = mycol.find({'address.postal1':"11598"})
    newColName = 'PropertyTaxAssessmentsNew1'
    mycol = mydb['PropertyTaxAssessmentsNew1']

    for z in zipCode:
        conn.close()
        print('sleeping...')
        sys.stdout.flush()
        time.sleep(65)
        conn = http.client.HTTPSConnection("api.gateway.attomdata.com")

        mycol = mydb[oldColName]
        addresses = mycol.find({'address.postal1':z})
        print('Number of addresses found for zp: ',z,' is ',addresses.count())

        for i in range(addresses.count()):

            print('Processing page: ',i,' out of: ',addresses.count())
            
            try:
                #print(add[i])
                propId = addresses[i]['identifier']['obPropId']
                query_string = 'https://api.gateway.attomdata.com/propertyapi/v1.0.0/assessmenthistory/detail?id='+str(propId)
                conn.request("GET", query_string, headers=headers) 
                res = conn.getresponse() 
                data = res.read() 

                results = json.loads(data.decode('utf-8'))['property']
            except Exception as e:
                print('api error: ',e)
                break

            try:
                mycol = mydb[newColName]
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


'''
    for i in range(1000,totalPages):

        print('Processing page: ',i)
        
        try:
            #print(add[i])
            propId = addresses[i]['identifier']['obPropId']
            query_string = 'https://api.gateway.attomdata.com/propertyapi/v1.0.0/assessmenthistory/detail?id='+str(propId)
            conn.request("GET", query_string, headers=headers) 
            res = conn.getresponse() 
            data = res.read() 

            results = json.loads(data.decode('utf-8'))['property']
        except Exception as e:
            print('api error: ',e)
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
'''

        


if __name__ == '__main__':
    get_addresses(conn,headers)
    #print('done')