# Structure
"""
* => Optional Args

Authorization:
    POST http://api/authorization/register -> Create Account
        JSON: {
            id: String(),
            password: String(),
            email: String(),
            username: String()
        }
    POST http://api/authorization/login -> Create Authorization Token
        JSON: {
            id: String(),
            password: String()
        }

User Profile:
    GET http://api/users/{id} -> Check a User Status
    GET http://api/users/me - Needs Auth -> Check the AU's Status
    PUT http://api/users/me - Needs Auth -> Update the AU's Status
        JSON: {
            * email: String(),
            * username: String(),
            * new-password: String(),
            password: String()
        }

Actions: - Needs Auth
    POST http://api/actions/send -> Send Money to Someone
        JSON: {
            password: String(),
            receive-token: String(),
            quantity: Integer()
        }
    POST http://api/actions/receive -> Create a Token to Receive Money
        JSON: {
            expires: Integer(),
            times: Integer(),
            persistent: Boolean()
        }

About:
    GET http://api/about/info -> Get the API info
    GET http://api/about/license -> Get the API License

"""