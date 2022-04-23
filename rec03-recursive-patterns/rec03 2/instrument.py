from functools import wraps
import sys

def show_recursive_structure(f):
    """Show call entry/exits on stderr

    Wrapper to instrument a function to show the
    call entry and exit from that function. Can
    customize view with instrument flags.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        arg_str = ', '.join(str(a) for a in args)
        if show_recursive_structure.TRIM_ARGS is not None and len(arg_str) > show_recursive_structure.TRIM_ARGS:
            arg_str = arg_str[:show_recursive_structure.TRIM_ARGS] + " ..."
        if show_recursive_structure.SHOW_CALL:
            sys.stderr.write("   "*wrapper._depth + "call to " + f.__name__ + ": " + arg_str + "\n")
        wrapper._count += 1
        wrapper._depth += 1
        wrapper._max_depth = max(wrapper._depth, wrapper._max_depth)
        result = f(*args, **kwargs)
        wrapper._depth -= 1
        res_str = str(result)
        if show_recursive_structure.TRIM_RET is not None and len(res_str) > show_recursive_structure.TRIM_RET:
            res_str = res_str[:show_recursive_structure.TRIM_RET] + " ..."
        if show_recursive_structure.SHOW_RET:
            sys.stderr.write("   "*wrapper._depth + f.__name__ + " returns: " +  res_str + "\n")
        return result
    wrapper._count = 0
    wrapper._depth = 0
    wrapper._max_depth = 0
    return wrapper

show_recursive_structure.SHOW_CALL = True
show_recursive_structure.SHOW_RET = True
show_recursive_structure.TRIM_ARGS = 55  #None if no trimming
show_recursive_structure.TRIM_RET = 60   #None if no trimming
