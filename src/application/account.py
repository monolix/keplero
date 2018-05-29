from flask_restplus import Namespace, Resource, fields
from .utils.database import getSessionID, sendMoney

api = Namespace("account", description="Account related operations.")

sendBundle = api.model("Sending Infos", {
    "token": fields.String("LL1L1LL1L111LLL1LLL111LLL111LLL1", required=True, description="The Sender's session token."),
    "to": fields.String("987654321", required=True, description="The Recipient's ID."),
    "quantity": fields.Integer(5, required=True, description="The amount of money.")
})

recvBundle = api.model("Receive Infos", {
    "token": fields.String("LL1L1LL1L111LLL1LLL111LLL111LLL1", required=True, description="The Sender's session token."),
    "time": fields.Integer(2700, description="The Receive-Token expiring time."),
    "allow": fields.List(fields.String, description="The list of allowed users."),
    "max-amount": fields.Integer(100, description="The max amount of money allowed.")
})

@api.route("/transact")
class Transaction(Resource):
    @api.expect(sendBundle)
    def post(self):
        if set(['token', 'to', 'quantity']) == set(api.payload.keys()):
            session = api.payload["token"]
            from_id = getSessionID(session)
            to_id = api.payload["to"]
            quantity = api.payload["quantity"]
            result = sendMoney(from_id, to_id, quantity)
            if result[0] == 1:
                return {
                    "ok": True,
                    "response": {
                        "from": result[1][2],
                        "to": result[1][3],
                        "quantity": result[1][4],
                        "sign": result[1][0],
                        "when": result[1][1]
                    }
                }
            elif result[0] == 2:
                return {
                    "ok": False,
                    "error": "<balance:not-enough-money>"
                }
            elif result[0] == 3:
                return {
                    "ok": False,
                    "error": "<syntax:invalid-json>"
                }
        else:
            return {
                'ok': False,
                'error': '<syntax:invalid-json>'
            }

    @api.expect(recvBundle)
    def get(self):
        if set(["token"]) <= set(api.payload):
            token = api.payload["token"]
            if "time" in api.payload:
                time = api.payload["time"]
            else:
                time = 600

            if "allow" in api.payload:
                allow = api.payload["allow"]
            else:
                allow = None

            if "max-amount" in api.payload:
                max = api.payload["max-amount"]
            else:
                max = None

            return "Ok"
        else:
            return "ok"

@api.route("/send")
class SendMoney(Resource):
    @api.expect(sendBundle)
    def post(self):
        if set(['token', 'to', 'quantity']) == set(api.payload.keys()):
            session = api.payload["token"]
            from_id = getSessionID(session)
            to_id = api.payload["to"]
            quantity = api.payload["quantity"]
            result = sendMoney(from_id, to_id, quantity)
            if result[0] == 1:
                return {
                    "ok": True,
                    "response": {
                        "from": result[1][2],
                        "to": result[1][3],
                        "quantity": result[1][4],
                        "sign": result[1][0],
                        "when": result[1][1]
                    }
                }
            elif result[0] == 2:
                return {
                    "ok": False,
                    "error": "<balance:not-enough-money>"
                }
            elif result[0] == 3:
                return {
                    "ok": False,
                    "error": "<syntax:invalid-json>"
                }
        else:
            return {
                'ok': False,
                'error': '<syntax:invalid-json>'
            }
