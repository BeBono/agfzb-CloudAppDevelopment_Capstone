# from imaplib import _Authenticator
import requests
import json
from .models import CarDealer, DealerReview
# from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# (1/2) Method-template request es necesario para realizar la solitud de los sub-siguientes bloques de código:

# def get_request(url, **kwargs):
#     print(kwargs)
#     print("GET from {} ".format(url))
#     try:

#         if api_key:
#         # Call get method of requests library with URL and parameters
        
#         # Basic authentication GET
#             response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
        
#         else:
#         # no authentication GET
#         # Call get method of requests library with URL and parameters
#             response = requests.get(url, headers={'Content-Type': 'application/json'},
#                                     params=kwargs)


#         status_code = response.status_code
#         print("With status {} ".format(status_code))
#         json_data = json.loads(response.text)
#         return json_data
#     except Exception as e:
#         # If any error occurs
#         print("Exception occurred: {}".format(e))
#         return None




# *****************************
# Lab Original by AI (1/2)

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

# *****************************

# There are many ways to make HTTP requests in Django.
# Here we use a very popular and easy-to-use Python library called 'requests' that could be installed as a requirement.txt.

# The get_request method has two arguments, the URL to be requested, and a Python keyword arguments representing
# all URL parameters to be associated with the get call.

# The requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs) calls a GET method in requests library with a URL and any URL
# parameters such as 'dealerId' or 'state'.




# Request HTTP Dealer short_name (2/2):
       
def get_dealers_from_cf(url, **kwargs):
    # arreglo que contendrá el resultado final
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the dealer list in JSON as dealers
        dealers = json_result["dealerships"]


        # The following code is use to loading data for ´CarDealer´ in model.py
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer  # Assuming each dealer is a dictionary: {"k":"v"}
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
            # print(dealer_obj)
      
    return results


# Get dealer name by id

def get_dealer_by_id_from_cf(url, id):
    results = []

    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            if dealer_doc["id"] == id:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], 
                                       city=dealer_doc["city"], 
                                       full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], 
                                       lat=dealer_doc["lat"], 
                                       long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"], 
                                       zip=dealer_doc["zip"])                    
                results.append(dealer_obj)
                print(dealer_doc)

    return results[0]


# Request HTTP Review (2/2):
# Este request obtiene el objeto JSON provisto por la URL en views.py 'def get_dealer_details'.  
# Este request también obtiene el segundo atributo llamado 'id' proveniente de views.py 'def get_dealer_details'
# El resultado de este request (filtro) es llamado por view.py dentro de 'def get_dealer_details' para ser presentado. En este caso,
# un filtro del atributo/propiedad 'review' del objeto/reviews de acuerdo al 'id' que concuerde con el id de la url (eje: http://127.0.0.1:8000/djangoapp/dealer/10).

# def get_dealer_reviews_from_cf(url, id):
#     # arreglo que contendrá el resultado final
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url, id=id)

#     # # Verificar si json_result tiene la clave "reviews"
#     if "reviews" in json_result:
#         # Filtrar las revisiones por el id proporcionado
#         Result = [review["review"] for review in json_result["reviews"] if review["id"] == id]
#         #Retrive the review text into [{´´}] that will be processed in resapis.py to be able to woring with Watson NLU that require type sting or text without "comillas" into a variable.
#         result_string = {Result[0]} if Result else "No se encontró la clave 'reviews' en json_result"

#         results.append(result_string)
#         # print(results)


# ***********************Lista de reviews según "id" coincidentes

def get_dealer_reviews_from_cf(url, id):
        # arreglo que contendrá el resultado final
    results = []
        # Call get_request with a URL parameter
    json_result = get_request(url, id=id)

    # Result = [review["review"] for review in json_result["reviews"] if review["id"] == id]
    Result = [review for review in json_result["reviews"] if review["id"] == id]
            # Almacenar todas las revisiones coincidentes en la lista results
    results.extend(Result)
    
    print(Result)


        #************************************** 

    # The following code is use to loading data for ´DealerReview´ in model.py for all reviews:

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
                # sentiment=review_doc["sentiment"]  // No used by staff instruccions (Rikkita) 
            )
                   
        
    return results



# Model as per IBM / Coursera forum:

def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/fb1caa68-eac5-4c0f-9e45-754e898db02e"
    api_key = "ydISe08oici-Hq2so_Ic47KGTF1KsxK4niyIYpZn_Qiv"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=dealerreview,features=Features(sentiment=SentimentOptions(targets=[dealerreview]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    # label = response['sentiment']

    
    # print(label)

    return(label)

# IBM Watson Natural Language Understanding (NLU):

# Cuando usas IBM Watson Natural Language Understanding (NLU) para analizar el sentimiento de un texto, obtendrás una respuesta en formato JSON que contiene información sobre el análisis realizado. La estructura de la respuesta puede variar según los parámetros que hayas configurado en tu solicitud, pero generalmente incluirá información sobre el sentimiento del texto.
# Aquí hay un ejemplo simplificado de cómo podría ser la respuesta:
# { "usage": { "text_units": 1, "text_characters": 44, "features": 1 }, "sentiment": { "document": { "score": 0.75, "label": "positive" } }, "language": "en" } 
# En este ejemplo:
# •	sentiment.document.score: Es un valor numérico que indica la puntuación de sentimiento del documento. Puede variar de -1 a 1, donde valores más cercanos a 1 indican un sentimiento más positivo y valores más cercanos a -1 indican un sentimiento más negativo.
# •	sentiment.document.label: Es una etiqueta que describe el sentimiento general del documento. Puede ser "positive", "negative" o "neutral".
# Estos son solo algunos de los campos posibles en la respuesta. Además del sentimiento, Watson NLU puede proporcionar información sobre entidades, conceptos, emociones, y más, dependiendo de cómo hayas configurado tus solicitudes.

# Related documentation:
# https://cloud.ibm.com/apidocs/natural-language-understanding?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMCD0321ENSkillsNetwork1046-2022-01-01&code=python#authentication
# Make sure import:
# from ibm_watson import NaturalLanguageUnderstandingV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions



# **************************** POST
def post_request(url, json_payload, **kwargs):
    url= "http://127.0.0.1:5000/api/post_review"
    response = requests.post(url, params=kwargs, json=json_payload)
    # response = requests.post(url, json=json_payload)
    return response
