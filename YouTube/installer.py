# -*- coding: utf-8 -*-
# code: BY MOHAMED_OS


from os import popen, system
from os.path import isfile
from re import MULTILINE, findall
from sys import version_info

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


class YouTube():
    link = "https://raw.githubusercontent.com/MOHAMED19OS/Download/main/YouTube"
    page = "https://github.com/MOHAMED19OS/Download/tree/main/YouTube"

    def __init__(self):
        self.package = "enigma2-plugin-extensions-youtube"
        self.depends = ["python-codecs", "python-core",
                        "python-json", "python-netclient"]

        if version_info[0] == 3:
            self.depends = list(
                map(lambda x: x.replace('python', 'python3'), self.depends))

    def stb_Image(self):
        if isfile('/etc/opkg/opkg.conf'):
            self.status = '/var/lib/opkg/status'
            self.update = 'opkg update >/dev/null 2>&1'
            self.install = 'opkg install'
            self.list = 'opkg list-installed'
            self.extension = 'ipk'
        else:
            self.status = '/var/lib/dpkg/status'
            self.update = 'apt-get update >/dev/null 2>&1'
            self.install = 'apt-get install'
            self.list = 'apt-get list-installed'
            self.extension = 'deb'
        return isfile('/etc/opkg/opkg.conf')

    def package_check(self, name):
        with open(self.status) as file:
            for item in file.readlines():
                if item.startswith('Package:'):
                    if findall(name, item[item.index(' '):].strip(), MULTILINE):
                        return True
            file.close()

    def info(self):
        try:
            req = Request(self.page)
            req.add_header(
                'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0')
            response = urlopen(req)
            link = response.read().decode('utf-8')
            return findall(r"".join(['href=.*?\/', self.package, '.*?>(.*?\.', self.extension, ')<.*?']), link)[0]
        except HTTPError as e:
            print('HTTP Error code: ', e.code)
        except URLError as e:
            print('URL Error: ', e.reason)

    def check(self):
        return popen(" ".join([self.list, self.package])).read().split("-")[-2].strip()

    def banner(self):
        system('clear')
        print(B,r"""
Y88b   d88P            88888888888       888
 Y88b d88P                 888           888
  Y88o88P                  888           888
   Y888P  .d88b.  888  888 888  888  888 88888b.   .d88b.
    888  d88""88b 888  888 888  888  888 888 "88b d8P  Y8b
    888  888  888 888  888 888  888  888 888  888 88888888
    888  Y88..88P Y88b 888 888  Y88b 888 888 d88P Y8b.
    888   "Y88P"   "Y88888 888   "Y88888 88888P"   "Y8888""", C)

if __name__ == '__main__':
    build = YouTube()
    build.banner()
    print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)".format(R, C))
