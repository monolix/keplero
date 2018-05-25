from flask_restplus import Namespace, Resource, fields
from .utils.database import getSessionID, sendMoney

api = Namespace("account", description="Account related operations.")

sendBundle = api.model("Transaction Infos", {
    "token": fields.String("LL1L1LL1L111LLL1LLL111LLL111LLL1", required=True, description="The Sender's session token."),
    "to": fields.String("987654321", required=True, description="The Recipient's ID."),
    "quantity": fields.Integer(5, required=True, description="The amount of money.")
})

@api.route("/send")
class SendMoney(Resource):
    @api.expect(sendBundle)
    def post(self):
        session = api.payload["token"]
        from_id = getSessionID(session)
        to_id = api.payload["to"]
        quantity = api.payload["quantity"]
        result = sendMoney(from_id, to_id, quantity)
        if result == 1:
            return {
                "ok": True,
                "response": {
                    "from": from_id,
                    "to": to_id,
                    "quantity": int(quantity)
                }
            }
        elif result == 2:
            return {
                "ok": False,
                "error": "<balance:not_enough_money>"
            }
        elif result == 3:
            return {
                "ok": False,
                "error": "<syntax:invalid_json>"
            }