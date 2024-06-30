Welcome to my project!

This project implements an Internet voting system. It includes a Server and two client applications, one for the administration and one for the voters.

## How to run

### Activate the virtual environment:

In Linux:
```bash
python -m venv venv
source venv\Scripts\activate
```
or for Windows:
```bash
venv/Scripts/activate
```

### Install dependencies
```bash
pip install -r requirements.txt`
```

### Run the server and 
```bash
cd Server
python Main.py
```

### Run the clients
```bash
cd Client/AdminClient/
python Main.py
```

```bash
Client/VotingClient/
python Main.py
```

