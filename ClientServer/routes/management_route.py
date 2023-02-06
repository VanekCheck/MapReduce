import jwt
import requests
from flask import Blueprint, jsonify, request

from ClientServer.constants import MANAGEMENT_NODE_URL

data_node_route = Blueprint('route', __name__)


@data_node_route.route('', methods=['POST'])
def insert_data_node():
    address = request.json.get('address', None)
    url = f'{MANAGEMENT_NODE_URL}/data-node'
    data = {'address': address}
    requests.post(url, json=data)
    return jsonify({"message": "Successfully inserted"}), 200


@data_node_route.route('/<data_node_id>', methods=['DELETE'])
def delete_data_node(data_node_id):
    url = f'{MANAGEMENT_NODE_URL}/data-node/{data_node_id}'
    requests.delete(url)
    return jsonify({"message": "Successfully deleted"}), 200


@data_node_route.route('/all', methods=['GET'])
def get_all_data_nodes_request():
    url = f'{MANAGEMENT_NODE_URL}/data-node/all'
    response = requests.get(url)
    return jsonify(response.json()), 200
