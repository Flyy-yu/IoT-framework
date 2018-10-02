# -*- coding:utf-8 -*-
from cmd import Cmd
import tempfile
import subprocess
import os
import sys
import platform
from time import sleep
from nbstreamreader import NonBlockingStreamReader as NBSR
from resources import banner
from colorama import Fore

class MyPrompt(Cmd):
    prompt = 'IOT-CLI> '
    intro = Fore.CYAN + "Welcome! Here is the version 0.0.1 of IOT Framework CLI, default mode is a shell interface\n\n\
    Core Commands:\n\
    ==============================================\n \
    netstat\t\t execute netstat in CLI\n \
    new\t\t create a new terminal\n \
    clear\t\t clear the output\n\
    quit or q\t\t exit the CLI\n\
    Type ? to list full commands" + Fore.RESET

    def do_exit(self, input):
        print(Fore.YELLOW+"Bye"+Fore.RESET)
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
    #Call an external program in python and retrieve the output/return code with subprocess
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
    '''
    #WIP
    #Call an external program in python and retrieve the output/return code with subprocess
    def do_ping(self, input):
        # run the shell as a subprocess:
        p = subprocess.Popen(['python', 'resources/script.py'],
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
        print("exec script.py")
    '''
    def do_new(self, input):
        #Mac
        if platform.system() == "Darwin":
            command = 'open -W -a Terminal.app'
            p = subprocess.Popen(command, shell=True)
            p.wait()
            p.terminate()
        elif platform.system() == "Linux":
            try:
                command = 'gnome-terminal'
                p = subprocess.Popen(command, shell=True)
                p.wait()
                p.terminate()
            except: 
                command = 'xterm'
                p = subprocess.Popen(command, shell=True)
                p.wait()
                p.terminate()
            
        elif platform.system() == "Windows":
            command = 'start /wait'
        #Unknown OS: modification
        else: 
            print("Unknown OS, You can modify the code in iot_CLI.py:92 or search keyword 'Unknown OS: modification' to modify")
       
        # os.system("sudo chmod a+x new_terminal.sh")
        # subprocess.call("./new_terminal.sh")

    def help_new(self):
        print("create a new terminal...")

    # a func used to test stuff 
    def do_test(self): 
        pass

    def help_test(self):
         print("a func used to test stuff...")

    def default(self, input):

        if input == 'x' or input == 'q':
            return self.do_exit(input)
        else:
            #"Run a shell command"
            print(Fore.GREEN + "\nRunning shell command in default: {}\n".format(input) + Fore.RESET)
            output = os.popen(input).read()
            print(output)
            self.last_output = output

    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == '__main__':
    banner.the_banner()
    cli = MyPrompt()
    cli.doc_header = cli.intro
    cli.cmdloop()
