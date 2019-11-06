from mcrcon import mcrcon
import argparse
import socket
import errno
import subprocess
import time


def seconds_to_str(s: int) -> str:
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
    if kill_session:
        subprocess.run(['tmux', 'kill-session', '-t', 'mc'])
    subprocess.run(['tmux', 'new-session', '-d', '-s', 'mc', 'bash --init-file ServerStart.sh'], cwd='/home/magnus/ftb_server')


def main(args):
    if args.start:
        print('Starting the server')
        start_server()

    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('localhost', 25575))

            try:
                if not mcrcon.login(sock, args.password):
                    print('Incorrect RCON password')
                    return

                if args.notify_restart:
                    print(mcrcon.command(sock, 'say Server will restart in {}'.format(seconds_to_str(args.notify_restart))))

                elif args.restart:
                    print(mcrcon.command(sock, 'say Server will restart now'))
                    print(mcrcon.command(sock, 'save-all'))
                    print(mcrcon.command(sock, 'stop'))
                    time.sleep(5)
                    start_server(kill_session=True)

            except socket.error as err:
                print('Error connecting to RCON: ', err)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--notify-restart', '-n', type=int, metavar='SECONDS', help='send notification that server will restart in SECONDS')
    parser.add_argument('--restart', '-r', action='store_true', help='restart server')
    parser.add_argument('--start', '-s', action='store_true', help='start server')
    parser.add_argument('--cmd', '-c', metavar='COMMAND', help='send RCON command')
    parser.add_argument('password', help='the server RCON password')
    args = parser.parse_args()
    main(args)
