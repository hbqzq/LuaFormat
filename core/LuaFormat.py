# -*- coding:utf-8 -*-
import subprocess
import os 
import sublime

def _lua_format(lines, settings):
    input = '\n'.join(lines)

    lfmt = os.path.join(sublime.packages_path(), "LuaFormat/tools/luafmt.exe")
    encoding = 'utf-8'
    args = []

    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        encoding = 'gbk'
        args.append(lfmt)
    elif os.name == 'posix':
        encoding = 'utf-8'
        args.append('mono')
        args.append(lfmt)

    if settings.get('use_tabs'):
        args.append('--use-tabs')

    args.append('--indent-count')
    if settings.get('indent_count'):
        args.append(str(settings.get('indent_count')))
    else:
        args.append(settings.get('use_tabs'))

    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
    out, err = p.communicate(input=bytes(input, encoding))

    err = err.decode(encoding)
    if err != None and err != '': 
        raise Exception('error: ' + err)
        
    return out.decode(encoding)

# return a string
def lua_format(lines, settings):
    return _lua_format(lines, settings)


# return a list of string for CudeText.
# def lua_format_by_cudatext(content,
#                            tab_size=4,
#                            separator_exclude=True,
#                            operator_exclude=True,
#                            bracket_exclude=False):
#     settings = {}
#     settings['tab_size'] = tab_size
#     # settings['special_symbol_split'] = separator_exclude
#     # settings['bracket_split'] = bracket_exclude

#     _lua_format(content, settings)

#     r = []
#     for line in _lines:
#         r.append[line]
#     return r
