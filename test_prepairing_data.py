from sql_code_db import check_keys, serializer, Questions

test_data = {
    'id': 70646,
    'answer': 'Lady Macbeth',
    'question': 'Judith Anderson won Emmys in 1955 & 1961 for playing this Shakespearean lady',
    'value': 200,
    'airdate': '2001-03-30T12:00:00.000Z',
    'created_at': '2022-07-27T00:54:42.058Z',
    'updated_at': '2022-07-27T00:54:42.058Z',
    'category_id': 6933,
    'game_id': 1484,
    'invalid_count': None,
    'category': {
        'id': 6933,
        'title': '"m" & emmys',
        'created_at': '2022-07-27T00:54:41.852Z',
        'updated_at': '2022-07-27T00:54:41.852Z', 'clues_count': 15
    }
}

test_question = {
    "id": 10,
    "question": "Test",
    "answer": "Good test",
    "created_at": "2022-07-27T00:54:41.852Z"
}
question = Questions(**test_question)


def test_check_keys():
    true_answer = {
        "id": 70646,
        "question": 'Judith Anderson won Emmys in 1955 & 1961 for playing this Shakespearean lady',
        "answer": 'Lady Macbeth',
        "created_at": '2022-07-27T00:54:42.058Z'
    }
    assert check_keys(test_data) == true_answer
    assert check_keys({}) == {"Error": "Connection error"}
    assert check_keys({'id': 70646}) == {"Error": "Connection error"}


def test_serializer_data():
    assert serializer(question=question) == test_question
