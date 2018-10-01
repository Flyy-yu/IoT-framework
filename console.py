# -*- coding:utf-8 -*-
from cmd import Cmd
import tempfile
import subprocess
import os
import sys
from time import sleep
from nbstreamreader import NonBlockingStreamReader as NBSR
from banner import banner
from resource import color

class MyPrompt(Cmd):
    prompt = 'IOT-Power> '
    intro = "Welcome! Type ? to list commands"

    def do_hello(self, s):
        if s == '':
            name = input('Your name please: ')
        else:
            name = s
        print ('Hello', name)

    def help_hello(self):
        print("interactive func")

    def do_exit(self, input):
        print("Bye")
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def do_add(self, input):
        print("adding '{}'".format(input))

    def help_add(self):
        print("Add a new entry to the system.")

    def do_netstat(self, input):
        ## command to run - tcp only ##
        cmd = "netstat -p tcp -f inet"

        ## run it ##
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

        ## But do not wait till netstat finish, start displaying output immediately ##
        while True:
            out = p.stderr.read(1)
            if out == '' and p.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()

    def help_netstat(self):
        print("execc netstat")

    def do_ping(self, input):
        # run the shell as a subprocess:
        p = subprocess.Popen(['python', 'shell.py'],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        # wrap p.stdout with a NonBlockingStreamReader object:
        nbsr = NBSR(p.stdout)
        # issue command:
        p.stdin.write(b'command\n')
        # get the output
        while True:
            output = nbsr.readline(0.1)
            # 0.1 secs to let the shell output the result
            if not output:
                print('[No more data]')
                break
            print(output)

    def help_ping(self):
        print("exec ping.py")

    def do_new(self, input):
        dirname = os.getcwd()
        with tempfile.NamedTemporaryFile(suffix='.command', dir=dirname) as f:
            f.write('#!/bin/sh\nls\n')
            # subprocess.call(['sudo chmod u+x', f.name])
            os.system("sudo chmod u+x {}".format(f.name))
            command = 'open -W ' + f.name
            p = subprocess.Popen(command, shell=True)
            p.wait()
        p.terminate()
        # os.system("sudo chmod a+x new_terminal.sh")
        # subprocess.call("./new_terminal.sh")

    def help_new(self):
        print("create a new terminal...")

    def default(self, input):

        if input == 'x' or input == 'q':
            return self.do_exit(input)
        else:
            subprocess.Popen(['/bin/bash', '-c', input], shell=False)
            print("Default Bash Mode, press ? or type help to list commands\n\n")

    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == '__main__':
    banner()
    MyPrompt().cmdloop()
