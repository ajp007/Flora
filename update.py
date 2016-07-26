from os.path import dirname, realpath
from os import chdir, popen
import asyncio
from sys import platform
import plugin_install as pl
root = dirname(realpath(__file__))
chdir(root)
print(root)

@asyncio.coroutine
def update():
    print('Updating Base')
    create = asyncio.create_subprocess_shell('git pull', stdout=asyncio.subprocess.PIPE, cwd=root)
    proc = yield from create
    yield from proc.wait()
    print('Updating Plugins')
    yield from pl.installer()
if platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
loop.run_until_complete(update())
print('Done')
