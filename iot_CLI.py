# -*- coding:utf-8 -*-

from subInterpreter import *
from interface import *

PROMPT = "IOT-CLI"


class IOT_CLI(Cmd):
    prompt = PROMPT + '> '

    intro = Fore.CYAN + "Welcome! Here is the version 0.0.1 of IOT Framework CLI, default mode is a shell interface\n\n\
    Core Commands:\n\
    ==============================================\n \
    tools\t\t show all avaiable tools with descriptions in CLI\n \
    resource\t\t show all avaiable resource\n \
    clear\t\t clear the output\n \
    exit or q\t\t exit the CLI\n\n \
    <> \t\t otherwise default is shell mode\n\n\
    Type ? to list full commands\n\
    And you can type help <command> to get help\n\
    ==============================================" + Fore.RESET

    def do_resource(self, input):
        sub_cmd = Resource_Interface()
        sub_intro = Fore.LIGHTCYAN_EX + "\nHere is a resource sub-module:\n\
        ==============================================\n \
        show\t\t show all avaiable resource\n \
        xx\t\t use a xx\n \
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
