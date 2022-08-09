from flask import Flask, make_response
from flask_restful import Api, Resource
from sql_code_db import create_question, delete_question, get_all_questions, get_one_question
from request_to_api import handle_request

app = Flask(__name__)
api = Api()


class Main(Resource):
    def get(self, number=None):
        if number is None:
            return make_response(get_all_questions())
        else:
            try:
                return make_response(get_one_question(id=number))
            except Exception as e:
                return {"Error": str(e)}, 500

    def delete(self, number=None):
        if number is None:
            return {"Error": "Bad request"}, 400
        try:
            response = delete_question(number)
            return response
        except Exception as e:
            return {"Error": str(e)}, 500

    def post(self, number=None):
        """
        1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса.
        :param number: 
        :return: 
        """
        if number is None:
            return {"Error": "Bad request"}, 400

        response = handle_request(method='GET', url='https://jservice.io/api/random', count=number)
        response = create_question(response)
        return response

    def put(self):
        try:
            return {"Error": "Forbidden"}, 403
        except Exception as e:
            return {"Error": str(e)}, 500


api.add_resource(Main, "/api/questions", "/api/questions/<int:number>")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=6000, host="127.0.0.1")
