import os
# from subprocess import Popen, PIPE
from os.path import dirname, realpath, join, exists, split
from os import listdir, mkdir, getcwd, chdir, popen
import asyncio
import sys

"""
Vundle inspired Plugin Installer
"""
@asyncio.coroutine
def any2hard(list: dict, argument: str) -> bool:
    """
    As embarrassing as it is, this is because i failed to get any working
    :param list: list of installed plugins
    :param argument: what to check if its there
    :return: True/False
    """
    argument = split(argument)[-1]
    for x in list:
        if x.endswith(argument):
            return True
    return False


@asyncio.coroutine
def installer(verbose=False):
    """
    An installer based on Vundle
    :param verbose: If this is True it prints out a bunch of debugging stuff
    :return:
    """
    #print('Identifying Plugins...')
    root = dirname(realpath(__file__))
    plugin_dir = join(root, 'Plugins')
    if not exists(plugin_dir):  # Check if Plugin Directory Exists
        mkdir(plugin_dir)  # Make it if not
    current_plugins = listdir(plugin_dir)  # List plugins
    with open(join(root, 'config', 'plugins.flora')) as f:
        plugins = f.readlines()  # Get a list of installed plugins
    use_pull = []  # Plugins to use Pull Command
    plugins_new = []  # Plugins to use Clone command
    for x in plugins:  # Split them into plugins_new and use_pull
        if x.startswith('Plugin'):
            x = x[6:].strip().strip('"\'')  # Removes the "Plugin"
            if verbose:
                print('----------------')
                print(current_plugins)
                print(x)
                print('----------------')
            any = yield from any2hard(current_plugins, x)
            if any:  # Check if plugin is already installed
                use_pull += [x.rsplit(sep='\\', maxsplit=1)[-1]]  # if its installed, it goes here
            else:
                plugins_new += [x]  # otherwise here
    plugins = plugins_new
    del plugins_new
    del f
    if len(plugins) > 0:
        print('Installing New Plugins')
        for plugin in plugins:
            print('Installing', split(plugin)[-1])
            cmd = 'git clone https://github.com/{}.git'.format(plugin)
            if verbose:
                print('Executing', cmd)
            create = asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, cwd =plugin_dir)
            proc = yield from create
            yield from proc.wait()
            print('Installed', split(plugin)[-1])
            if verbose:
                print(proc.stdout.read())
    if len(use_pull) > 0:
        print('Updating old plugins')
        for plugin in use_pull:
            plugin=split(plugin)[-1]
            print('Updating', plugin)
            cmd = 'git pull'
            create = asyncio.create_subprocess_shell(cmd, cwd = join(plugin_dir, plugin))
            proc = yield from create
            yield from proc.wait()
            if verbose:
                print(proc.stdout.read())

if __name__ == '__main__':
        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()
        loop.run_until_complete(installer())
        print('Done')
        exit(0)
