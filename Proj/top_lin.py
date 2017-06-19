from mininet.net import Mininet
from mininet.node import Controller, RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import os

def add_host( net, N ):
    "Create host hN and add to net."
    name = 'h%d' % N
    ip = '10.0.0.%d' % N
    mac = '11:11:00:00:00:0%d' % N
    return net.addHost( name, ip=ip, mac = mac )

def add_switch( net, N ):
    "Create switch sN and add to net."
    name = 's%d' % N
    mac = '00:00:00:00:00:0%d' % N
    return net.addSwitch( name, mac = mac )


def myNet():
    
    CONTROLLER_0_IP='127.0.0.1'

    CONTROLLER_0_PORT=6633

    net = Mininet( topo=None, build=False)

    # Create Hosts
    h1= add_host(net, 1)
    h2 = add_host(net, 2)
    

    # Create switches
    s1 = add_switch(net,1)
    s2 = add_switch(net,2)

    #Creating Links
    net.addLink(h1,s1)
    net.addLink(h2,s2)
    net.addLink(s1,s2,bw=10, delay='5ms', loss=2,
                          max_queue_size=1000)

    c0 = net.addController( 'c0', controller=RemoteController, ip=CONTROLLER_0_IP, port=CONTROLLER_0_PORT)

    net.build()
    net.start()
    os.system("sudo ovs-vsctl set bridge s1 protocols=OpenFlow13")
    os.system("sudo ovs-vsctl set bridge s2 protocols=OpenFlow13")
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNet()