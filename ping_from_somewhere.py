import random
import string
import requests
import time
from stem import Signal
from stem.control import Controller

PING_ADDRES = '' 
MY_IP_ADDRES = 'http://httpbin.org/ip'
PASSWORD = '' 
PING_COUNT = 0 


def create_tor_session():
    session = requests.session()

    # TO Request URL with SOCKS over TOR

    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    return session


def ping_addres(session, addres=PING_ADDRES):
    try:
        r = session.get(addres)
    except Exception as e:
        print(str(e))
    else:
        return r.text


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def renew_tor_ip():
    # with Controller.from_port(port=9051) as controller:   original
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=PASSWORD)
        controller.signal(Signal.NEWNYM)


if __name__ == "__main__":
    i = 0
    addr_list = []
    while i < PING_COUNT:
        session = create_tor_session()
        new_addr = ping_addres(session, MY_IP_ADDRES)
        if not (new_addr in addr_list):
            addr_list.append(new_addr)
            print("{}+++++++++++\n{}\n{}+++++++++++".format(i, new_addr, i))
            ping_addres(session)
            i += 1
        else:
            print('------------')
        renew_tor_ip()
