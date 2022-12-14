import logging_conf
from loguru import logger
from flask import Flask, make_response, Response, request, jsonify
from flask_restful import Api, Resource, reqparse
from sql_code_db import create_question, delete_question, get_all_questions, get_one_question, create_test_data
from request_to_api import handle_request

app = Flask(__name__)
api = Api()

parser = reqparse.RequestParser()
parser.add_argument("questions_num", type=int)


class Main(Resource):
    def get(self, number: int = None) -> Response or tuple[dict, int]:
        """
        Get all questions or one question
        For all questions use url: /api/questions
        For one question use url: /api/questions/<id>
        :param number: - ID of question
        :return: - JSON with all questions or one question and code
        """
        if number is None:
            # Get all questions
            logger.info("Method = Get;\nQuery = all questions;")
            return make_response(get_all_questions())
        else:
            try:
                # Get one question
                logger.info(f"Method = Get;\nQuery = one question;\nID = {number};")
                return make_response(get_one_question(id=number))
            except Exception as e:
                logger.error(f"Method = Get;\nQuery = one question;\nID = {number};\nError = {e};")
                return {"Error": str(e)}, 500

    def delete(self, number: int = None) -> tuple[dict, int]:
        """
        Delete one question by id.
        :param number: - ID of question for delete
        :return: - Response server and code
        """
        if number is None:
            logger.info("Method = Delete;\nMessage = bad request (number is None);\nCode = 400;")
            return {"Error": "Bad request"}, 400
        try:
            # Delete one question
            logger.info(f"Method = Delete;\nMessage = delete question;\nID = {number};")
            response = delete_question(number)
            return response
        except Exception as e:
            logger.error(f"Method = Delete;\nID = {number};\nError = {e};")
            return {"Error": str(e)}, 500

    def post(self, number: int = None) -> tuple[dict, int]:
        """
        {"questions_num": integer}
        Create a certain number of questions
        :param number: - Number of questions for create
        :return: - Response server and code
        """
        if number is None:
            try:
                number = request.get_json(force=True)["questions_num"]
            except KeyError:
                logger.info("Method = Post;\nMessage = bad request (number is None);\nCode = 400;")
                return {"Error": "Bad request"}, 400
            except Exception as e:
                logger.error(f"Method = Post;\nError = {e};")
                return {"Error": str(e)}, 500
        logger.info(f"Method = Post;\nMessage = create questions;\nCount = {number};")
        response = handle_request(method='GET', url='https://jservice.io/api/random', count=number)
        response = create_question(response)
        response[0]["count"] = number
        return response

    def put(self) -> tuple[dict, int]:
        """
        Update one question, but now it is not implemented.
        :return:
        """
        try:
            logger.info("Method = Put;\nMessage = No accept;\nCode = 403;")
            return {"Error": "Forbidden"}, 403
        except Exception as e:
            logger.error(f"Method = Put;\nError = {e};\nCode = 500;")
            return {"Error": str(e)}, 500


@app.route('/info')
def main_page():
    create_test_data()
    content = {
        "GET": [
            {
                "Url": "/api/questions",
                "Parameters": "None",
                "Description": "Get all questions",
                "Response": handle_request(method='GET', url='http://127.0.0.1:5000/api/questions')
            },
            {
                "Url": "/api/questions/<int:number>",
                "Parameters": "number - ID of question",
                "Description": "Get one question",
                "Response": handle_request(method='GET', url='http://127.0.0.1:5000/api/questions/0')
            }
        ],
        "POST": [
            {
                "Url": "/api/questions",
                "Data": {"questions_num": 2},
                "Parameters": "None",
                "Description": "Create a certain number of questions",
                "Response": handle_request(method='POST', url='http://127.0.0.1:5000/api/questions',
                                           json={"questions_num": 2})
            },
            {
                "Url": "/api/questions/<int:number>",
                "Parameters": "number - count of new questions",
                "Description": "Create a certain number of questions",
                "Response": handle_request(method='POST', url='http://127.0.0.1:5000/api/questions/1')
            }
        ],
        "PUT": {
            "Url": "/api/questions",
            "Parameters": "None",
            "Description": "Lack of access.",
            "Response": {"Error": "Forbidden"}
        },
        "DELETE": {
            "Url": "/api/questions/<int:number>",
            "Parameters": "number - ID of question",
            "Description": "Delete one question",
            "Response": handle_request(method='DELETE', url='http://127.0.0.1:5000/api/questions/0')
        }
    }
    rez = make_response(jsonify(content), 200)
    return rez


api.add_resource(Main, "/api/questions", "/api/questions/<int:number>")
api.init_app(app)

if __name__ == "__main__":
    logger.info("Start server.\nUrl = http://127.0.0.1:5000;\nDebug = False;")
    app.run(host="0.0.0.0", port=5000, debug=False)
