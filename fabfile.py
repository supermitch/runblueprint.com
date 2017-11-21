from fabric.api import *

def host_type():
        run('uname -s')

env.use_ssh_config = True
env.user = 'runblueprint'
env.hosts = ['runblueprint@bookstore.dreamhost.com', 'mitch@localhost']
