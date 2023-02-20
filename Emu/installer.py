# -*- coding: utf-8 -*-
# code BY: MOHAMED_OS

from __future__ import print_function

from os import chdir, chmod, popen, remove, system
from os.path import exists, isfile, join
from re import MULTILINE, findall, match
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


if hasattr(__builtins__, 'raw_input'):
    input = raw_input


class Emulator():
    URL = 'https://raw.githubusercontent.com/MOHAMED19OS/Download/main/Emu/'
    page = "https://github.com/MOHAMED19OS/Download/tree/main/Emu"

    def __init__(self):
        self.package = 'enigma2-plugin-softcams-'

    def Stb_Image(self):
        if isfile('/etc/opkg/opkg.conf'):
            self.status = '/var/lib/opkg/status'
            self.update = 'opkg update >/dev/null 2>&1'
            self.install = 'opkg install'
            self.list = 'opkg list'
            self.uninstall = 'opkg remove --force-depends'
            self.extension = 'ipk'
        else:
            self.status = '/var/lib/dpkg/status'
            self.update = 'apt-get update >/dev/null 2>&1'
            self.install = 'apt-get install'
            self.list = 'apt-get list'
            self.uninstall = 'apt-get purge --auto-remove'
            self.extension = 'deb'
        return isfile('/etc/opkg/opkg.conf')

    def info(self, name):
        try:
            req = Request(self.page)
            req.add_header(
                'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0')
            response = urlopen(req)
            link = response.read().decode('utf-8')
            return findall(r"".join(['href=.*?\/Emu.*?">.*?', name, '_(.*?)_']), link)[0]
        except HTTPError as e:
            print('HTTP Error code: ', e.code)
        except URLError as e:
            print('URL Error: ', e.reason)

    def banner(self):
        system('clear')
        print(B,
              r"""
            d88888b .88b  d88. db    db db       .d8b.  d888888b  .d88b.  d8888b.
            88'     88'YbdP`88 88    88 88      d8' `8b `~~88~~' .8P  Y8. 88  `8D
            88ooooo 88  88  88 88    88 88      88ooo88    88    88    88 88oobY'
            88~~~~~ 88  88  88 88    88 88      88~~~88    88    88    88 88`8b
            88.     88  88  88 88b  d88 88booo. 88   88    88    `8b  d8' 88 `88.
            Y88888P YP  YP  YP ~Y8888P' Y88888P YP   YP    YP     `Y88P'  88   YD""", C)
        print(
            "".join(["\t\t\t{}Oscam Version{}: ".format(Y, C), self.info('oscam')]))
        print(
            "".join(["\t\t\t{}Ncam Version{}: ".format(Y, C), self.info('ncam')]))

    def check(self, pkg):
        with open(self.status) as file:
            for item in file.readlines():
                if item.startswith('Package:'):
                    if findall(pkg, item[item.index(' '):].strip(), MULTILINE):
                        return True
            file.close()

    def prompt(self, choices):

        options = list(choices)
        options.sort(key=int)

        while True:
            print(
                "{}(?){} Choose an option [{}-{}] : ".format(B, C, options[0], options[-1]), end='')
            choice = [str(x) for x in input().split()]

            for name in choice:
                if name not in options:
                    print(
                        "\n{}(!){} Select one of the available options !!\n".format(R, C))
                    continue
            return choice

    def FixEmu(self):
        for name in ["RELOAD.sh", "SUPAUTO.sh"]:
            if exists(join("/etc/", name)):
                remove(join("/etc/", name))
            if exists('/etc/cron/crontabs/root'):
                self.RootPath = '/etc/cron/crontabs/root'
            else:
                self.RootPath = '/var/spool/cron/crontabs/root'
            with open(self.RootPath, "r+") as f:
                line = f.readline()
                f.seek(0)
                if name not in line:
                    f.write(line)
                f.truncate()
        with open('/etc/init.d/fixemu.sh', "w") as file:
            file.writelines("""#!/bin/bash\n
STB_IMAGE=$(cut /etc/opkg/all-feed.conf -d'-' -f1 | awk '{{ print $2 }}')

if [ $STB_IMAGE = 'egami' ] || [ $STB_IMAGE = 'openbh' ]; then
    update-rc.d -f softcam remove
    sleep 1
    unlink /etc/init.d/softcam

    sleep 1

    ln -sf /etc/init.d/softcam.None /etc/init.d/softcam
    update-rc.d softcam defaults

    if [ -e /etc/init.d/softcam.SupCam ]; then
        rm -rf /etc/init.d/softcam.SupCam
    fi

fi

if [ -e /etc/RELOAD.sh ]; then
    rm -rf /etc/RELOAD.sh
fi

if [ -e /etc/SUPAUTO.sh ]; then
    rm -rf /etc/SUPAUTO.sh
fi
sed -i '/RELOAD/d' {}
sed -i '/SUPAUTO/d' {}\n""".format(self.RootPath, self.RootPath))
            file.close()

        chmod('/etc/init.d/fixemu.sh', 0o755)
        system("update-rc.d fixemu.sh defaults >/dev/null 2>&1")

    def main(self):

        self.Stb_Image()

        if not self.check('libcurl4'):
            system('clear')
            print("   >>>>   {}Please Wait{} while we Install {}libcurl4{} ...".format(
                G, C, Y, C))
            system('{};{} libcurl4'.format(self.update, self.install))

        if self.Stb_Image():
            cam = {
                "1": "".join([self.package, "oscam"]),
                "2": "".join([self.package, "ncam"]),
                "3": "".join([self.package, "powercam"]),
                "4": "".join([self.package, "revcam"]),
                "5": "".join([self.package, "gosatplus"]),
                "6": "".join([self.package, "supcam-oscam"]),
                "7": "".join([self.package, "revcam-oscam"]),
                "8": "".join([self.package, "gosatplus-oscam"]),
                "9": "".join([self.package, "powercam-oscam"]),
                "10": "".join([self.package, "supcam-ncam"]),
                "11": "".join([self.package, "powercam-ncam"]),
                "12": "".join([self.package, "revcam-ncam"]),
                "13": "".join([self.package, "gosatplus-ncam"])
            }
            menu = """
                                (00) Exit

            (1) Oscam       (6)  SupTV_Oscam        (11) PowerCam_Ncam
            (2) Ncam        (7)  Revcam_Oscam       (12) Revcam_Ncam
            (3) PowerCam    (8)  GosatPlus_Oscam    (13) GosatPlus_Ncam
            (4) Revcam      (9)  PowerCam_Oscam
            (5) GosatPlus   (10) SupTV_Ncam
            """
        else:
            cam = {
                "1": "".join([self.package, "oscam"]),
                "2": "".join([self.package, "ncam"]),
                "3": "".join([self.package, "revcam"]),
                "4": "".join([self.package, "powercam"]),
                "5": "".join([self.package, "gosatplus"])
            }
            menu = """
                            (00) Exit

            (1) Oscam          (2) Ncam          (3) Revcam
            (4) PowerCam       (5) GosatPlus
            """
        self.banner()

        print(menu)
        choice = self.prompt(cam.keys())

        for number in choice:
            if number == '00':
                system('clear')
                self.banner()
                print("\nGoodBye ...!\n", "   Written by {}MOHAMED_OS{}(͡๏̯͡๏) \n".format(
                    B, C, R, C))
                exit()
            else:
                value = cam.get(number)
                self.file = "{}_{}_all.{}".format(
                    value, self.info(value.split('-')[-1]), self.extension)

                if self.check(value):
                    system('{} {} '.format(self.uninstall, value))

                if isfile(self.file):
                    remove(self.file)
                    sleep(0.8)

                chdir('/tmp')

                if self.Stb_Image():
                    UrlSsl = "".join(
                        [self.URL[:46], 'OpenSsl_IPK/main/OE2.0/'])
                    FileSsl = "libcrypto1.0.0_1.0.2_all.ipk"
                else:
                    UrlSsl = "".join(
                        [self.URL[:46], 'OpenSsl_IPK/main/OE2.6/'])
                    FileSsl = "libcrypto1.0.0_1.0.2h-r0.0_all.deb"

                if "powercam" in value:
                    CheckLib = popen(
                        " ".join([self.list, 'libcrypto-compat-1.0.0'])).read().split(' - ')[0]
                    if CheckLib == 'libcrypto-compat-1.0.0':
                        if not self.check('libcrypto-compat-1.0.0'):
                            system('clear')
                            print(
                                "   >>>>   {}Please Wait{} while we Install {}libcrypto-compat-1.0.0{} ...".format(G, C, Y, C))
                            system(
                                '{};{} libcrypto-compat-1.0.0'.format(self.update, self.install))
                    else:
                        if not self.check(FileSsl.split('_')[0]):
                            print(
                                "   >>>>   {}Please Wait{} while we Install {}{}{} ...".format(G, C, Y, FileSsl.split('_')[0], C))
                            urlretrieve(
                                "".join([UrlSsl, FileSsl]), filename=FileSsl)
                            system(" ".join([self.install, FileSsl]))
                            remove(FileSsl)

                system('clear')
                print("{}Please Wait{} while we Download And Install {}{}{} ...".format(
                    G, C, Y, value, C))

                urlretrieve("".join([self.URL, self.file]), filename=self.file)
                sleep(0.8)

                system(" ".join([self.install, self.file]))
                sleep(1)

                if "supcam" in value:
                    self.FixEmu()


if __name__ == '__main__':
    build = Emulator()
    build.main()
    print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)".format(R, C))
