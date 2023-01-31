import math
import os
import shutil
import uuid
from flask import request, jsonify, Blueprint

import requests
from werkzeug.utils import secure_filename

from ClientServer.app.constants import urlAddresses
from ClientServer.app.helpers.auth import get_auth_header, get_user
from ClientServer.app.middleware import auth_middleware, error_handler
from ClientServer.app.models.File import insert_file_data, get_all_user_filenames, get_file_by_file_name, \
    delete_file_by_file_id
from ClientServer.app.models.Snippet import insert_snippet, delete_file_snippets, get_file_snippets

file_route = Blueprint('route', __name__)


@file_route.route('/list', methods=['GET'])
@auth_middleware
@error_handler
def list_of_user_files():
    try:
        user = get_user(request)
        filenames = get_all_user_filenames(user.id)
        return jsonify(filenames), 200

    except:
        return jsonify({'message': 'Something went wrong'}), 404


@file_route.route('', methods=['POST'])
@auth_middleware
def upload_file():
    # try:
    file = request.files['file']

    # TODO: move to middleware
    if not file:
        return jsonify({'message': 'File is required'}), 404

    session_id = str(uuid.uuid4())
    filename = secure_filename(file.filename).split('.')[0]

    headers = get_auth_header(request)

    list_of_files = requests.get(f'http://{request.host}/file/list', headers=headers).json()

    if filename in list_of_files:
        return jsonify({'message': 'File with such a name already exists'}), 404

    if not os.path.exists('temporary-folder'):
        os.makedirs('temporary-folder')

    os.makedirs('./temporary-folder/' + session_id)
    file.save(os.path.join('./temporary-folder/' + session_id, filename))

    file_total_size = os.path.getsize('./temporary-folder/' + session_id + '/' + filename)

    # define the size of each file
    separating_size = 1024  # lines

    with open('./temporary-folder/' + session_id + '/' + filename, 'r') as f:
        # read the contents of the file
        data = f.read()

    file_lines = data.splitlines()
    # get the number of lines in the file
    num_lines = len(file_lines)

    # calculate the number of files to be created
    num_files = math.ceil(num_lines / separating_size)

    user = get_user(request)

    file_data = insert_file_data(file_name=filename, path='./', user_id=user.id, size=file_total_size)

    # create the files
    for i in range(num_files):
        # open the file
        with open('./temporary-folder/' + session_id + '/' + filename + f'_{i}.txt', 'w') as f:

            # write the lines
            f.write('\n'.join(file_lines[i * separating_size:(i + 1) * separating_size]))

            files = {'file': open('./temporary-folder/' + session_id + '/' + filename + f'_{i}.txt', 'rb')}
            data = {'username': user.username, 'filename': filename}

            data_node_url = urlAddresses[i % len(urlAddresses)]

            url = f'{data_node_url}/file'

            message = requests.post(url, files=files, data=data)

            if message.status_code == 404:
                return jsonify({'message': 'Something went wrong'}), 404
            else:
                snippet_size = separating_size
                if i == num_files - 1:
                    snippet_size = num_lines % separating_size

                insert_snippet(file_id=file_data.id, data_node=data_node_url, index=i, size=snippet_size)

    shutil.rmtree('./temporary-folder/' + session_id)
    return jsonify({'message': 'File uploaded successfully'}), 200

    # except Exception as e:
    #     print(e)
    #     return jsonify({'message': 'Something went wrong'}), 404


@file_route.route('/<filename>', methods=['DELETE'])
@auth_middleware
def delete_file(filename):
    try:
        user = get_user(request)
        file = get_file_by_file_name(file_name=filename, user_id=user.id)

        data = {'username': user.username}
        for urlAddress in urlAddresses:
            url = f'{urlAddress}/file/{filename}'
            response = requests.delete(url, data=data)
            if response.status_code == 404:
                return jsonify({'message': 'Something went wrong'})

        delete_file_snippets(file_id=file.id)
        delete_file_by_file_id(file_id=file.id, user_id=user.id)

        return jsonify({'message': 'File deleted successfully'}), 200

    except:
        return jsonify({'message': 'Something went wrong'}), 400


@file_route.route('/<filename>', methods=['GET'])
@auth_middleware
def get_file(filename):
    # try:
    user = get_user(request)
    file = get_file_by_file_name(file_name=filename, user_id=user.id)
    snippets = get_file_snippets(file_id=file.id)

    file_snippets = []
    for snippet in snippets:
        data = {'username': user.username, 'index': snippet.index}
        url = f'{snippet.data_node}/file/{filename}'
        response = requests.get(url, data=data).json()
        file_data = response['file_data']
        file_snippets.append(file_data)

    headers = get_auth_header(request)
    requests.delete(f'http://{request.host}/file/{filename}', headers=headers)

    with open(f'../{filename}.txt', 'w') as f:
        f.write('\n'.join(file_snippets))

    return jsonify({'message': 'File received successfully'}), 200

    # except:
    #     return jsonify({'message': 'Something went wrong'}), 400

