# -*- coding:utf-8 -*-

from subInterpreter import *
from tools.ping import ping_usage

PROMPT = "IOT-CLI"


# tools libs sub-module
#   second level
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
            # print tool_info
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
        prompt = PROMPT + ">>" + Fore.RED + \
                 " (tools_lib)>> " + Fore.RESET + \
                 Back.RED + command + " >>>" + Back.RESET
        json_dir = 'tools/{}/config.json'.format(command.lower())
        if command.lower() == 'arpspoof':
            use_cli = ArpspoofSubInterpreter(json_dir)
        elif command.lower() == 'tftp':
            use_cli = TftpSubInterpreter(json_dir)
        elif command.lower() == 'hydra':
            use_cli = HydraSubInterpreter(json_dir)
        elif command.lower() == 'killerbee':
            use_cli = KillerbeeSubInterpreter(json_dir)
        elif command.lower() == 'apktools':
            use_cli = ApktoolsSubInterpreter(json_dir)
        elif command.lower() == 'ropgadget':
            use_cli = RopgadgetSubInterpreter(json_dir)
        elif command.lower() == 'kismet':
            use_cli = KismetSubInterpreter(json_dir)
        elif command.lower() == 'ping':
            use_cli = PingSubInterpreter(json_dir)
        elif command.lower() == 'firmwalker':
            use_cli = FirmwalkerSubInterpreter(json_dir)
        elif command.lower() == 'baudrate':
            use_cli = BaudrateSubInterpreter(json_dir)
        elif command.lower() == 'binwalk':
            use_cli = BinwalkSubInterpreter(json_dir)
        elif command.lower() == 'tcpdump':
            use_cli = TcpdumpSubInterpreter(json_dir)
        else:
            print(
                Fore.YELLOW + "Unknown Tools name, you can type 'show' to know all supported tools." + Fore.RESET)
            return

        use_cli.prompt = prompt
        use_cli.cmdloop()

    def do_back(self, args):
        print("Back to Main CLI...")
        return True

    def help_back(self):
        print("Back to Main CLI...")

        # do_EOF = do_back


class IOT_CLI(Cmd):
    prompt = PROMPT + '> '

    intro = Fore.CYAN + "Welcome! Here is the version 0.0.1 of IOT Framework CLI, default mode is a shell interface\n\n\
    Core Commands:\n\
    ==============================================\n \
    tools\t\t show all avaiable tools with descriptions in CLI\n \
    clear\t\t clear the output\n \
    exit or q\t\t exit the CLI\n\n \
    <> \t\t otherwise default is shell mode\n\n\
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
        sub_cmd.doc_header = sub_cmd.intro + \
                             "\n\nSupported Commands\n=============================="
        sub_cmd.undoc_header = Fore.LIGHTYELLOW_EX + \
                               '\nSub Modules \n===========================' + Fore.RESET
        sub_cmd.ruler = ''
        sub_cmd.cmdloop()

    def do_exit(self, input):
        print(Fore.YELLOW + "Bye" + Fore.RESET)
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    '''
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
    
    # create an new terminal
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
            print(
                "Unknown OS, You can modify the code in iot_CLI.py:92 or search keyword 'Unknown OS: modification' to modify")

            # os.system("sudo chmod a+x new_terminal.sh")
            # subprocess.call("./new_terminal.sh")

    def help_new(self):
        print("create a new terminal...")
    '''
    # a func used to test stuff
    def do_test(self):
        pass

    def help_test(self):
        print("a func used to test stuff...")

    def default(self, input):
        # func used to capture stdout in real-time
        def run_command_real_time(command):
            try:
                process = subprocess.Popen(
                    shlex.split(command), stdout=subprocess.PIPE)
                while True:
                    output = process.stdout.readline()
                    # output,error = process.communicate()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
                rc = process.poll()
                return rc
            except OSError as e:
                # print("OSError > ",e.errno)
                print
                "OSError > ", e.strerror
                # print("OSError > ",e.filename)
                print(
                    Fore.RED + "Note: Default Shell mode, please check you input" + Fore.RESET)
            except ValueError:
                pass
            except:
                print("Error > ", sys.exc_info()[0])

        if input == 'x' or input == 'q':
            return self.do_exit(input)
        else:
            # "Run a shell command"
            print(
                Fore.GREEN + "\nRunning shell command in default: {}\n".format(input) + Fore.RESET)
            run_command_real_time(input)


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
    cli = IOT_CLI()
    cli.doc_header = cli.intro + "\n\nSupported Commands\n=============================="
    # cli.misc_header = '123'
    cli.undoc_header = Fore.LIGHTYELLOW_EX + \
                       'Sub Modules \n===========================' + Fore.RESET
    cli.ruler = ''
    cli.cmdloop()
