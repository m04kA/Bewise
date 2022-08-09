from flask import Flask, make_response
from flask_restful import Api, Resource
from sql_code_db import create_question, delete_question, get_all_questions, get_one_question
from request_to_api import handle_request
from loguru import logger

app = Flask(__name__)
api = Api()


class Main(Resource):
    def get(self, number=None):
        if number is None:
            logger.info("Method = Get;\nQuery = all questions;")
            return make_response(get_all_questions())
        else:
            try:
                logger.info(f"Method = Get;\nQuery = one question;\nID = {number};")
                return make_response(get_one_question(id=number))
            except Exception as e:
                logger.error(f"Method = Get;\nQuery = one question;\nID = {number};\nError = {e};")
                return {"Error": str(e)}, 500

    def delete(self, number=None):
        if number is None:
            logger.info("Method = Delete;\nMessage = bad request (number is None);\nCode = 400;")
            return {"Error": "Bad request"}, 400
        try:
            logger.info(f"Method = Delete;\nMessage = delete question;\nID = {number};")
            response = delete_question(number)
            return response
        except Exception as e:
            logger.error(f"Method = Delete;\nID = {number};\nError = {e};")
            return {"Error": str(e)}, 500

    def post(self, number=None):
        if number is None:
            logger.info("Method = Post;\nMessage = bad request (number is None);\nCode = 400;")
            return {"Error": "Bad request"}, 400
        logger.info(f"Method = Post;\nMessage = create questions;\nCount = {number};")
        response = handle_request(method='GET', url='https://jservice.io/api/random', count=number)
        response = create_question(response)
        return response

    def put(self):
        try:
            logger.info("Method = Put;\nMessage = No accept;\nCode = 403;")
            return {"Error": "Forbidden"}, 403
        except Exception as e:
            logger.error(f"Method = Put;\nError = {e};\nCode = 500;")
            return {"Error": str(e)}, 500


api.add_resource(Main, "/api/questions", "/api/questions/<int:number>")
api.init_app(app)

if __name__ == "__main__":
    logger.info("Start server.\nUrl = http://localhost:6000;\nDebug = True;")
    app.run(debug=True, port=6000, host="127.0.0.1")
