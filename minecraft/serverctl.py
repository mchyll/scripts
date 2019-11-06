#!/usr/bin/python3

from mcrcon import mcrcon
import argparse
import socket
import errno
import subprocess
import time


class RCON:
    def __init__(self, password: str, host='localhost', port=25575):
        self.password = password
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self.sock.connect((self.host, self.port))
        if not mcrcon.login(self.sock, self.password):
            raise Exception('Wrong RCON password')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.__exit__()

    def cmd(self, command: str) -> str:
        return mcrcon.command(self.sock, command)


def seconds_to_str(s: int) -> str:
    """
    Returns a string describing the given number of seconds in a human-readable form.
    """

    s = abs(s)
    result = []

    days = s // 86400
    if days:
        result.append('{} day{}'.format(days, '' if days == 1 else 's'))

    hours = s // 3600 % 24
    if hours:
        result.append('{} hour{}'.format(hours, '' if hours == 1 else 's'))

    minutes = s // 60 % 60
    if minutes:
        result.append('{} minute{}'.format(minutes, '' if minutes == 1 else 's'))

    secs = s % 60
    if secs or len(result) == 0:
        result.append('{} second{}'.format(secs, '' if secs == 1 else 's'))

    if len(result) == 1:
        return result[0]
    else:
        return ', '.join(result[:-1]) + ' and ' + result[-1]


def start_server(kill_session=False):
    """
    Starts the minecraft server in a tmux session.
    """
    if kill_session:
        subprocess.run(['tmux', 'kill-session', '-t', 'mc'])

    subprocess.run(['tmux', 'new-session', '-d', '-s', 'mc', 'bash --init-file ServerStart.sh'], cwd='/home/magnus/ftb_server')


def main(args):
    rcon = RCON(args.password, args.host, args.port)

    if args.start:
        start_server()

    elif args.notify_restart:
        with rcon:
            rcon.cmd('say Server will restart in {}'.format(seconds_to_str(args.notify_restart)))

    elif args.restart:
        try:
            with rcon:
                rcon.cmd('say Server will restart now')
                rcon.cmd('save-all')
                rcon.cmd('stop')

        except (socket.error, Exception) as err:
            print('Error connecting to server for stopping it: ', err)

        # Wait some seconds for the server to shut down before restarting it
        time.sleep(5)
        start_server(kill_session=True)

    elif args.cmd:
        with rcon:
            print(rcon.cmd(args.cmd))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument('--notify-restart', '-n', type=int, metavar='SECONDS', help='send notification that server will restart in SECONDS')
    actions.add_argument('--restart', '-r', action='store_true', help='restart server')
    actions.add_argument('--start', '-s', action='store_true', help='start server')
    actions.add_argument('--cmd', '-c', metavar='COMMAND', help='send RCON command')
    parser.add_argument('--password', '-p', required=True, help='the server RCON password')
    parser.add_argument('--host', '-H', default='localhost', help='the RCON port. Default: localhost')
    parser.add_argument('--port', '-P', default=25575, help='the RCON host. Default: 25575')
    args = parser.parse_args()
    main(args)
