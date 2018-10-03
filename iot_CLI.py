# -*- coding:utf-8 -*-
from cmd import Cmd
import json
import signal
import subprocess
import time
import os
import sys
import platform
import atexit
import shlex
import textwrap
from resources import banner
from colorama import Fore
from resources.prettytable import PrettyTable
from tools.ping import ping_usage
PROMPT = "IOT-CLI"


class Ping_SubInterpreter(Cmd):

    def do_ping(self, args):
        print(ping_usage.get_basic_command(args))

    def do_back(self, args):
        print("Back to Pre CLI...")
        return True
    def help_back(self):
        print("Back to Pre CLI...")

class Tftp_SubInterpreter(Cmd):

    def do_tftp(self, args):
        pass

    def do_back(self, args):
        print("Back to Pre CLI...")
        return True
    def help_back(self):
        print("Back to Pre CLI...")

class Tools_Interface(Cmd):
    prompt = PROMPT + ">>" + Fore.RED + " (tools_lib)> " + Fore.RESET

    def do_show(self, input):
        # WIP now just implementing basic functioning
        t = PrettyTable(header_style='upper', padding_width=0)
        t.field_names = ["Tools name", "Description", "Example"]
        t.align["Tools name"] = "c"
        t.align["Description"] = "l"
        t.align["Example"] = "l"

        with open('tools/tools.json') as f:
            tool_info = json.load(f)
            #print tool_info
            for tool in tool_info['Tools'].keys():
                name = textwrap.fill(str(tool), 20)
                description = textwrap.fill(
                    str(tool_info['Tools'][name]['Description']), 50)
                example = textwrap.fill(
                    str(tool_info['Tools'][name]['Example']), 30)
                t.add_row([name, description, example])
                padding = '{s:{c}^{n}}'.format(s='-', n=20, c='-')
                t.add_row([padding, padding, padding])
        print(t)

    def help_show(self):
        print("show included tools with descriptions...")

    def do_use(self, command):
        if command.lower() == 'ping':
            use_cli = Ping_SubInterpreter()
            use_cli.prompt = PROMPT + ">>" + Fore.RED + " (tools_lib)>> " + command + ">> " + Fore.RESET 
            use_cli.cmdloop()
        elif command.lower() == 'tftp':
            use_cli = Ping_SubInterpreter()
            use_cli.prompt = PROMPT + ">>" + Fore.RED + " (tools_lib)>> " + command + ">> " + Fore.RESET 
            use_cli.cmdloop()
        else:
            print(Fore.YELLOW+"Unknown Tools name, you can type 'show' to know all supported tools."+Fore.RESET)

    def do_back(self, args):
        print("Back to Main CLI...")
        return True
    def help_back(self):
        print("Back to Main CLI...")

    #do_EOF = do_back


class MyPrompt(Cmd):
    prompt = PROMPT + '> '

    intro = Fore.CYAN + "Welcome! Here is the version 0.0.1 of IOT Framework CLI, default mode is a shell interface\n\n\
    Core Commands:\n\
    ==============================================\n \
    tools\t\t show all avaiable tools with descriptions in CLI\n \
    new\t\t create a new terminal\n \
    clear\t\t clear the output\n \
    quit or q\t\t exit the CLI\n\n \
    Type ? to list full commands\n\
    And you can type help <command> to get help\n\
    ==============================================" + Fore.RESET

    def do_tools(self, input):
        sub_cmd = Tools_Interface()
        sub_intro = Fore.LIGHTCYAN_EX + "\nHere is a tools_lib sub-module:\n\
        ==============================================\n \
        show\t\t show all avaiable tools with descriptions in CLI\n \
        use\t\t use a tool\n \
        back\t\t back to the main CLI\n\n \
        Type ? to list full commands\n\
        And you can type help <command> to get help\n\
        ==============================================" + Fore.RESET
        sub_cmd.intro = sub_intro
        sub_cmd.doc_header = sub_cmd.intro + "\n\nSupported Commands\n=============================="
        sub_cmd.undoc_header = Fore.LIGHTYELLOW_EX + '\nSub Modules \n==========================='+Fore.RESET
        sub_cmd.ruler = ''
        sub_cmd.cmdloop()

    def do_exit(self, input):
        print(Fore.YELLOW+"Bye"+Fore.RESET)
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
    # Call an external program in python and retrieve the output/return code with subprocess

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
        # Mac
        if platform.system() == "Darwin":
            command = 'open -a Terminal "`pwd`"'
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
        # Unknown OS: modification
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
            print(
                Fore.GREEN + "\nRunning shell command in default: {}\n".format(input) + Fore.RESET)
            #output = os.popen(input).read()
            # print(output)
            process = subprocess.Popen(
                shlex.split(input), stdout=subprocess.PIPE)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print output.strip()
            try:
                rc = process.poll()
            except KeyboardInterrupt:
                print("exiting...")
            except OSError:
                print("OS Error: wrong command")
            # return rc
            #self.last_output = output

    #do_EOF = do_exit
    #help_EOF = help_exit


def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)


if __name__ == '__main__':
    banner.the_banner()
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    cli = MyPrompt()
    cli.doc_header = cli.intro + "\n\nSupported Commands\n=============================="
    #cli.misc_header = '123'
    cli.undoc_header = Fore.LIGHTYELLOW_EX + \
        'Sub Modules \n==========================='+Fore.RESET
    cli.ruler = ''
    cli.cmdloop()
