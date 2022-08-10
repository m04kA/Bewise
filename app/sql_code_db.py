import sqlalchemy
from loguru import logger
from table_bd import Questions, get_session_db
from request_to_api import handle_request
import datetime

session = get_session_db()


def preparing_data(data: list = None) -> dict or list:
    """
    Preparing data for creating a question or questions.
    :param data: - list of dicts with data for creating a question or questions.
    :return: - ready to use data for creating a question or questions.
    """
    logger.debug(f"Preparing data for DB;\nData = {data}")
    if len(data) > 1:
        for ind in range(len(data)):
            logger.debug(f"Preparing data (ind = {ind}).")
            data[ind] = check_keys(data[ind])
            if data[ind] is {"Error": "Connection error"}:
                logger.error(f"External api is disabled")
                return data[ind]
            if session.query(Questions).get(data[ind]["id"]) is not None:
                logger.info(f"Question with id {data[ind]['id']} already exists.")
                data[ind] = preparing_data([data[ind]])

    else:
        logger.debug(f"Preparing data.\nData = {data}")
        data = check_keys(data[0])
        if data is {"Error": "Connection error"}:
            logger.error(f"External api is disabled")
            return data
        if session.query(Questions).get(data["id"]) is not None:
            logger.info(f"Question with id {data['id']} already exists.")
            test_data = handle_request(method='GET', url='https://jservice.io/api/random', count=1)
            return preparing_data(test_data)
    logger.debug(f"Data is ready.\nData = {data}.")
    return data


def check_keys(data: dict) -> dict:
    """
    Check keys in data.
    :param data: - dict with data from server.
    :return: - dict with data ready to use.
    """
    logger.debug(f"Creating a selection of keys.\nData = {data}")
    my_data = {
        "id": "",
        "question": "",
        "answer": "",
        "created_at": ""
    }
    for key in my_data.keys():
        try:
            my_data[key] = data[key]
        except KeyError:
            logger.error(f"Key ({key}) not found in data.\nData = {data}")
            return {"Error": "Connection error"}
    return my_data


def create_question(data: list = None) -> tuple[dict, int]:
    """
    Create a question or questions to database.
    :param data: - response from server with data.
    :return: - answer from our server and code.
    """
    logger.debug(f"Creating a question.\nData = {data}")
    data = preparing_data(data)
    if data is {"Error": "Connection error"}:
        return data, 523
    if type(data) is list:
        question = [Questions(**item) for item in data]
        logger.info(f"Creating {len(question)} questions.\nData = {question}")
        session.add_all(question)
    else:
        question = Questions(**data)
        logger.info(f"Creating question.\nData = {question}")
        session.add(question)
    try:
        logger.info(f"Committing changes to DB.")
        session.commit()
    except sqlalchemy.exc.DataError:
        logger.error(f"Data error.\nData = {data}")
        return {"Error": "Connect error"}, 523
    except Exception as e:
        logger.error(f"Unknown error.\nError = {e}")
        return {"Error": "Connect error"}, 500
    logger.info(f"Question created, everything successful.")
    return {"Success": "Question created"}, 201


def delete_question(id: int = None) -> tuple[dict, int]:
    """
    Delete question from database.
    :param id: - id of question.
    :return: - answer from our server and code.
    """
    logger.info(f"Start deleting question with id {id}.")
    if id is None:
        logger.error(f"Bad request.\nData = {id}")
        return {"Error": "Bad request"}, 400
    if session.query(Questions).get(id) is None:
        logger.error(f"Question with id {id} not found.")
        return {"Error": "Question not found"}, 404
    session.query(Questions).filter(Questions.id == id).delete()
    session.commit()
    logger.info(f"Question with id {id} deleted.")
    return {"Success": "Question deleted"}, 204


def get_all_questions() -> tuple[list[dict], int]:
    """
    Get all questions from database.
    :return: - list questions(JSON) and code.
    """
    logger.info(f"Start getting all questions.")
    answer = session.query(Questions).all()
    return [serializer(item) for item in answer], 200


def get_one_question(id: int = None) -> tuple[dict, int]:
    """
    Get one question from database.
    :param id: - id of question.
    :return: - question(JSON) and code.
    """
    logger.info(f"Start getting question with id {id}.")
    if id is None:
        logger.error(f"Bad request.\nID is None.")
        return {"Error": "Bad request"}, 400
    answer = session.query(Questions).get(id)
    if answer is None:
        logger.error(f"Question with id {id} not found.")
        return {"Error": "Question not found"}, 404
    return serializer(answer), 200


def serializer(question: Questions) -> dict:
    """
    Serialize question from database.
    :param question: - question from database.
    :return: - question(JSON)
    """
    logger.info(f"Serializing question.\nData = {question}")
    return {
        "id": question.id,
        "question": question.question,
        "answer": question.answer,
        "created_at": question.created_at
    }


def create_test_data() -> int:
    """
    Func for creating test data for show all functional.
    :return: - id test data in DB.
    """
    data = {
        "id": 0,
        "question": "Test question",
        "answer": "Test answer",
        "created_at": datetime.datetime.now()
    }
    if session.query(Questions).get(0) is None:
        question = Questions(**data)
        session.add(question)
        session.commit()
    return data["id"]
