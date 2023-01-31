import argparse
import os
import shutil

from flask import Flask, request, jsonify, make_response
from werkzeug.utils import secure_filename


app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, help='Port number to run the server on')

args = parser.parse_args()


@app.route('/file', methods=['POST'])
def upload_file():
    username = request.form['username']
    filename = request.form['filename']
    file = request.files['file']

    if file:
        chunk_filename = secure_filename(file.filename)

        if not os.path.exists('./storage/' + str(args.port)):
            os.makedirs('./storage/' + str(args.port))

        if not os.path.exists('./storage/' + str(args.port) + '/' + username):
            os.makedirs('./storage/' + str(args.port) + '/' + username)

        if not os.path.exists('./storage/' + str(args.port) + '/' + username + '/' + filename):
            os.makedirs('./storage/' + str(args.port) + '/' + username + '/' + filename)

        file.save(os.path.join(f'./storage/{str(args.port)}/{username}/{filename}/', chunk_filename))
        return jsonify({'message': 'File uploaded successfully'})


@app.route('/file/<filename>', methods=['DELETE'])
def delete_file(filename):
    username = request.form['username']
    shutil.rmtree('./storage/' + str(args.port) + '/' + username + '/' + filename)
    return jsonify({'message': 'File deleted successfully'}), 200


@app.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    username = request.form['username']
    index = request.form['index']
    with open(f'./storage/{str(args.port)}/{username}/{filename}/{filename}_{index}.txt', 'r') as f:
        file_data = f.read()
        return jsonify({'file_data': file_data}), 200


# @app.route('/status')
# def data_node_info():
#     memory = psutil.virtual_memory()
#     disk = psutil.disk_usage('/')
#     data_node_stas = {
#         'domain': 'http://127.0.0.1:' + str(args.port),
#         'cpu': psutil.cpu_percent(),
#         'memory': {
#             'total': memory.total >> 20,
#             'available': memory.available >> 20,
#             'used': memory.used >> 20
#         },
#         'disk': {
#             'total': disk.total >> 30,
#             'available': disk.free >> 30,
#             'used': disk.used >> 30
#         }
#     }
#     return jsonify(data_node_stas)


@app.route('/list-of-files/<username>', methods=['GET'])
def list_of_files(username):
    if os.path.exists('./storage/' + str(args.port) + '/' + username):
        files = os.listdir('./storage/' + str(args.port) + '/' + username)
        return jsonify(files), 200
    else:
        return make_response('', 204)


if __name__ == '__main__':
    app.run(port=args.port)
