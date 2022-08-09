from table_bd import Questions, get_session_db
from request_to_api import handle_request

session = get_session_db()


def prepair_data(data):
    if len(data) > 1:
        for ind in range(len(data)):
            data[ind] = check_keys(data[ind])
            if data[ind] is {"Error": "Connection error"}:
                return data[ind]
            if session.query(Questions).get(data[ind]["id"]) is not None:
                data[ind] = prepair_data([data[ind]])

    else:
        data = check_keys(data[0])
        if data is {"Error": "Connection error"}:
            return data
        if session.query(Questions).get(data["id"]) is not None:
            test_data = handle_request(method='GET', url='https://jservice.io/api/random', count=1)
            return prepair_data(test_data)
    return data


def check_keys(data: dict) -> dict:
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
            return {"Error": "Connection error"}
    return my_data


def create_question(data: dict or list = None):
    data = prepair_data(data)
    if data is {"Error": "Connection error"}:
        return data, 523
    if type(data) is list:
        question = [Questions(**item) for item in data]
        session.add_all(question)
    else:
        question = Questions(**data)
        session.add(question)
    session.commit()
    return {"Success": "Question created"}, 201


def delete_question(id=None):
    if id is None:
        return {"Error": "Bad request"}, 400
    if session.query(Questions).get(id) is None:
        return {"Error": "Question not found"}, 404
    session.query(Questions).filter(Questions.id == id).delete()
    session.commit()
    return {"Success": "Question deleted"}, 204


def get_all_questions():
    answer = session.query(Questions).all()
    return [serializer(item) for item in answer], 200


def get_one_question(id=None):
    if id is None:
        return {"Error": "Bad request"}, 400
    answer = session.query(Questions).get(id)
    if answer is None:
        return {"Error": "Question not found"}, 404
    return serializer(answer), 200


def serializer(question):
    return {
        "id": question.id,
        "question": question.question,
        "answer": question.answer,
        "created_at": question.created_at
    }


# print(get_one_question(id=85598))

# test_data = handle_request(method='GET', url='https://jservice.io/api/random', count=1)

# print(create_question(test_data))

# print(session.query(Questions).all())

# print(delete_question(1))

# print(session.query(Questions).all())

# session.close()
