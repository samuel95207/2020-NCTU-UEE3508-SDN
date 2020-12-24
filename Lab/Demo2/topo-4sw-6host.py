"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )
        h4 = self.addHost( 'h4' )
        h5 = self.addHost( 'h5' )
        h6 = self.addHost( 'h6' )

        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )


        # Add links
        self.addLink( s1,s2,bw=1024,ls=5 )
        self.addLink( s2,s3,bw=1024,ls=5 )
        self.addLink( s3,s4,bw=1024,ls=5 )

        self.addLink( s1,h1,bw=100 )
        self.addLink( s1,h2,bw=100 )
        self.addLink( s2,h3,bw=100 )
        self.addLink( s3,h4,bw=100 )
        self.addLink( s4,h5,bw=100 )
        self.addLink( s4,h6,bw=100 )





topos = { 'mytopo': ( lambda: MyTopo() ) }
