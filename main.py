from flask import Flask, Blueprint, request, jsonify
from networkinfo import Ipinfo

app_bp = Blueprint('api', __name__, url_prefix='/api')

@app_bp.route('/', methods=['GET'])
def greeting():
    return jsonify({"message": "Welcome to the personal assistant api!"}), 200

@app_bp.route('/ipinfo', methods=['GET'])
def ipInfo():
    clientIP = request.remote_addr
    ipinfo_obj = Ipinfo(clientIP) 
    ipinfo = ipinfo_obj.getInfo()

    return jsonify({"ip": ipinfo['ip'], "city": ipinfo['city'], "country": ipinfo['country']}), 200

@app_bp.route('/ipinfo/<ip>', methods=['GET'])
def externalipInfo(ip):
    externalipInfo = Ipinfo(ip)
    ipinfo = externalipInfo.getInfo()

    return jsonify({"ip": ipinfo['ip'], "city": ipinfo['city'], "country": ipinfo['country']}), 200

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(app_bp)
    app.run(debug=True, host="127.0.0.1", port="8000")
