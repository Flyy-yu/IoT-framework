import importlib
import os

# "After user select the tool, store the tool name in a variable"
tool_name = 'tftp'

# 'generate the python module filename'
# in this cast, the module name is: tools.ping.ping_usage
tool_module_name = 'tools.{}.{}'.format(tool_name, tool_name + '_usage')

# load the tool module by the module name dynamically
current_module = importlib.import_module(tool_module_name)
# you can call the function inside that module, with the requied argument, in this case, ip address:
# this will give you 'ping 8.8.8.8'
print current_module.get_basic_command('get','/etc/passwd','8.8.8.8')

# we have two file for each tool(right now), one call tool_argument.txt, which has all the argument
# required for the tool, the other file call intro.txt which has the introduction of the tool
# your get the two file using the filepath:
argument_file_path = '{}/tools/{}/tool_argument.txt'.format(os.path.dirname(os.path.abspath(__file__)), tool_name)
intro_file_path = '{}/tools/{}/intro.txt'.format(os.path.dirname(os.path.abspath(__file__)), tool_name)

print argument_file_path
print intro_file_path


# this function will take in the filepath and return an array of all the argument
def get_argument_list(file_path):
    arg_list = []
    try:
        with open(file_path) as argument_file:
            for line in argument_file:
                #remove '\n' in the end
                arg_list.append(line[:-1])
    except IOError:
        print 'Failed to open argument file'
    return arg_list


# this function will return array of introduction content
def get_intro_content(file_path):
    intro_content = []
    try:
        with open(file_path) as argument_file:
            for line in argument_file:
                # remove '\n' in the end
                print line[:-1]
    except IOError:
        print 'Failed to open introduction file'
    return 0


print get_argument_list(argument_file_path)
get_intro_content(intro_file_path)
