#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Custom ring Topology
"""

from mininet.topo import Topo
from mininet.cli  import CLI
from mininet.node import OVSSwitch
from mininet.log import setLogLevel
from mininet.net import Mininet

class MyRingTopo(Topo):
    def build(self, max_sw=20, **_opts):
	Switchs = []
	Hosts   = []

	max_h = max_sw * 2


	sw_head = 1
	h_head  = 1001

	for i in range(sw_head, sw_head + max_sw):
	    Switchs.append('sw%d'  %i)
	    self.addNode('sw%d'  %i)

	for i in range(h_head, h_head + max_h):
	    Hosts.append('h%d'  %i)
	    self.addNode('h%d'  %i)

        #"""偶数と奇数をここで分ける"""
	Hostknum = Hosts[0::2] #偶数
	Hostgnum = Hosts[1::2] #奇数

	for (i,j,sw) in zip(Hostknum, Hostgnum, Switchs):
	    if i != None: self.addLink(sw,i)
	    if j != None: self.addLink(sw,j)

	for i in range(0, max_sw-1):
	    self.addLink(Switchs[i], Switchs[i+1])
        self.addLink(Switchs[max_sw-1], Switchs[0])

# topos = { 'myringtopo': ( lambda: MyRingTopo() ) }

if __name__ == '__main__':
    setLogLevel( 'info' )
    topo    = MyRingTopo( max_sw=22 )
    network = Mininet(topo, switch=OVSSwitch )
    network.run( CLI, network )


