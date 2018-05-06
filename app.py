from flask import Flask, jsonify, make_response
from recognize import get_user_images, search_collection

app = Flask(__name__)

@app.route('/fetch/<user_id>')
def fetch(user_id):
    return make_response(jsonify({
        'id': user_id
    }))

if __name__ == '__main__':
    app.run(debug=True)