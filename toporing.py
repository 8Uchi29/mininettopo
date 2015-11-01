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

"""
for Quagga
"""
import inspect
import os
from mininext.topo import Topo
from mininext.services.quagga import QuaggaService
from collections import namedtuple
QuaggaHost = namedtuple("QuaggaHost", "name ip loIP")
net = None

class MyRingTopo(Topo):
    def build(self, max_sw=20, **_opts):
        #self.forRegacy(max_sw)
        self.forQuagga(max_sw)

    def forRegacy(self, max_sw):
	Switchs = []
	Hosts   = []

	max_h = max_sw * 2


	sw_head = 1
	h_head  = 1001

	for i in range(sw_head, sw_head + max_sw):
	    Switchs.append('sw%d'  %i)
	    self.addSwitch('sw%d'  %i)

	for i in range(h_head, h_head + max_h):
	    Hosts.append('h%d'  %i)
	    self.addNode('h%d'  %i)

        #偶数と奇数をここで分ける
	Hostknum = Hosts[0::2] #偶数
	Hostgnum = Hosts[1::2] #奇数

	for (i,j,sw) in zip(Hostknum, Hostgnum, Switchs):
	    if i != None: self.addLink(sw,i)
	    if j != None: self.addLink(sw,j)

	for i in range(0, max_sw-1):
	    self.addLink(Switchs[i], Switchs[i+1])
        self.addLink(Switchs[max_sw-1], Switchs[0])

    def forQuagga(self, max_sw):
        # Directory where this file / script is located"
        selfPath = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))  # script directory

        # Initialize a service helper for Quagga with default options
        quaggaSvc = QuaggaService(autoStop=False)

        # Path configurations for mounts
        quaggaBaseConfigPath = selfPath + '/configs/'

	max_h = max_sw * 2
	sw_head = 1
	h_head  = 1
        quaggaHosts   = []
	quaggaSwitchs = []

	for i in range(sw_head, sw_head + max_sw):
	    quaggaSwitchs.append('sw%d'  %i)
	    self.addSwitch('sw%d'  %i)

	for i in range(h_head, h_head + max_h):
	    hostnum = 1000 + i
            quaggaHosts.append(QuaggaHost(name='h%d' %hostnum, 
	                                  ip='172.0.253.%d/24' %i,
	                                  loIP='192.168.0.%d/24' %i))

        for host in quaggaHosts:
            # Create an instance of a host, called a quaggaContainer
            quaggaContainer = self.addHost(name=host.name,
                                           ip=host.ip,
                                           hostname=host.name,
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True)

            # Add a loopback interface with an IP in router's announced range
            self.addNodeLoopbackIntf(node=host.name, ip=host.loIP)

            # Configure and setup the Quagga service for this node
            quaggaSvcConfig = \
                {'quaggaConfigPath': quaggaBaseConfigPath + host.name}
            self.addNodeService(node=host.name, service=quaggaSvc,
                                nodeConfig=quaggaSvcConfig)

            ## Attach the quaggaContainer to the IXP Fabric Switch
            #self.addLink(quaggaContainer, ixpfabric)

        #偶数と奇数をここで分ける
	Hostknum = quaggaHosts[0::2] #偶数
	Hostgnum = quaggaHosts[1::2] #奇数
	for (k,j,sw) in zip(Hostknum, Hostgnum, quaggaSwitchs):
	    if k != None: self.addLink(sw,k)
	    if j != None: self.addLink(sw,j)

	for i in range(0, max_sw-1):
	    self.addLink(quaggaSwitchs[i], quaggaSwitchs[i+1])
        self.addLink(quaggaSwitchs[max_sw-1], quaggaSwitchs[0])

# topos = { 'myringtopo': ( lambda: MyRingTopo() ) }



