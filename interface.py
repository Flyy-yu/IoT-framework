from subInterpreter import *

PROMPT = "IOT-CLI"


class Resource_Interface(Cmd):
    prompt = PROMPT + ">>" + Fore.RED + " (Resource)> " + Fore.RESET

    def do_show(self, input):
        # WIP now just implementing basic functioning
        t = PrettyTable(header_style='upper', padding_width=0)
        t.field_names = ["Resource", "Description", "URL"]
        t.align["Resource"] = "c"
        t.align["Description"] = "l"
        t.align["URL"] = "l"

        with open('resources/resources.json') as f:
            tool_info = json.load(f)
            # print tool_info
            for tool in tool_info['Resource'].keys():
                name = textwrap.fill(str(tool), 20)
                description = textwrap.fill(
                    str(tool_info['Resource'][name]['Description']), 50)
                example = textwrap.fill(
                    str(tool_info['Resource'][name]['URL']), 30)
                t.add_row([name, description, example])
                padding = '{s:{c}^{n}}'.format(s='-', n=20, c='-')
                t.add_row([padding, padding, padding])
        print(t)

    def do_use(self, command):
        prompt = PROMPT + ">>" + Fore.RED + \
                 " (tools_lib)>> " + Fore.RESET + \
                 Back.RED + command + " >>>" + Back.RESET
        json_dir = 'tools/{}/config.json'.format(command.lower())

        try:
            class_name = command.lower()[0].upper() + command.lower()[1:] + 'SubInterpreter'
            current_module = importlib.import_module('subInterpreter')
            current_class = getattr(current_module, class_name)
            use_cli = current_class(json_dir)
        except:
            print(
                Fore.YELLOW + "Unknown Tools name, you can type 'show' to know all supported tools." + Fore.RESET)
            return

        use_cli.prompt = prompt
        use_cli.cmdloop()

    def do_back(self, args):
        print("Back to Main CLI...")
        return True


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

        try:
            class_name = command.lower()[0].upper() + command.lower()[1:] + 'SubInterpreter'
            current_module = importlib.import_module('subInterpreter')
            current_class = getattr(current_module, class_name)
            use_cli = current_class(json_dir)
        except:
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
