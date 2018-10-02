#!/usr/bin/env python
# encoding: utf-8
from colorama import Fore

def the_banner():
    banner_logo = Fore.RED + """
                    ___ ___ _____   _____         _   _             
            |_ _/ _ \_   _| |_   _|__  ___| |_(_)_ __   __ _ 
            | | | | || |     | |/ _ \/ __| __| | '_ \ / _` |
            | | |_| || |     | |  __/\__ \ |_| | | | | (_| |
            |___\___/ |_|     |_|\___||___/\__|_|_| |_|\__, |
                                                    |___/ 
             Powered by JHU - https://www.xxx.com/
                              Version: 0.0.1                                           
            """
    print(banner_logo)