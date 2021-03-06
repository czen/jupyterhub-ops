import os
from dockerspawner import DockerSpawner

class DemoFormSpawner(DockerSpawner):
    def _options_form_default(self):
        default_stack = "jupyter/minimal-notebook"
        return """
        <label for="stack">Select your desired stack</label>
        <select name="stack" size="1">
        <option value="jupyter/scipy-notebook">Default Scipy notebook </option>
        <option value="czen/ops-cling-notebook:0.2">Scipy notebook with cling and OPS </option>
        <option value="www2.opsgroup.ru/ops-notebook:0.3"> Better scipy notebook with cling and OPS </option>
        <option value="jupyter/datascience-notebook">Datascience notebook </option>
        </select>
        """.format(stack=default_stack)

    def options_from_form(self, formdata):
        options = {}
        options['stack'] = formdata['stack']
        container_image = ''.join(formdata['stack'])
        print("SPAWN: " + container_image + " IMAGE" )
        self.container_image = container_image
        return options

c.JupyterHub.template_paths = ['/templates']

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

## Authenticator
#from jhub_cas_authenticator.cas_auth import CASAuthenticator
#c.JupyterHub.authenticator_class = CASAuthenticator
## Configure authentication (delagated to GitLab)
from oauthenticator.gitlab import GitLabOAuthenticator
c.JupyterHub.authenticator_class = GitLabOAuthenticator
c.Authenticator.admin_users=['czen']

# The CAS URLs to redirect (un)authenticated users to.
#c.CASAuthenticator.cas_login_url = 'https://cas.uvsq.fr/login'
#c.CASLocalAuthenticator.cas_logout_url = 'https://cas.uvsq/logout'

# The CAS endpoint for validating service tickets.
#c.CASAuthenticator.cas_service_validate_url = 'https://cas.uvsq.fr/serviceValidate'

# The service URL the CAS server will redirect the browser back to on successful authentication.
#c.CASAuthenticator.cas_service_url = 'https://%s/hub/login' % os.environ['HOST']

#c.Authenticator.admin_users = { 'lucadefe' }


## Docker spawner
#c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.spawner_class = DemoFormSpawner
#c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
jupyter_workdir = '/home/jovyan'
ops_notebook_dir = os.environ.get('DOCKER_DATA_DIR') or '/home/jovyan/data'
c.DockerSpawner.notebook_dir = jupyter_workdir
c.DockerSpawner.volumes = { 
    'jupyterhub-user-{username}': notebook_dir,
    '/media/vivado-user/extra/ops_notebooks': ops_notebook_dir
    }

# Other stuff
c.Spawner.cpu_limit = 2
c.Spawner.mem_limit = '10G'


## Services
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
]
