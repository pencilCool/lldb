

import lldb
import os
import shlex
import optparse

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand(
    'command script add -f lookup.handle_command lookup')

def handle_command(debugger, command, result, internal_dict):
    '''
    Documentation for how to use lookup goes here 
    '''

    command_args = shlex.split(command, posix=False)
    parser = generateOptionParser()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        result.SetError(parser.usage)
        return

    clean_command = shlex.split(args[0])[0]
    target = debugger.GetSelectedTarget()
    contextlist = target.FindGlobalFunctions(clean_command, 0, lldb.eMatchTypeRegex)
    output = ''
    for context in contextlist:
        output += context.symbol.name + '\n\n'
    result.AppendMessage(output)

def generateOptionParser():
    usage = "usage: %prog [options] TODO Description Here :]"
    parser = optparse.OptionParser(usage=usage, prog="lookup")
    parser.add_option("-m", "--module",
                      action="store",
                      default=None,
                      dest="module",
                      help="This is a placeholder option to show you how to use options with strings")
    parser.add_option("-c", "--check_if_true",
                      action="store_true",
                      default=False,
                      dest="store_true",
                      help="This is a placeholder option to show you how to use options with bools")
    return parser
    