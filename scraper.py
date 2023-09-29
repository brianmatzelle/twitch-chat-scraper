import socket, logging, re, os
from datetime import datetime
from dotenv import load_dotenv
from emoji import demojize
load_dotenv()

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'edgar_money'
token = os.getenv('TOKEN')
channel = '#shroud'

sock = socket.socket()
sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

resp = sock.recv(2048).decode('utf-8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler(f'logs/chat_{datetime.now().strftime("%m-%d-%Y,%H-%M-%S")}.log', encoding='utf-8')])

logging.info(resp)

while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    
    if len(resp) > 0:
        logging.info(demojize(resp))
