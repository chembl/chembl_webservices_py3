import os
import sys
import traceback
SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, os.pardir))
APP_PATH = os.path.join(SCRIPT_DIR, 'src')
sys.path.append(APP_PATH)

ENV_FILE_LOADED = int(os.environ.get('CHEMBL_WS_PY3_ENV_LOADED', 0))

ENV_FILE = os.environ.get('CHEMBL_WS_PY3_ENV')
if ENV_FILE and not ENV_FILE_LOADED:
    if os.path.exists(ENV_FILE) and os.path.isfile(ENV_FILE):
        # noinspection PyBroadException
        try:
            with open(ENV_FILE, 'r') as env_file:
                env_lines = env_file.readlines()
                for line in env_lines:
                    line = line.strip()
                    if line[0] != '#':
                        env_setting = line.split('=')
                        if len(env_setting) < 2:
                            print('WARNING ENV VARIABLE LINE IGNORED: {0}'.format(line), file=sys.stderr)
                            continue
                        os.environ.setdefault(env_setting[0], '='.join(env_setting[1:]))
                        print('ENV VARIABLE LOADED: {0} => {1}'.format(env_setting[0], os.environ.get(env_setting[0])))
                os.environ.setdefault('CHEMBL_WS_PY3_ENV_LOADED', '1')
        except:
            print('ENV FILE ERROR - - -'.format(ENV_FILE), file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print('ERROR: Environment file at {0} could not be read.'.format(ENV_FILE), file=sys.stderr)
            print('ENV FILE ERROR - - -'.format(ENV_FILE), file=sys.stderr)
    else:
        print('ENV FILE ERROR - - -'.format(ENV_FILE), file=sys.stderr)
        print('ERROR: Environment file at {0} does not exist or is not a file.'.format(ENV_FILE), file=sys.stderr)
        print('ENV FILE ERROR - - -'.format(ENV_FILE), file=sys.stderr)

import chembl_ws_app.manage as inner_manage
inner_manage.main()