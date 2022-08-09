import json as JSON
import urllib
from loguru import logger

from requests import Session


def handle_request(
        method: str,
        url: str,
        json: dict = None,
        data: str = None,
        **kwargs) -> dict:
    """Request to server
    Args:
        method (str): Method of request
        url (str): Url of server
        json (dict, optional): Data for complete method POST. Defaults to None.
        data (str, optional): Data for complete method POST. Defaults to None.
    Kwargs:
        Using for adding Params to link
    Raises:
        ConnectionError - If the connection failed.
    Returns:
        dict: Response server
    """
    session = Session()
    # При различном теле запроса необходим различный тип.
    if json:
        session.headers['content-type'] = "application/json"
        logger.debug(f"Set content-type:\napplication/json")
    else:
        session.headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        logger.debug(f"Set content-type:\napplication/x-www-form-urlencoded; charset=UTF-8")

    params = urllib.parse.urlencode(kwargs)  # Формирование строки с параметрами
    if params:
        url += f"?{params}"  # Ссылка для запроса с прараметрами

    # Формирование самого запроса.
    response = session.request(
        method=method,
        url=url,
        json=json,
        data=data,
        timeout=10
    )
    logger.debug(f"Do request to server:\n"
                 f"method - {method}\n"
                 f"url - {url}\n"
                 f"json - {json}\n"
                 f"data - {data}")
    # Проверка на валидность ответа.
    if response.status_code == 200:
        response_dict = JSON.loads(response.text)
        logger.info(f'Successful - {url}')
        return response_dict
    else:
        logger.error(ConnectionError)
        raise ConnectionError
