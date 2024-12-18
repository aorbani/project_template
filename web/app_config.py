import os
from urllib import request, parse
import json
from dotenv import load_dotenv
import logging

from src.Containers.AIModelContainer import AIModelContainer
from src.Containers.BasicContainer import BasicContainer
from src.Containers.ControllerContainer import ControllerContainer

bc = BasicContainer()
bc.init_resources()
aimc = AIModelContainer()
aimc.init_resources()
cc = ControllerContainer()
cc.init_resources()
def init():
    try:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        load_dotenv(verbose=True)
        with open('logs/api_service.log', 'w') as f:
            pass

        logging.basicConfig(
            filename='logs/api_service.log',
            filemode='a',
            format="[%(asctime)s %(levelname)-8s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s",
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')

        auth_url = os.getenv('auth_host')
        auth_body = {
            "grant_type": "client_credentials",
            "scope": "ops.access",
            "client_id": "aurora.ai.api",
            "client_secret":os.getenv('auth_client_secret')
        }
        data = parse.urlencode(auth_body).encode()
        req = request.Request(auth_url, data = data,
                              method='POST')
        with request.urlopen(req) as response:
            res = response.read()
            auth_res = json.loads(res)

        req = request.Request(os.getenv('ops_host'), headers={
            "Authorization": f"Bearer {auth_res['access_token']}"
        })
        with request.urlopen(req) as response:
            app_config = json.load(response)

        for app_config_rec in app_config:
            os.environ[app_config_rec] = str(app_config[app_config_rec])

    except Exception as e:
        logging.error(msg=str(e))
        raise Exception


