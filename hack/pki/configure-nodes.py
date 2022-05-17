#!/usr/bin/env python3

import argparse
import os 
import sys
from fabric import Connection
from invoke import Responder
from fabric import SerialGroup as Group

SpecialSym =['$', '@', '#', '%']

# on prem k3s nodes.
# TODO find a better way to manage this list.
nodes = [
    "10.1.32.20",
    "10.1.32.21",
    "10.1.32.23",
    "10.1.32.24",
    "10.1.32.25",
    "10.1.32.26",
    "10.1.32.27",
    "10.1.32.28",
    "10.1.32.29"
]

# Env vars
HOME = os.environ.get('HOME', None)

def validate_args(args):
    """Validate input args
    """
    ## TODO improve validation.
    
    ## init password
    if args.username == None or len(args.username) == 0:
        print("ERR: Username missing")
        sys.exit(1) 
        
    ## init password
    if args.init_password == None or len(args.init_password) == 0:
        print("ERR: Init password missing")
        sys.exit(2) 
    
    if args.strong_password == None or \
        (len(args.strong_password) < 8 and \
            not any(char.isdigit() for char in args.strong_password) and \
            not any(char.isupper() for char in args.strong_password) and \
            not any(char.islower() for char in args.strong_password) and \
            not any(char in SpecialSym for char in args.strong_password)):
        print("ERR: Strong password fails validation:")
        print("     At least 1 digit")
        print("     At least 1 small char")
        print("     At least 1 upper char")
        print("     At least 1 special char - ", SpecialSym)
        sys.exit(3) 
    
    if not os.path.exists(args.pub_key_path):
        print("ERR: Pub key is missing - ", args.pub_key_path)
        sys.exit(4)    
        

def configure_nodes(args):
    """Configure for secure access individual k3s nodes
    """
    conn_kwargs = {"password": args.init_password}
    
    # TODO run it in parallel
    for node in nodes:
        print(f"Configuring {node}")
        
        with Connection(node, 
                        user = args.username,
                        connect_kwargs = conn_kwargs) as c:
            
            c.run('hostname')            
            
            append_ssh_pub_key(args, c)
           
            change_password(args, c)

def append_ssh_pub_key(args, conn):
    print(" > Uploading SSH pub key")
    
    if not os.path.exists(args.pub_key_path):
        print(" > ERR: Pub key file is missing -",  args.pub_key_path)
        return
    
    pub_key = None
    with open(args.pub_key_path, 'r') as f:
        pub_key = f.read()
        
    if pub_key is None:
        print(" > ERR: Pub key not set")
        return
    
    ssh_dir = ".ssh"
    auth_file = f"{ssh_dir}/authorized_keys"
    if conn.run(f"test -d {ssh_dir}", warn=True).failed:
        print(f" > Create SSH dir {ssh_dir}")
        conn.run(f"mkdir {ssh_dir}") 
    
    if conn.run(f"test -f {auth_file}", warn=True).failed: 
        print(f" > Create auth keys file {auth_file}")
        conn.run(f"touch {auth_file}; chmod 0600 {auth_file}")
    
    # TODO: Check first if key is already present before adding it.
    #       Currently failing with grep invocation.     
    # if conn.run(f"grep -q '{pub_key}' {auth_file}").failed:  
    #     print(" > Adding missing pub key")  
    conn.run(f"echo \"{pub_key}\" > {auth_file}")
        
    
def change_password(args, conn):
    print(" > Changing password")
    current_password = Responder(
        pattern = r"Current password\: ",
        response = f"{args.init_password}\n",
    )
    
    new_password = Responder(
        pattern = r"New password\: ",
        response = f"{args.strong_password}\n",
    )
    
    retype_new_password = Responder(
        pattern = r"Retype new password\: ",
        response = f"{args.strong_password}\n",
    )
    
    conn.run("passwd", watchers=[current_password, 
                                 new_password, 
                                 retype_new_password])
    
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Config access to nodes')
    parser.add_argument('--username', action="store", dest="username")
    parser.add_argument('--init-password', action="store", dest="init_password")
    parser.add_argument('--strong-password', action="store", dest="strong_password")
    parser.add_argument('--pub-key-path', 
                        action="store", 
                        dest="pub_key_path",
                        default=f"{HOME}/.ssh/id_rsa.pub")
    args = parser.parse_args()
    validate_args(args)
    
    configure_nodes(args)
    
