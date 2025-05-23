"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")  

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello(): 
    members=jackson_family.get_all_members()  
    response_body=members
    return jsonify(response_body),200

@app.route('/member', methods=['POST'])
def add_a_member(): 
    try: 
        request_body=request.get_json() 
        if not request_body: 
            return jsonify({"msg":"not request body"}),400
        jackson_family.add_member(request_body)
        return jsonify("member added"),200 
    except:
        return jsonify({"msg":"internal server error"}),500  
    
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id): 
    try: 
        member=jackson_family.get_member(id)
        if member: 
            return jsonify(member),200 
        else:
            return jsonify({"msg":"no member found"}),400 
    except:
        return jsonify({"msg":"internal server error"}),500
   



@app.route('/member/<int:id>', methods=['DELETE'])
def delete_a_member(id): 
    try: 
        deleted=jackson_family.delete_member(id)
        if not deleted:         
            return jsonify({'done':False}),400 
        return jsonify({'done':True}),200 
    except:
        return jsonify({"msg":"internal server error"}),500
   
   
    # # this is how you can use the Family datastructure by calling its methods
    # members = jackson_family.get_all_members()
    # response_body = {
    #     "hello": "world",
    #     "family": members
    # }



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)