from flask import Flask, request, jsonify
import utils
app = Flask(__name__)

@app.route('/record_data', methods=["POST"])
def record_data():
    user = request.json['user']
    email_id = request.json['email_id']
    utils.record_data(user, email_id)
    return jsonify({"status": 200})

if __name__ == '__main__':
    app.run()