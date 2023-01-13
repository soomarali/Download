# -*- coding: utf-8 -*-
# code: BY MOHAMED_OS


from os import chdir, popen, remove, system
from os.path import isfile, join
from re import MULTILINE, findall
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


class YouTube():
    link = "https://raw.githubusercontent.com/MOHAMED19OS/Download/main/YouTube/"
    page = "https://github.com/MOHAMED19OS/Download/tree/main/YouTube"

    def __init__(self):
        self.plugin_dir = '/usr/lib/enigma2/python/Plugins/Extensions/YouTube/'
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
            self.uninstall = 'opkg remove --force-depends'
            self.list = 'opkg list-installed'
            self.extension = 'ipk'
        else:
            self.status = '/var/lib/dpkg/status'
            self.update = 'apt-get update >/dev/null 2>&1'
            self.install = 'apt-get install'
            self.uninstall = 'apt-get purge --auto-remove'
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

    def version(self):
        check = popen(" ".join([self.list, self.package])).read().split("-")[-2].strip()
        return check.split('+')[-2]

    def banner(self):
        system('clear')
        print(B, r"""
Y88b   d88P            88888888888       888
 Y88b d88P                 888           888
  Y88o88P                  888           888
   Y888P  .d88b.  888  888 888  888  888 88888b.   .d88b.
    888  d88""88b 888  888 888  888  888 888 "88b d8P  Y8b
    888  888  888 888  888 888  888  888 888  888 88888888
    888  Y88..88P Y88b 888 888  Y88b 888 888 d88P Y8b.
    888   "Y88P"   "Y88888 888   "Y88888 88888P"   "Y8888""", C)

    def main(self):
        self.stb_Image()

        self.banner()
        print("\n{}(!){} Please Wait Check Package ...".format(R, C))
        system(self.update)
        sleep(1)

        if not self.stb_Image():
            self.depends.extend("gstreamer1.0-plugins-base-meta",
                                "gstreamer1.0-plugins-good-spectrum")

        for pkg_name in self.depends:
            if not self.package_check(pkg_name):
                system('clear')
                print("     Need To InsTall : {}{}{}\n".format(Y, pkg_name, C))
                system(" ".join([self.install, pkg_name]))
                sleep(1)

        system('clear')
        self.banner()
        sleep(2)

        file = self.info()

        if isfile(join('/tmp/', file)):
            remove(join('/tmp/', file))
            sleep(0.8)

        if self.version() == file.split('+')[-2].strip():
            print('\nyou are use the latest version: {}{}{}\n'.format(
                Y, file.split('+')[-2].strip(), C).capitalize())
            sleep(0.8)
            print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
            exit()
        else:
            system("".join([self.uninstall, file.split('_')[0]]))

        system('clear')
        self.banner()
        print("\n{}Please Wait{} while we Download And Install {}YouTube{} ...".format(
            G, C, Y, C))

        chdir('/tmp')

        urlretrieve("".join([self.link, file]), filename=file)
        sleep(0.8)

        system(" ".join([self.install, file]))
        sleep(1)

        if isfile(join('/tmp/', file)):
            remove(join('/tmp/', file))
            sleep(0.8)

        if isfile('/etc/enigma2/YouTube.key-opkg'):
            remove('/etc/enigma2/YouTube.key-opkg')

        if not isfile(join(self.plugin_dir, 'version')):
            with open(join(self.plugin_dir, 'version')) as f:
                f.write("version={}".format(file.split('+')[-2].strip()))

        if self.stb_Image():
            system('killall -9 enigma2')
        else:
            system('systemctl restart enigma2')


if __name__ == '__main__':
    build = YouTube()
    build.main()
    print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)".format(R, C))
