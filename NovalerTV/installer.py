# -*- coding: utf-8 -*-
# code BY: MOHAMED_OS

from os import chdir, popen, remove, system
from os.path import isfile, join
from re import MULTILINE, findall
from socket import gethostname
from sys import version_info
from time import sleep

if version_info[0] == 3:
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen, urlretrieve
else:
    from urllib import urlretrieve

    from urllib2 import HTTPError, Request, URLError, urlopen

# colors
C = "\033[0m"     # clear (end)
R = "\033[0;31m"  # red (error)
G = "\033[0;32m"  # green (process)
B = "\033[0;36m"  # blue (choice)
Y = "\033[0;33m"  # yellow (info)


class NovalerTV():
    URL = 'https://raw.githubusercontent.com/MOHAMED19OS/Download/main/NovalerTV/'
    page = "https://github.com/MOHAMED19OS/Download/tree/main/NovalerTV"

    def __init__(self):
        self.hostname = gethostname()
        self.package = ['python-core', 'python-image', 'python-json',
                        'python-multiprocessing', 'python-requests', 'python-imaging', 'enigma2-plugin-systemplugins-serviceapp', 'exteplayer3', 'gstplayer', 'ffmpeg']

        if version_info[0] == 3:
            self.package = list(
                map(lambda x: x.replace('python', 'python3').replace('python3-imaging', 'python3-pillow'), self.package))

    def Stb_Image(self):
        if isfile('/etc/opkg/opkg.conf'):
            self.status = '/var/lib/opkg/status'
            self.update = 'opkg update >/dev/null 2>&1'
            self.install = 'opkg install'
            self.uninstall = 'opkg remove --force-depends'

    def info(self, name):
        try:
            req = Request(self.page)
            req.add_header(
                'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0')
            response = urlopen(req)
            link = response.read().decode('utf-8')
            return findall(r"".join(['href=.*?\/NovalerTV.*?">.*?(.*?', name, '.*?)<']), link)[0]
        except HTTPError as e:
            print('HTTP Error code: ', e.code)
        except URLError as e:
            print('URL Error: ', e.reason)

    def banner(self):
        system('clear')
        print(B, r""""
888b    888                            888              88888888888 888     888
8888b   888                            888                  888     888     888
88888b  888                            888                  888     888     888
888Y88b 888  .d88b.  888  888  8888b.  888  .d88b.  888d888 888     Y88b   d88P
888 Y88b888 d88""88b 888  888     "88b 888 d8P  Y8b 888P"   888      Y88b d88P
888  Y88888 888  888 Y88  88P .d888888 888 88888888 888     888       Y88o88P
888   Y8888 Y88..88P  Y8bd8P  888  888 888 Y8b.     888     888        Y888P
888    Y888  "Y88P"    Y88P   "Y888888 888  "Y8888  888     888         Y8P
""", C)

    def check(self, pkg):
        with open(self.status) as file:
            for item in file.readlines():
                if item.startswith('Package:'):
                    if findall(pkg, item[item.index(' '):].strip(), MULTILINE):
                        return True
            file.close()

    def version(self, name):
        return popen("opkg info {} | grep Version | awk '{{print $2}}'".format(name)).read().strip()

    def main(self):
        self.Stb_Image()

        for filename in self.package:
            if not self.check(filename):
                system(self.update)
                system('clear')
                print("   >>>>   {}Please Wait{} while we Install {}{}{} ...".format(
                    G, C, Y, filename, C))
                system(" ".join([self.install, filename]))
                sleep(1)

        system('clear')
        self.banner()
        sleep(2)

        if version_info[0] == 3:
            file = self.info('python3')
        else:
            file = self.info('python2')

        if isfile(join('/tmp/', file)):
            remove(join('/tmp/', file))
            sleep(0.8)

        if self.version(file.split('_')[0]) == file.split('_')[1]:
            system('clear')
            print('you are use the latest version: {}{}{}\n'.format(
                Y, file.split('_')[1], C).capitalize())
            sleep(0.8)
            print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
            exit()
        else:
            system("".join([self.uninstall, file.split('_')[0]]))

        system('clear')
        print("{}Please Wait{} while we Download And Install {}NovalerTV{} ...".format(
            G, C, Y, C))

        chdir('/tmp')

        urlretrieve("".join([self.URL, file]), filename=file)
        sleep(0.8)

        system(" ".join([self.install, file]))
        sleep(1)

        if isfile(join('/tmp/', file)):
            remove(join('/tmp/', file))
            sleep(0.8)


if __name__ == '__main__':
    build = NovalerTV()
    build.main()
    print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)".format(R, C))
