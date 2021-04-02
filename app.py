from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from azure.cosmos import CosmosClient, exceptions, PartitionKey
import os
import json

app = Flask(__name__)
CORS(app)

@app.route("/getPrediction/<user_id>",methods=['GET'])
def getPrediction(user_id):
    url = "https://adbms-cosmos.documents.azure.com:443/"
    key = 'MjyGDQH9W1ZRAPUkhDzSyKHhPQS3nmUIXOm2MpE8tIDx7EYXx5sLkBkpWXUUoAlfVHDXZzcQm461NTyUU2GUmA=='
    client = CosmosClient(url, credential=key)
    database_name = 'HDIdatabase'
    database = client.get_database_client(database_name)
    container_name = 'ProductRecommendations'
    container = database.get_container_client(container_name)
    str_user = "user_"+user_id
    result = []
    for item in container.query_items( query='SELECT * FROM c["%s"]'%(str_user), enable_cross_partition_query=True):
        result = item
    
    return {"message":"Prediction Data from UserId", "prediction_data":result}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)