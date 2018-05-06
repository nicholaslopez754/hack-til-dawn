from flask import Flask, jsonify, make_response
from recognize import get_user_images, search_collection, create_train_image
from config import raw_collection, similarity_threshold

application = Flask(__name__)

@application.route('/')
def root():
    return "Crowd Cam Server"

@application.route('/fetch/<user_id>')
def fetch(user_id):
    user_image_names = get_user_images(user_id)

    result_set = set()
    for image_name in user_image_names:
        train_img = create_train_image(image_name)
        matches = search_collection(train_img, raw_collection, similarity_threshold)['FaceMatches']
        for match in matches:
            result_set.add(match['Face']['ExternalImageId'])

    return make_response(jsonify({
        'results': list(result_set)
    }))

if __name__ == '__main__':
    application.run(debug=True)