from DAL import DAL
from Server import Server

if __name__ == '__main__':
    dal = DAL()
    server = Server(dal)
    server.main_loop()
