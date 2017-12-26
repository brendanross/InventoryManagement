#inventory/utils.py
import json
import coreapi

#Authenticate User
def login_user(user, passphrase):
    auth = coreapi.auth.BasicAuthentication(
        username=user,
        password=passphrase
    )
    client = coreapi.Client(auth=auth)
    schema = client.get("http://35.227.154.9:8080/api-doc/")

    return client, schema
    
#Find Storage Locations
def get_locations():
    client = coreapi.Client()
    schema = client.get("http://35.227.154.9:8080/api-doc/")
    
    action = ["stock-location", "list"]
    params = {
        # "page": ,
        # "parent": ...,
    }
    result = client.action(schema, action, params=params)
    url_list = []
    name_list = []
    for item in result:
        url_list.append(item['url'])
        name_list.append(item['name'])
    
    return zip(url_list, name_list)

#Part must exist before stock can.
def create_part(request):
    client, schema = login_user('admin', 'Missmanticary!')
    
    action = ['part', 'create']
    params = {
        'name':request.POST['item'],
        'IPN':request.POST['SKU'], #Must be unique. SKU
        'description':request.POST['description'],
        'category':'http://35.227.154.9:8080/api/part-category/1'
    }
    result = client.action(schema, action, params=params)
    for item in result:
        part = result['url']
    return part
    
#Create New Item  
def create_stock(request):
    client, schema = login_user('admin', 'Missmanticary!')
    part = create_part(request)
    print(request.POST['location'])
    action = ["stock", "create"]
    params = {
        'quantity': request.POST['quantity'],
        'part': part,
        'location': request.POST['location'],
        'purchase_cost': request.POST['purchase_price'],
        'estimated_price': request.POST['expected_price'],
    }
    result = client.action(schema, action, params=params)