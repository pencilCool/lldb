import lldb

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f BreakAfterRegex.breakAfterRegex bar')

def breakAfterRegex(debugger, command, result, internal_dict):
  '''breakAfterRegx
  '''
  target = debugger.GetSelectedTarget()
  breakpoint = target.BreakpointCreateByRegex(command)
  
  if not breakpoint.IsValid() or breakpoint.num_locations == 0:
    result.AppendWarning(
      "Breakpoint isn't valid or hasn't found any hits")
  else:
    result.AppendMessage("{}".format(breakpoint))

  breakpoint.SetScriptCallbackFunction("BreakAfterRegex.breakpointHandler") 

def breakpointHandler(frame, bp_loc, dict):
  '''The function called when the regular
  expression breakpoint gets triggered
  '''
  thread = frame.GetThread()
  process = thread.GetProcess()
  debugger = process.GetTarget().GetDebugger()

  function_name = frame.GetFunctionName()
  debugger.SetAsync(False)
  thread.StepOut()
  output = evaluateReturnedObject(debugger,thread,function_name)
  if output is not None:
    print(output)

def evaluateReturnedObject(debugger, thread, function_name):
  '''Grabs the reference from the return register
  and returns a string from the evaluated value.
  TODO ObjC only
'''
#1
  res = lldb.SBCommandReturnObject()
#2
  interpreter = debugger.GetCommandInterpreter()
  target = debugger.GetSelectedTarget()
  frame = thread.GetSelectedFrame()
  parent_function_name = frame.GetFunctionName()
#3
  expression = 'expression -lobjc -O -- {}'.format(getRegisterString(target))
#4
  interpreter.HandleCommand(expression, res)
#5
  if res.HasResult(): #6
    output = '{}\nbreakpoint: '\
      '{}\nobject: {}\nstopped: {}'.format(
        '*' * 80,
        function_name,
        res.GetOutput().replace('\n', ''),
        parent_function_name)
    return output
  else:
    #7
    return None

def getRegisterString(target):
  triple_name = target.GetTriple()
  if "x86_64" in triple_name:
    return "$rax"
  elif "i386" in triple_name:
    return "$eax"
  elif "arm64" in triple_name:
    return "$x0"
  elif "arm" in triple_name:
    return "$r0"
  raise Exception('Unknown hardware. Womp womp')
