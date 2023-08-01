# Live_Chat_System
Final Project for Computation 2 - University of Mendoza - Campus San Rafael, Mendoza, Argentina

**Table of Contents**

- [🧰 Install](#-install)
- [🚀 Usage](#-usage)
  * [👨‍🔧 Client actions](#-client-actions)
- [🚨 Protocol](#-protocol)


# 🧰 Install

To install and run this program you will need to have:
- python3
- pip3
- flask
- flask-socketio
- sqlalchemy

The next step is the cloning of the repository:

```bash
git clone https://github.com/Lucas16AR/Live_Chat_System.git
```
Once the repository has been created, the virtual environment must be created within it:

```bash
virtualenv realtimepythonchat_env
```
Once the virtual environment has been created, it must be activated as follows:

```bash
source realtimepythonchat_env/bin/activate
```
Once inside the environment, the last step is the installation of the requirements:

```bash
pip3 install -r requirements.txt
```

# 🚀 Usage
Fist you need to go to the file directory

```bash
cd files
```

To start the server you just need to run the file server.py.

```bash
python3 server.py
```

To start the client you just need to run the file client.py.

```bash
python3 client.py
```

To start the chat you just need to run the file server.py.

```bash
python3 messages.py
```

## 👨‍🔧 Client actions
Once the connection to the server is established, the client will be able to perform different actions, these are:

- Enter to a room
- Chat with other people
- Exit


# 🚨 Protocol
The socket used to perform the interconnection is AF_INET is used to designate the type of addresses with which its socket can communicate (in this case, Internet Protocol v4 addresses) and SOCK_STREAM type of the socket, dependent on the previous parameter (not all domains support the same types). In this case, a socket of type STREAM: using the TCP protocol, provides certain security guarantees: packets arrive in order, discarding repeated and/or corrupted packets.
