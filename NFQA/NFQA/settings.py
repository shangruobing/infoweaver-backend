import os
import datetime
from pathlib import Path

# Import the public settings
from conf.base_settings import *

# Import the configuration file by setting the running mode
is_development_mode = True

ENABLE_BERT = False
ENABLE_NEO4J = False
ENABLE_REDIS = False

DEBUG = True

if is_development_mode:
    from conf.dev_settings import *
else:
    from conf.prod_settings import *
