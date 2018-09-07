from . import app
from flask import jsonify, abort
from werkzeug.exceptions import HTTPException, default_exceptions

class PaymentRequired(HTTPException):
    code = 402
    description = 'Payment Required.'

default_exceptions[402] = PaymentRequired

@app.errorhandler(400)
def badRequest(e):
    return jsonify({
        "ok": False,
        "result": {
            "error-code": 400,
            "description": "Bad Request: Malformed data passed as a Payload."
        }
    }), 400

@app.errorhandler(401)
def authenticationError(e):
    return jsonify({
        "ok": False,
        "result": {
            "error-code": 401,
            "description": "Unauthorized: Wrong Credentials or Unverified Account."
        }
    }), 401

@app.errorhandler(402)
def paymentRequired(e):
    return jsonify({
        "ok": False,
        "result": {
            "error-code": 402,
            "description": "Payment Required: Not enough money for the transaction."
        }
    }), 402

@app.errorhandler(403)
def forbiddenResource(e):
    return jsonify({
        "ok": False,
        "result": {
            "error-code": 403,
            "description": "Forbidden: This Resource requires Authentication."
        }
    }), 403

@app.errorhandler(404)
def notFound(e):
    return jsonify({
        "ok": False,
        "result": {
            "error-code": 404,
            "description": "Not Found: Rescource not found on the Server."
        }
    }), 404

@app.errorhandler(405)
def methodNotAllowed(e):
    return jsonify({
        "ok": False,
        "result": {
            "error-code": 405,
            "description": "Method Not Allowed: This Method is not implemented in this Resource."
        }
    }), 405

@app.errorhandler(409)
def conflictError(e):
    return jsonify({
        "ok": False,
        "result": {
            "error-code": 409,
            "description": "Conflict: Resource already created on the Server (the user already exists or session already created)."
        }
    }), 409
