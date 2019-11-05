from mcrcon import mcrcon
import argparse
import socket
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--notify', type=int)
    parser.add_argument('--restart', action='store_true')
    parser.add_argument('password')
    args = parser.parse_args()

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
            subprocess.run(['tmux', 'kill-session', '-t', 'mc'])
            subprocess.run(['tmux', 'new-session', '-d', '-s', 'mc', 'bash --init-file /home/magnus/ftb_server/ServerStart.sh'])

    finally:
        sock.close()


if __name__ == '__main__':
    main()