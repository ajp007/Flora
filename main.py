import discord
from discord.ext import commands
import json
import arrow
import logging
from os import mkdir, chdir, listdir
from os.path import join, exists
import ConfigUpdater as CU
import checks
checks = checks
CU = CU
def y_or_n(question: str):
    """Yes/No Prompt"""
    while True:
        x = input('{}\nY\\N: '.format(question.strip())).lower()
        if x in ['yes','y']:
            return True
        if x in ['no', 'n']:
            return False


def config_setup():
    "config Setup"
    return {'token': input('Token: '), 'prefix': input('Prefix: '), 'owner_id': input('Owner ID: ')}


def get_config() -> dict:
    if not exists('config'):
        mkdir('config')
    try:
        config = json.load(open(join('config','config.json')))
        test = [config['token'], config['owner_id'], config['prefix']]
        del test
        return config
    except Exception:
        print('Config Was Corrupted/Doesnt Exist')
        print('Creating Config....')
        while True:
            config = config_setup()
            if y_or_n('Token: {}\nPrefix: {}\nOwner ID: {}'
                              .format(config['token'], config['prefix'], config['owner_id'])):
                with open(join('config', 'config.json')) as f:
                    json.dump(config, f, indent=4, sort_keys=True)
                return config


config = get_config()
description = 'Flora Bot\nMade by Fuzen.py who cant speel\nhttps://github.com/Fuzen-py/Flora\n'
help_attrs = dict(hidden=True)
flora = commands.Bot(command_prefix=config['prefix'], description=description, pm_help=True, help_attrs=help_attrs)
divider = '--------------------------------------\n'
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.WARN)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='flora.log', encoding='utf-8', mode='a')
log.addHandler(handler)


def get_plugins() -> list:
    plugins_list = []
    li = listdir('Plugins')
    li.remove('__init__.py')
    for l in li:
        try:
            for l2 in listdir(join('Plugins', l)):
                if l2.endswith('.py') and l2 != '__init__.py':
                    plugins_list += ['.'.join(['Plugins',l,l2[:-3]])]
                    break
        except Exception:
            pass
    return plugins_list


@flora.event
async def on_ready():
    print('Running as:', flora.user.name)
    print('Prefix:', flora.command_prefix)
    print('Started at:',flora.uptime)
    print('Plugins Loaded:', flora.loaded_plugins)
class Core:
    def __init__(self, flora):
        self.flora = flora
    @commands.group(pass_context=True)
    @checks.is_owner()
    async def plugin(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.flora.say('Invalid criteria passed "{0.subcommand_passed}"'.format(ctx))
    @plugin.command()
    async def load(self, plugin_name):
        try:
            self.flora.load_extension(plugin_name)
            self.flora.loaded_plugins += 1
            await self.flora.say(':ok_hand:')
        except:
            await self.flora.say('Failed to load {}'.format(plugin_name))
    @plugin.command()
    async def unload(self, plugin_name):
        try:
            self.flora.unload_extention(plugin_name)
            self.flora.loaded_plugins -= 1
            await self.flora.say(':ok_hand:')
        except:
            await self.flora.say('Failed to unload {}'.format(plugin_name))
    @plugin.command()
    async def reload(self, plugin_name):
        unloaded = False
        try:
            self.flora.unload_extension(plugin_name)
            unloaded = True
            self.flora.load_extension(plugin_name)
            await self.flora.say(':ok_hand:')
        except:
            if unloaded:
                self.flora.loaded_plugins -= 1
                await self.flora.say('Failed To Reload plugin, plugin has been unloaded')
            else:
                await self.flora.say('Was the plugin Ever loaded?')
    @plugin.command()
    async def list_plugins(self):
        await self.flora.whisper(get_plugins())

if __name__ == '__main__':
    plugins = get_plugins()
    flora.command_counter = 0
    flora.in_queue = 0
    flora.message_processed = 0
    flora.loaded_plugins = 0
    flora.add_cog(Core(flora))
    print(get_plugins())
    for extension in get_plugins():
        print(extension)
        try:
            flora.load_extension(extension)
            flora.loaded_plugins += 1
        except:
            print('Failed to load', extension)
    flora.uptime = arrow.utcnow()
    flora.run(config['token'])
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
