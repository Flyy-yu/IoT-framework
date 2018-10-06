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
from colorama import Fore, Back
from resources.prettytable import PrettyTable
from tools.ping import ping_usage
from tools.hydra import tools
PROMPT = "IOT-CLI"

# JSON CONFIG FILES API


class UtilityTool(object):
    def __init__(self, config_file):
        with open(config_file, 'r') as fp:
            self.config = self.load_config(fp)
        self.name = self.config["name"]
        self.version = self.config["version"]
        self.intro = self.config["intro"]
        self.links = self.config["links"]

    def load_config(self, config_file):
        config_file = json.load(config_file)
        return config_file

    # generate system command
    def get_command_info(self):
        command_dict = dict(self.config["command"])
        return command_dict

    def check_cmd(self, cmd):
        for key, value in cmd.items():
            if key in self.config["command"] and value in self.config["command"][key]:
                for req_item, info in self.config["command"][key][value].items():
                    if req_item not in cmd:
                        return 'Error option "{}" needs "{}"'.format(value, req_item)
        return 1

    def get_basic_command(self, cmd_dict):
        self.cmd_string = None
        return self.cmd_string

    # TODO execuate the command
    def run_command(self):
        return 1

# API: Print table 


class Print_Utils(object):

    def print_info_table(self, dir):
        tool_info = UtilityTool(dir)
        info_table = PrettyTable(header_style='upper', padding_width=0)
        info_table.field_names = ["Name", "Version", "Intro", "Links"]
        info_table.align["Name"] = "c"
        info_table.align["Version"] = "c"
        info_table.align["Intro"] = "c"
        info_table.align["Links"] = "c"
        name = textwrap.fill(str(tool_info.name), 10)
        version = textwrap.fill(str(tool_info.version), 10)
        intro = textwrap.fill(str(tool_info.intro), 60)
        links = textwrap.fill(str(tool_info.links), 60)
        info_table.add_row([name, version, intro, links])
        return info_table

    def print_options(self, dir):
        hydra_option = UtilityTool(dir).get_command_info()
        option_table = PrettyTable(header_style='upper', padding_width=0)
        option_table.field_names = ["Option Name",
                                    "Current Setting", "Required", "Description"]
        option_table.align["Option Name"] = "c"
        option_table.align["Current Setting"] = "c"
        option_table.align["Required"] = "c"
        option_table.align["Description"] = "c"
        # hydra_option['']
        for item in hydra_option.keys():
            option_name = textwrap.fill(item, 10)
            current_setting = textwrap.fill(
                str(hydra_option[item]['default']), 20)
            required = textwrap.fill(str(hydra_option[item]['required']), 10)
            description = textwrap.fill(str(hydra_option[item]['intro']), 60)
            option_table.add_row(
                [option_name, current_setting, required, description])
            #padding = '{s:{c}^{n}}'.format(s='-', n=20, c='-')
            next_line = ''
            option_table.add_row([next_line, next_line, next_line, next_line])
        return option_table

#  API: Update json config file
class Update_Setting(object):
    # seek() to move the cursor back to the beginning of the file then start writing,
    # followed by a truncate() to deal with the case where the new data is smaller than the previous.
    def set_setting(self, DIR, option_name, new_value):
        with open(DIR, "r+") as jsonFile:
            data = json.load(jsonFile)
            data["command"][option_name]['default'] = str(new_value)
            jsonFile.seek(0)  # rewind
            json.dump(data, jsonFile)
            jsonFile.truncate()

    def refresh(self, DIR):
        refreshing = Print_Utils()
        print("\nSETTING UPDATE!\n")
        print(refreshing.print_options(DIR))

# third level
class Hydra_SubInterpreter(Cmd):
    # static object: json file directory
    DIR = "tools/hydra/config.json"
    intro = Fore.MAGENTA + "Interface: Hydra\n\
    ==============================================\n \
    info\t\t show all descriptions in CLI\n \
    options\t\t show all options and current setting\n \
    set\t\t update config value\n \
    back\t\t back to the previous CLI level\n\n \
    Type ? to list full commands\n\
    And you can type help <command> to get help\n\
    ==============================================" + Fore.RESET
    def do_run(self, args):
        pass

    def do_options(self, args):
        options = Print_Utils()
        table = options.print_options(self.DIR)
        print(table)
        print("\nFor example, You can type:\n   set ip 192.168.1.1 \n\n to update current setting.")

    def help_options(self):
        print("show all options and arguments...")

    def do_info(self, args):
        # "tools/hydra/config.json"
        info = Print_Utils()
        table = info.print_info_table(self.DIR)
        print(table)

    def help_info(self):
        print("show all brief info ...")
    # update setting value from user's input

    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1].lower()
            if option_name == 'ip':
                update.set_setting(self.DIR, option_name, setting_value)
                update.refresh(self.DIR)
            elif option_name == 'protocol':
                update.set_setting(self.DIR, option_name, setting_value)
                update.refresh(self.DIR)
            elif option_name == 'wordlist':
                update.set_setting(self.DIR, option_name, setting_value)
                update.refresh(self.DIR)
            else:
                print("Please check the option name. Type 'options' to get help... ")

    def do_back(self, args):
        print("Back to Pre CLI...")
        return True

    def help_back(self):
        print("Back to Pre CLI...")


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
            use_cli.prompt = PROMPT + ">>" + Fore.RED + \
                " (tools_lib)>> " + Fore.RESET + \
                Back.RED + command + " >>>" + Back.RESET
            use_cli.cmdloop()
        elif command.lower() == 'tftp':
            use_cli = Ping_SubInterpreter()
            use_cli.prompt = PROMPT + ">>" + Fore.RED + \
                " (tools_lib)>> " + Fore.RESET + \
                Back.RED + command + " >>>" + Back.RESET
            use_cli.cmdloop()
        elif command.lower() == 'hydra':
            use_cli = Hydra_SubInterpreter()
            use_cli.prompt = PROMPT + ">>" + Fore.RED + \
                " (tools_lib)>> " + Fore.RESET + \
                Back.RED + command + " >>>" + Back.RESET
            use_cli.cmdloop()
        else:
            print(
                Fore.YELLOW+"Unknown Tools name, you can type 'show' to know all supported tools."+Fore.RESET)

    def do_back(self, args):
        print("Back to Main CLI...")
        return True

    def help_back(self):
        print("Back to Main CLI...")

    #do_EOF = do_back


class IOT_CLI(Cmd):
    prompt = PROMPT + '> '

    intro = Fore.CYAN + "Welcome! Here is the version 0.0.1 of IOT Framework CLI, default mode is a shell interface\n\n\
    Core Commands:\n\
    ==============================================\n \
    tools\t\t show all avaiable tools with descriptions in CLI\n \
    new\t\t create a new terminal\n \
    clear\t\t clear the output\n \
    quit or q\t\t exit the CLI\n\n \
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
            '\nSub Modules \n==========================='+Fore.RESET
        sub_cmd.ruler = ''
        sub_cmd.cmdloop()

    def do_exit(self, input):
        print(Fore.YELLOW+"Bye"+Fore.RESET)
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
        # func used to capture stdout in real-time
        def run_command_real_time(command):
            try:
                process = subprocess.Popen(
                    shlex.split(command), stdout=subprocess.PIPE)
                while True:
                    output = process.stdout.readline()
                    #output,error = process.communicate()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
                rc = process.poll()
                return rc
            except OSError as e:
                #print("OSError > ",e.errno)
                print "OSError > ", e.strerror
                #print("OSError > ",e.filename)
                print(
                    Fore.RED + "Note: Default Shell mode, please check you input" + Fore.RESET)
            except ValueError:
                pass
            except:
                print("Error > ", sys.exc_info()[0])

        if input == 'x' or input == 'q':
            return self.do_exit(input)
        else:
            #"Run a shell command"
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
    #cli.misc_header = '123'
    cli.undoc_header = Fore.LIGHTYELLOW_EX + \
        'Sub Modules \n==========================='+Fore.RESET
    cli.ruler = ''
    cli.cmdloop()
