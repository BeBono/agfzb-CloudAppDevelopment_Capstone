import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth


# (1/2) Method request es necesario para realizar la solitud del sub-siguiente bloque de código:

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data



# There are many ways to make HTTP requests in Django.
# Here we use a very popular and easy-to-use Python library called 'requests' that could be installed as a requirement.txt.

# The get_request method has two arguments, the URL to be requested, and a Python keyword arguments representing
# all URL parameters to be associated with the get call.

# The requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs) calls a GET method in requests library with a URL and any URL
# parameters such as 'dealerId' or 'state'.




# Request HTTP (This is subsecuence 2/2):
       

def get_dealers_from_cf(url, **kwargs):
    # arreglo que contendrá el resultado final
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the dealer list in JSON as dealers
        dealers = json_result["dealerships"]

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer  # Assuming each dealer is a dictionary
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

        
    return results
