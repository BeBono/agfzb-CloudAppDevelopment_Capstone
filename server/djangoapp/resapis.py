import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# (1/2) Method request es necesario para realizar la solitud de los sub-siguientes bloques de código:

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        # If any error occurs
        print("Exception occurred: {}".format(e))
        return None



# There are many ways to make HTTP requests in Django.
# Here we use a very popular and easy-to-use Python library called 'requests' that could be installed as a requirement.txt.

# The get_request method has two arguments, the URL to be requested, and a Python keyword arguments representing
# all URL parameters to be associated with the get call.

# The requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs) calls a GET method in requests library with a URL and any URL
# parameters such as 'dealerId' or 'state'.




# Request HTTP Dealer (2/2):
       
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




# Request HTTP Review (2/2):
# Este request obtiene el objeto JSON provisto por la URL en views.py 'def get_dealer_details'.  
# Este request también obtiene el segundo atributo llamado 'id' proveniente de views.py 'def get_dealer_details'
# El resultado de este request (filtro) es llamado por view.py dentro de 'def get_dealer_details' para ser presentado. En este caso,
# un filtro del atributo/propiedad 'review' del objeto/reviews de acuerdo al 'id' que concuerde con el id de la url (eje: http://127.0.0.1:8000/djangoapp/dealer/10).

def get_dealer_reviews_from_cf(url, id):
    # arreglo que contendrá el resultado final
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)

    # # Verificar si json_result tiene la clave "reviews"
    if "reviews" in json_result:
        # Filtrar las revisiones por el id proporcionado
        Result = [review["review"] for review in json_result["reviews"] if review["id"] == id]
        
        # Muestra el resultado sin comas ni corchetes:
        results.append(Result[0] if Result else "No se encontró la clave 'reviews' en json_result") 




    # Código adicional no usado pero pedido en el Lab:

    if json_result:
        # Get the review list in JSON as dealers_review
        dealers_review = json_result["reviews"]

        # For each review object
        for review in dealers_review:
            # Get its content in `doc` object
            review_doc = review  # Assuming each review is a dictionary
            # Create a CarReview object with values in `doc` object
            review_obj = DealerReview(
                id=review_doc["id"],
                name=review_doc["name"],
                dealership=review_doc["dealership"],
                review=review_doc["review"],
                purchase=review_doc["purchase"],
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_model"],
                car_year=review_doc["car_year"],
                # sentiment=review_doc["sentiment"]
            )
      
    # fin Código adicional no usado pero pedido en el Lab:        
            
            

    return results