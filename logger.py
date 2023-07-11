import logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
@staticmethod
def Log(text:str):
     logging.info(text)