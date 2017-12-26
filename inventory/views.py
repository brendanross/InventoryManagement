#inventory/views.py
from django.shortcuts import render
import coreapi
from django.http import HttpResponse
import json
from .utils import *
#utility functions. Separate later.


# Create your views here.
def inventory_list(request):
    client = coreapi.Client()
    schema = client.get("http://35.227.154.9:8080/api-doc/")
    
    
    
    action = ["stock", "list"]
    params = {
        "page": '1',
        # "quantity": ...,
        # "part": ...,
        # "location": ...,
        # "min_stock": ...,
        # "max_stock": ...,
    }
    result = client.action(schema, action, params=params)
    
    #Iterates over list to access OrderedDict() object.
    for item in result:
        print(item['url'])
        print("--------------")
        
    ###Screwed this up. Just use the damn OrderedDict(...)
    ###by iterating the list.. 
    #Removes OrderedDict(...)
    #data = json.dumps(result)
    #Removes Unnecessary []
    #data = json.loads(data[1:-1])
    
    
    
    
    return render(request, 'inventory/createItem.html')

def new_item(request):
    if request.method == "POST":
        #make stuff
        create_stock(request)
        return HttpResponse("can't make it yet")
        
    else:
        location_list = get_locations()
        print(location_list)
        return render(request, 
            'inventory/createItem.html', 
            {
                'location_list' : location_list
            }
        )

    