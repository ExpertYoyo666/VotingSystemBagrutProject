from DAL import DAL
from Server import Server
from logger import logger


def main():
    dal = DAL()
    server = Server(dal)
    server.main_loop()


if __name__ == "__main__":
    logger.info("Voting server started")
    main()
    logger.info("Voting server stopped")
