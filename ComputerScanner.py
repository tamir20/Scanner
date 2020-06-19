import subprocess  # For executing a shell command
import os
import socket
import sys
import string

try:
    from subprocess import DEVNULL  # Python 3.
except ImportError:
    DEVNULL = open(os.devnull, 'wb')


def test_ping(host):
    # Returns True if host (str) responds to a ping request.

    # Building the command. Ex: "ping -n 1 google.com"
    command = ['ping', '-n', '1', host]

    try:
        # run the command with timeout
        command_ended_successfully = subprocess.call(command, stdout=DEVNULL, stderr=subprocess.STDOUT,
                                                     timeout=0.5) == 0
    except subprocess.TimeoutExpired:
        # if timeout then the host didn't respond on time
        command_ended_successfully = False
    if command_ended_successfully:
        # maybe the command ended successfully and on time, but the host was unreachable
        output = subprocess.Popen(["ping", '-n', '1', host], stdout=subprocess.PIPE).communicate()[0]
        if 'unreachable' not in str(output):
            # if it is unreachable then return false
            return True
    return False


def represents_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def test_port(ip, port):
    # socket with timeout
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        # try to connect and end the connection gracefully and return true that the connection was
        # formed on the desired port
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except socket.timeout:
        # if timeout then connection wasn't formed, return false
        return False
    except socket.gaierror:
        # another error when trying to form a connection but the dns name is resolvable
        return False
    finally:
        s.close()


# Count the arguments
arguments = len(sys.argv) - 1
file_path = 'computers.txt'

# create the output files
with open('online.txt', 'w') as online_file, open('offline.txt', 'w') as offline_file:
    if arguments == 0:
        # if no arguments then check for ping
        with open(file_path) as fp:
            for line in fp:
                host = str.strip(line)
                if test_ping(host) == 1:
                    online_file.write(host + "\n")
                else:
                    offline_file.write(host + "\n")

    else:
        if not represents_int(sys.argv[1]):
            print("argument must be an integer")
        else:
            # if there are arguments then check for port
            with open(file_path) as fp:
                for line in fp:
                    host = str.strip(line)
                    if test_port(host, sys.argv[1]) == 1:
                        online_file.write(host + "\n")
                    else:
                        offline_file.write(host + "\n")
