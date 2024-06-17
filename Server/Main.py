from DAL import DAL
from Server import Server


def main():
    dal = DAL()
    server = Server(dal)
    server.main_loop()


if __name__ == "__main__":
    main()