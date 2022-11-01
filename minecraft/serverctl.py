#!/usr/bin/python3

from mcrcon import mcrcon
import argparse
import socket
import subprocess
import time


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


class RCON:
    def __init__(self, host: str, port: int, password: str):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        if not mcrcon.login(self.sock, password):
            raise Exception('Wrong RCON password')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.__exit__()

    def cmd(self, command: str) -> str:
        return mcrcon.command(self.sock, command)


class ServerCtl:
    def __init__(self, rcon_host: str=None, rcon_port: int=None, rcon_password: str=None):
        self.rcon_host = rcon_host
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password

    def _create_rcon_connection(self) -> RCON:
        return RCON(self.rcon_host, self.rcon_port, self.rcon_password)

    def start_server(self, kill_session=False):
        """
        Starts the minecraft server in a tmux session.
        """

        if kill_session:
            subprocess.run(['tmux', 'kill-session', '-t', 'mc'])

        subprocess.run(['tmux', 'new-session', '-d', '-s', 'mc', 'bash --init-file ServerStart.sh'], cwd='/home/magnus/ftb_server')

    def notify_restart(self, seconds: int):
        """
        Sends notification to users on the server that it will restart in `seconds`.
        """

        with self._create_rcon_connection() as rcon:
            rcon.cmd('say Server will restart in {}'.format(seconds_to_str(args.notify_restart)))

    def restart(self):
        """
        Restarts the server.
        """

        try:
            with self._create_rcon_connection() as rcon:
                rcon.cmd('say Server will restart now')
                rcon.cmd('save-all')
                rcon.cmd('stop')

        except (socket.error, Exception) as err:
            print('Error connecting to server for stopping it: ', err)

        # Wait some seconds for the server to shut down before restarting it
        time.sleep(5)
        self.start_server(kill_session=True)

    def exec_cmd(self, cmd: str) -> str:
        """
        Executes a command on the server via RCON and returns the response string.
        """

        with self._create_rcon_connection() as rcon:
            return rcon.cmd(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument('--notify-restart', '-n', type=int, metavar='SECONDS', help='send notification that server will restart in SECONDS')
    actions.add_argument('--restart', '-r', action='store_true', help='restart server')
    actions.add_argument('--start', '-s', action='store_true', help='start server')
    actions.add_argument('--cmd', '-c', metavar='COMMAND', help='send RCON command')
    actions.add_argument('--test', '-t', action='store_true', help='test')
    parser.add_argument('--pwfile', '-p', default=None, help='a file containing the server RCON password')
    parser.add_argument('--host', '-H', default='localhost', help='the RCON port. Default: localhost')
    parser.add_argument('--port', '-P', type=int, default=25575, help='the RCON host. Default: 25575')
    args = parser.parse_args()

    password = None
    if args.pwfile:
        with open(args.pwfile) as file:
            password = file.readline().strip()

    ctl = ServerCtl(args.host, args.port, password)

    if args.start:
        ctl.start_server()

    elif args.notify_restart:
        ctl.notify_restart(args.notify_restart)

    elif args.restart:
        ctl.restart()

    elif args.cmd:
        print(ctl.exec_cmd(args.cmd))

    elif args.test:
        with ctl._create_rcon_connection() as rcon:
            print(rcon.cmd('list'))
            print(rcon.cmd('list'))
            print(rcon.cmd('clone'))
            print(rcon.cmd('list'))
            print(rcon.cmd('help 8'))
