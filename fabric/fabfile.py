
from fabric.api import local,put,run ,env
from fabric.api import cd
env.hosts=['120.24.239.32:22','120.24.239.32:22']
env.passwords={'root@12'}


def test():
    local('mkdir -p /tmp/xixi')
    put('/etc/passwd','/tmp/')
    run('ls /tmp')
    with cd('/tmp/xixi'):
        run('touch hujingggggg')
        run('pwd')
        
        local('pwd')
        run('w')
    run('pwd')

    

