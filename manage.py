import os
import sys
SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, os.pardir))
APP_PATH = os.path.join(SCRIPT_DIR, 'src')
sys.path.append(APP_PATH)

import chembl_ws_app.manage as inner_manage
inner_manage.main()