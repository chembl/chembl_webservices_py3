import os
import sys
SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, os.pardir))
APP_PATH = os.path.join(SCRIPT_DIR, 'src')
sys.path.append(APP_PATH)


bind="0.0.0.0:8000"
workers=8
worker_class="sync"
graceful_timeout=600
timeout=600
loglevel="critical"
daemon=False
accesslog="./gunicorn/_access.log"
errorlog="./gunicorn/error.log"
proc_name="chembl_ws_py3"
pid="./gunicorn/run.pid"