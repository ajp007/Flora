import ConfigUpdater as CU
from os.path import exists, join
from discord.ext import commands
def get_input(input_msg: str, is_list: bool = False, is_number: bool = False):
    if is_list:
        the_list = []
        while True:
            try:
                print('press enter with no text when done')
                list_item = input(input_msg)
                if list_item.strip() == '':
                    return the_list
                if is_number:
                    int(list_item)
                the_list += [list_item.strip()]
            except:
                print('Must be a number')
    else:
        while True:
            try:
                c = input(input_msg)
                if is_number:
                    int(c)
                return c
            except:
                pass

# noinspection PyBroadException
def get_perms(msg) -> dict:
    try:
        c = CU.read_values(msg.server.id, 'per_server')
        if c is None:
            return CU.read_values('permissions', 'config')
    except:
        return CU.read_values('permissions', 'config')



# noinspection PyBroadException
def is_owner_check(msg) -> bool:
    try:
        return msg.author.id == get_perms(msg)['owner id']
    except:
        return False

# noinspection PyBroadException
def is_owner() -> bool:
    return commands.check(lambda ctx: is_owner_check(ctx.message))

# noinspection PyBroadException
def is_allowed_check(msg) -> bool:
    try:
        for role in msg.author.roles:
            if role.name.lower() in get_perms(msg)['allowed roles']:
                return True
        return discord_server_owner_check(msg)
    except:
        return False

# noinspection PyBroadException
def is_allowed() -> bool:
    return commands.check(lambda ctx: is_allowed_check(ctx.message))

# noinspection PyBroadException
def is_home_server_check(msg) -> bool:
    try:
        return msg.server.id in get_perms(msg)['home server']
    except:
        return False

# noinspection PyBroadException
def is_home_server() -> bool:
    return commands.check(lambda ctx: is_home_server_check(ctx.message))

# noinspection PyBroadException
def server_access_check(msg) -> bool:
    try:
        if is_owner_check(msg):
            return True
        return msg.author.id in get_perms(msg)['server access']
    except Exception:
        return False

# noinspection PyBroadException
def server_access() -> bool:
    return commands.check(lambda ctx: server_access_check(ctx.message))

def global_blacklist_check(msg) -> bool:
    try:
        return msg.author.id in get_perms(msg)['global_blacklist']
    except:
        return

def global_blacklist():
    return commands.check(lambda ctx: global_blacklist_check(ctx.message))

def discord_server_owner_check(msg):
    try:
        return msg.author == msg.server.owner
    except:
        return False

def discord_server_owner():
    return commands.check(lambda ctx: discord_server_owner_check(ctx.message))

#try:
c = CU.read_values('permissions', 'config')
if c is None:
    c = {}
try:
    c['owner id']
except:
    c['owner id'] = config['owner_id']
try:
    c['allowed roles']
except:
    c['allowed roles'] = get_input('Leave blank if done or type a name of a role\n>>> ', is_list=True)
try:
    c['home server']
except:
    c['home server'] = get_input('home server id\n>>> ', is_list=True, is_number=True)
try:
    c['server access']
except:
    c['server access'] = get_input('id of user with server access\n>>> ', is_list=True, is_number=True)
try:
    c['global blacklist']
except:
    c['global blacklist'] = []
CU.write_values(c, 'permissions', 'config')
del c
#except Exception as e:
#    print(e)
#    exit('Could not get permissions config')
