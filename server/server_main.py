from server_config import *
from server_handlers import *
from server_prepacket import *


battle_update_thread = BattleUpdateLoop()

while True:
    client, addr = s_tcp.accept()
    print('new connection')
    client_handler = threading.Thread(target=handle_client_listener, args=(client, addr,))
    client_handler.start()
