# BruteForSSHer
A stealthy tool for automatically scanning networks, finding SSH servers and cracking their passwords.
You will need to throw into its directory a users dictionary and a password dictionary.
These files should be named: users.txt and passwords.txt
It requires the user to provide a network interface as a command-line argument.

From there it will take it away and fly autonomously:

a) Scan the local network around you to find open SSH ports

b) Attempt to establish SSH connection to each discovered server

c) Brute-force its way into the SSH server using the provided dictionaries

d) Report all successful logins

# Usage

Get a user-name dictionary and name it "users.txt", and a password dictionary and name it "passwords.txt"
Place the two files in the same directory with this code. Then run the following command:

> brutessh.py <network-interface>

Whereas <network-interface> is the one you want to use for the net scan. For instance:

> brutessh.py eth0

If you do not include an interface name, a menu will offer you to choose from available interfaces.

So you can basically run this tool on your laptop in the background, and by the time you leave the premises, 
you might walk away with more than just free coffee...

As always, please use it for legal purposes only of course ;-)

BruteForSSHer uses the wonderful Paramiko library, so go grab it first at: http://www.paramiko.org
