from mininet.net import Mininet
from mininet.node import Controller, RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

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

    CONTROLLER_1_IP='127.0.0.1'

    CONTROLLER_0_PORT=6633

    CONTROLLER_1_PORT=5656

    net = Mininet( topo=None, build=False)

    # Create Hosts
    hosts = []
    for i in range(1,9):
        hosts.append(add_host(net, i))
    

    # Create switches
    switches = []
    for i in range(1,8):
        switches.append(add_switch(net,i))

    print "*** Creating links"
    # Hosts to switches    
    net.addLink(hosts[1 -1], switches[4 -1] )
    net.addLink(hosts[2 -1], switches[4 -1] )   
    net.addLink(hosts[3 -1], switches[5 -1] )
    net.addLink(hosts[4 -1], switches[5 -1] )
    net.addLink(hosts[5 -1], switches[6 -1] )
    net.addLink(hosts[6 -1], switches[6 -1] )
    net.addLink(hosts[7 -1], switches[7 -1] )
    net.addLink(hosts[8 -1], switches[7 -1] )  

    # Switches to switches
    net.addLink(switches[1 -1], switches[2 -1] )
    net.addLink(switches[1 -1], switches[3 -1] )
    net.addLink(switches[2 -1], switches[4 -1] )
    net.addLink(switches[2 -1], switches[5 -1] )
    net.addLink(switches[3 -1], switches[6 -1] )
    net.addLink(switches[3 -1], switches[7 -1] )

    # Add Controllers
    controller_0 = net.addController( 'c0', controller=RemoteController, ip=CONTROLLER_0_IP, port=CONTROLLER_0_PORT)

    controller_1 = net.addController( 'c1', controller=RemoteController, ip=CONTROLLER_1_IP, port=CONTROLLER_1_PORT)


    net.build()

    # Connect each switch to a different controller
    for i in 1,2,4,5:
        switches[i -1].start( [controller_0] )

    for i in 3,6,7:
        switches[i -1].start( [controller_1] )

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNet()