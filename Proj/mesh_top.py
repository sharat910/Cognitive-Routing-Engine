from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from functools import partial
from mininet.link import TCLink
import os
from mininet.cli import CLI
from itertools import combinations
import time,random

CONTROLLER_0_IP = '127.0.0.1'

CONTROLLER_0_PORT = 6633

class Mesh(Topo):

    '''
    Mesh topology of k switches, with two hosts per switch.
    '''

    def __init__(self, k = 2, **opts):

        super(Mesh, self).__init__(**opts)

        self.k = k
        switches = []
        for i in irange(1, k):
            h1str = str(2*i)
            host1 = self.addHost('h%s' % h1str,ip='10.0.0.%s' % h1str)
            h2str = str(2*i-1)
            host2 = self.addHost('h%s' % h2str,ip='10.0.0.%s' % h2str)
            switch = self.addSwitch('s%s' % i)
            self.addLink(host1,switch,bw=100)
            self.addLink(host2,switch,bw=100)
            switches.append(switch)

        #Switch Links
        for link in list(combinations(switches,2)):
            self.addLink(link[0],link[1],bw=50,delay='2ms')


def host_discover(net):
    h1 = net.hosts[0]
    h2 = net.hosts[1]
    h1.cmd('ping -c1 %s' % h2.IP())
    for host in net.hosts[1:]:
        host.cmd('ping -c1 %s' % h1.IP())
    h1.cmd('ping -c1 %s' % h2.IP())

def random_traffic(net):
    hosts = net.hosts
    for host in hosts:
        print "starting server in host %s" % host
        host.cmd('iperf -s &')
    random.seed(143)
    for i in xrange(100):
        h1 = random.choice(hosts)
        h2 = random.choice(hosts)
        if h1 == h2:
            continue
        t = random.randint(8,15)
        print i,"Random traffic between %s and %s for %d sec" % (h1,h2,t)
        h1.cmd('iperf -c %s -t %d &' % (h2.IP(),t))
        t2 = random.randint(0,6)
        time.sleep(t2)

def simpleTest():
    ''
    'Create and test a simple network'
    ''

    k = 4
    topo = Mesh(k)
    c0 = RemoteController('c0', ip = CONTROLLER_0_IP,port = CONTROLLER_0_PORT)
    net = Mininet(topo = topo,
        switch = OVSKernelSwitch, controller = c0,
        link = TCLink)
    net.start()
    for i in irange(1, k):
        os.system('sudo ovs-vsctl set bridge s%s protocols=OpenFlow13' % i)
    print 'Dumping host connections'
    dumpNodeConnections(net.hosts)
    time.sleep(3)
    host_discover(net)
    print 'Testing network connectivity'

    #    net.pingAll()
    #random_traffic(net)
    CLI(net)
    net.stop()

if __name__ == '__main__':

    #Tell mininet to print useful information

    setLogLevel('info')
    simpleTest()