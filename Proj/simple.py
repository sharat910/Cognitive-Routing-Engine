from mininet.net import Mininet
from mininet.node import Controller, RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink


def myNet():
    
    CONTROLLER_0_IP='127.0.0.1'

    CONTROLLER_0_PORT=6633

    net = Mininet( topo=None, build=False,link=TCLink)

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    s1 = net.addSwitch('s1')

    net.addLink(h1,s1,bw=1000,delay='10ms')
    net.addLink(h2,s1,bw=1000,delay='10ms')

    controller_0 = net.addController( 'c0', controller=RemoteController, ip=CONTROLLER_0_IP, port=CONTROLLER_0_PORT)

    s1.start([controller_0])

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNet()