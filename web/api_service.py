import uvicorn
import logging
import argparse
import app_config

def start_api_service(host:str, port: int) -> None:
    try:
        logging.info("API Service starting ...")
        uvicorn.run("APIs.application:app", host=host, port=int(port))
    except Exception as err:
        logging.error(str(err))
    finally:
        logging.info("API Service shutting down ...")


if __name__ == '__main__':
    app_config.init()
    parser = argparse.ArgumentParser(description='APIs app')
    parser.add_argument('--host', action="store", dest='host', default='localhost')
    parser.add_argument('--port', action="store", dest='port', default=8000)
    args = parser.parse_args()
    config = vars(args)
    start_api_service(config['host'],config['port'])