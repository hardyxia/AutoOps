import logging
import os.path
import uuid

from tornado.options import define
from webssh.policy import (
    load_host_keys, get_policy_class, check_policy_setting
)


define('address', default='0.0.0.0', help='listen address')
define('port', default=9999, help='listen port', type=int)
define('debug', default=True, help='debug mode', type=bool)
define('policy', default='warning',
       help='missing host key policy, reject|autoadd|warning')
define('hostFile', default='', help='User defined host keys file')
define('sysHostFile', default='', help='System wide host keys file')


base_dir = os.path.dirname(__file__)


def get_app_settings(options):
    settings = dict(
        template_path=os.path.join(base_dir, 'templates'),
        static_path=os.path.join(base_dir, 'static'),
        #cookie_secret=uuid.uuid4().hex,
        #xsrf_cookies=(not options.debug),
        debug=options.debug
    )
    return settings


def get_host_keys_settings(options):
    if not options.hostFile:
        host_keys_filename = os.path.join(base_dir, 'known_hosts')
    else:
        host_keys_filename = options.hostFile
    host_keys = load_host_keys(host_keys_filename)

    if not options.sysHostFile:
        filename = os.path.expanduser('~/.ssh/known_hosts')
    else:
        filename = options.sysHostFile
    system_host_keys = load_host_keys(filename)

    settings = dict(
        host_keys=host_keys,
        system_host_keys=system_host_keys,
        host_keys_filename=host_keys_filename
    )
    return settings


def get_policy_setting(options, host_keys_settings):
    policy_class = get_policy_class(options.policy)
    logging.info(policy_class.__name__)
    check_policy_setting(policy_class, host_keys_settings)
    return policy_class()
