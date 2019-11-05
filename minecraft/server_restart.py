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
    result.append('{} second{}'.format(secs, '' if secs == 1 else 's'))

    if len(result) == 1:
        return result[0]
    else:
        return ', '.join(result[:-1]) + ' and ' + result[-1]


def start_server():
    subprocess.run(['tmux', 'kill-session', '-t', 'mc'])
    subprocess.run(['tmux', 'new-session', '-d', '-s', 'mc', 'bash --init-file ServerStart.sh'], cwd='/home/magnus/ftb_server')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--notify', type=int, metavar='SECONDS', help='just send notification that server will restart in SECONDS')
    parser.add_argument('--restart', action='store_true', help='restart server')
    parser.add_argument('password', help='the server RCON password')
    args = parser.parse_args()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 25575))

        try:
            if not mcrcon.login(sock, args.password):
                print('Incorrect RCON password')
                return

            if args.notify:
                response = mcrcon.command(sock, 'say Server will restart in {}'.format(seconds_to_str(args.notify)))
                print(response)

            elif args.restart:
                response = mcrcon.command(sock, 'say Server will restart now')
                print(response)
                response = mcrcon.command(sock, 'save-all')
                print(response)
                response = mcrcon.command(sock, 'stop')
                print(response)
                time.sleep(5)
                start_server()

        finally:
            sock.close()

    except socket.error as err:
        print('Error connecting to server: ', err)
        if err.errno == errno.ECONNREFUSED:
            print('Just starting the server instead')
            start_server()


if __name__ == '__main__':
    main()
