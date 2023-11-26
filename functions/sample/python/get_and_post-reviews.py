from cloudant.client import Cloudant
from cloudant.query import Query
from flask import Flask, abort, jsonify, request
import atexit

#Add your Cloudant service credentials here:
cloudant_username = '8263b58c-2acc-4424-974c-ef24dccbb5d9-bluemix'
cloudant_api_key = 'sFy_rwKmjdcGk6Y-YCRHf9zUbf6lnjR-sqB0e_-6OVVD'
cloudant_url = 'https://8263b58c-2acc-4424-974c-ef24dccbb5d9-bluemix.cloudantnosqldb.appdomain.cloud'
client = Cloudant.iam(cloudant_username, cloudant_api_key, connect=True, url=cloudant_url)

session = client.session()
print('Databases:', client.all_dbs())

db = client['reviews']

app = Flask(__name__)


# ********** 1 version (lab) to retrive reviews by 'id':
# @app.route('/api/get_reviews', methods=['GET'])
# def get_reviews():
#     dealership_id = request.args.get('id')

#     # Check if "id" parameter is missing
#     if dealership_id is None:
#         return jsonify({"error": "Missing 'id' parameter in the URL"}), 400

#     # Convert the "id" parameter to an integer (assuming "id" should be an integer)
#     try:
#         dealership_id = int(dealership_id)
#     except ValueError:
#         return jsonify({"error": "'id' parameter must be an integer"}), 400

#     # Define the query based on the 'dealership' ID
#     selector = {
#         # 'dealership': dealership_id      # before  
#         'id': dealership_id                # now
    
#     }

#     # Execute the query using the query method
#     result = db.get_query_result(selector)

#     # Create a list to store the documents
#     data_list = []

#     # Iterate through the results and add documents to the list
#     for doc in result:
#         data_list.append(doc)

#     # Return the data as JSON
#     return jsonify(data_list)

# ********** 2 version to retrive all reviews's object:

@app.route('/api/get_reviews', methods=['GET'])
def get_reviews():
    # Use all_docs to get all documents in the database
    result = db.all_docs(include_docs=True)

    # Create a list to store the documents
    data_list = []

    # Iterate through the results and add documents to the list
    for row in result['rows']:
        # Extract the document from the row
        doc = row['doc']
        data_list.append(doc)
    
    # Ya que 'data_list' se muestra de la forma [{}] el siguiente código transforma para que sea de 
    # la forma {"reviews": []} dicionaario para que pueda incluir la propiedad "reviews" que está 
    # parametrizada en 'resapis.py' y se pueda procesar como tal.
        reviewsDictionay = {"reviews" : data_list}


    # Return the data as JSON
    return jsonify(reviewsDictionay)

if __name__ == '__main__':
    app.run(debug=True)



# ******************************************************

@app.route('/api/post_review', methods=['POST'])
def post_review():
    if not request.json:
        abort(400, description='Invalid JSON data')
    
    # Extract review data from the request JSON
    review_data = request.json

    # Validate that the required fields are present in the review data
    required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
    for field in required_fields:
        if field not in review_data:
            abort(400, description=f'Missing required field: {field}')

    # Save the review data as a new document in the Cloudant database
    db.create_document(review_data)

    return jsonify({"message": "Review posted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)


    # To roun in locals

    # http://127.0.0.1:5000/api/get_reviews?id=1

    # http://localhost:5000/api/post_review

    