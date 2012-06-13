from fabric.api import *
from fabric.contrib.console import confirm

# This fabfile is compatible with Ubuntu Server Edition.

env.roledefs = {
    'prod': ['demo']
}
env.use_ssh_config = True
env.user = 'ubuntu'
env.key_filename = '.keys/demo.pem'
env.password = ''

DEPLOY_BASE = '/var/www'
DEPLOY_PATH = DEPLOY_BASE + '/deploy'
REPO_NAME = 'DealAPI'
REPO_URL = 'https://github.com/zdexter/{0}.git'.format(REPO_NAME)

def test():
    with settings(warn_only=True):
        test_result = local('nosetests')
    if test_result.failed and not confirm("Nosetest indicated failed tests.  Proceed anyways?"):
        abort("Aborting")

def setup_server():
    """
    Every command here should be roughly idempotent.
    """
    # The -p option to mkdir creates parent directories if they don't exist
    sudo('test -d {0} || mkdir -p {0}'.format(DEPLOY_PATH))
    # TODO:  Make the directory owned by a low-permission user other than the login user
    sudo('chown {0}:{0} {1}'.format(env.user, DEPLOY_PATH))
    # We aren't there to answer any prompts, so say yes to them.
    sudo('apt-get install python-virtualenv git -y')
    run('cd {0} && test -d {0}/{2} || git clone {1} {2}'.format(DEPLOY_PATH, REPO_URL, REPO_NAME))
    # Pull and install submodules
    run('cd {0}/{1} && git pull && git submodule update --init'.format(DEPLOY_PATH, REPO_NAME))
    run('test -d venv || virtualenv --distribute venv')
    run('source venv/bin/activate')
    run('pip install -r requirements.txt')
    
def deploy():
    run('cd %s && git pull' % DEPLOY_PATH)
    env.hosts += ['']
    