from flask import Flask, Blueprint, request, jsonify, Response
from networkinfo import Ipinfo
from portchecker import Checkport
from dnschecker import DNSChecker
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

app_bp = Blueprint('api', __name__, url_prefix='/api')

# Define a Prometheus Counter
REQUEST_COUNT = Counter('http_requests_total', 'HTTP requests total', ['method', 'endpoint', 'status_code'])

@app_bp.route('/', methods=['GET'])
def greeting():
    REQUEST_COUNT.labels(method='GET', endpoint='/', status_code=200).inc()
    return jsonify({"message": "Welcome to the personal assistant api!"}), 200

@app_bp.route('/ipinfo', methods=['GET'])
def ipInfo():
    try:
        ipinfo_obj = Ipinfo(request.remote_addr)
        ipinfo = ipinfo_obj.getInfo()
        REQUEST_COUNT.labels(method='GET', endpoint='/ipinfo', status_code=200).inc()
        return jsonify({"ip": ipinfo['ip'], "city": ipinfo['city'], "country": ipinfo['country']}), 200
    except Exception as error:
        REQUEST_COUNT.labels(method='GET', endpoint='/ipinfo', status_code=500).inc()
        return str(error), 500

@app_bp.route('/ipinfo/<ip>', methods=['GET'])
def externalipInfo(ip):
    try: 
        externalipinfo_obj = Ipinfo(ip)
        ipinfo = externalipinfo_obj.getInfo()
        REQUEST_COUNT.labels(method='GET', endpoint='/ipinfo/<ip>', status_code=200).inc()
        return jsonify({"ip": ipinfo['ip'], "city": ipinfo['city'], "country": ipinfo['country']}), 200
    except Exception as error:
        REQUEST_COUNT.labels(method='GET', endpoint='/ipinfo/<ip>', status_code=500).inc()
        return str(error), 500

@app_bp.route('/portchecker', methods=['GET'])
def local_portChecker():
    ip = request.args.get('ip')
    port = request.args.get('port')
    if ip is None or port is None:
        REQUEST_COUNT.labels(method='GET', endpoint='/portchecker', status_code=400).inc()
        return jsonify({"error": "Please provide both 'ip' and 'port' parameters in the endpoint."}), 400
    try:
        port = int(port)
    except ValueError:
        REQUEST_COUNT.labels(method='GET', endpoint='/portchecker', status_code=400).inc()
        return jsonify({"error": "Port must be an integer."}), 400
    checker = Checkport(ip=ip, port=port)
    try:
        result = checker.portChecker()
        REQUEST_COUNT.labels(method='GET', endpoint='/portchecker', status_code=200).inc()
        return jsonify(result), 200
    except Exception as error:
        REQUEST_COUNT.labels(method='GET', endpoint='/portchecker', status_code=500).inc()
        return jsonify({"error": str(error)}), 500

@app_bp.route('/dnschecker', methods=['GET'])
def dnsChecker():
    dnsname = request.args.get('dnsname')
    try:
        checker = DNSChecker(dnsname)
        REQUEST_COUNT.labels(method='GET', endpoint='/dnschecker', status_code=200).inc()
        return jsonify({"message": checker.dnslookUp()}), 200
    except Exception as error:
        REQUEST_COUNT.labels(method='GET', endpoint='/dnschecker', status_code=400).inc()
        return jsonify({"message": str(error)}), 400

# Add /metrics endpoint to the Flask app
@app_bp.route('/metrics', methods=['GET'])
def metrics():
    """
    Expose Prometheus metrics at /metrics endpoint.
    """
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app = Flask(__name__)

    # Register your blueprint
    app.register_blueprint(app_bp)

    # Get host and port from environment variables
    host = os.environ.get('HOST', '0.0.0.0')  # Default to 0.0.0.0 if HOST is not set
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set

    # Run the app
    app.run(debug=True, host=host, port=port)
