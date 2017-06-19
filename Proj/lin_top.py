from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Controller, RemoteController,OVSKernelSwitch
from functools import partial
from mininet.link import TCLink
import os
from mininet.cli import CLI

CONTROLLER_0_IP='127.0.0.1'

CONTROLLER_0_PORT=6633

class LinearTopo(Topo):
   "Linear topology of k switches, with one host per switch."

   def __init__(self, k=2, **opts):
       """Init.
           k: number of switches (and hosts)
           hconf: host configuration options
           lconf: link configuration options"""

       super(LinearTopo, self).__init__(**opts)

       self.k = k

       lastSwitch = None
       for i in irange(1, k):
           host = self.addHost('h%s' % i)
           switch = self.addSwitch('s%s' % i)
           self.addLink( host, switch)
           if lastSwitch:
               self.addLink( switch, lastSwitch)
           lastSwitch = switch

def simpleTest():
   "Create and test a simple network"
   k=2
   topo = LinearTopo(k)
   link = partial( TCLink, delay='20ms', bw=1000 )
   c0 = RemoteController( 'c0', ip=CONTROLLER_0_IP, port=CONTROLLER_0_PORT)
   net = Mininet( topo=topo,switch=OVSKernelSwitch,controller=c0,link=link)   
   net.start()
   for i in irange(1, k):
           os.system("sudo ovs-vsctl set bridge s%s protocols=OpenFlow13"%i)
   print "Dumping host connections"
   dumpNodeConnections(net.hosts)
   print "Testing network connectivity"
   #net.pingAll()
   CLI( net )
   net.stop()

if __name__ == '__main__':
   # Tell mininet to print useful information
   setLogLevel('info')
   simpleTest()