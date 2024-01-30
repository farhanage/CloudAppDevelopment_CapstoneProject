from cloudant.client import Cloudant
from cloudant.query import Query
from flask import Flask, jsonify, request
import atexit

cloudant_username = "29c5ecb9-fb80-4cd1-b2c9-5b9a32bbb893-bluemix"
cloudant_api_key = "moe3l7eFLGr9Df8qanZRuQO-VY_lIfBkpmdf4TZp7bsJ"
cloudant_url = "https://29c5ecb9-fb80-4cd1-b2c9-5b9a32bbb893-bluemix.cloudantnosqldb.appdomain.cloud"

app = Flask(__name__)

@app.route('/api/review', methods=['GET','POST'])
def get_reviews():
    try:
        client = Cloudant.iam(
            account_name=cloudant_username,
            api_key=cloudant_api_key,
            connect=True,
            url=cloudant_url
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}, 500
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}, 500

    session = client.session()
    db = client['reviews']

    if request.method == 'GET':
        dealership_id = request.args.get('dealerId')
        if not dealership_id:
            return jsonify({"error": "Missing 'dealerId' parameter in the URL"}), 404
        
        dealership_id = int(dealership_id)
        selector = {
            'dealership': dealership_id
        }
        result = db.get_query_result(selector)
        data_list = []
        for doc in result:
            data_list.append(doc)

        if not len(data_list):
            return jsonify({"error": "dealerId does not exist"}), 404

        return jsonify(data_list)

    if request.method == 'POST':
        review_data = request.json

        if not request.json:
            jsonify({"error": "Missing JSON data to post"}), 404

        required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']

        for field in required_fields:
            if field not in review_data['review']:
                abort(404, description=f'Missing required field: {field}')

        db.create_document(review_data['review'])
        return jsonify({"message": "Review posted successfully"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)