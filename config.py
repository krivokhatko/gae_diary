# -*- coding: utf-8 -*-
import os
import db.model

PRODUCTION = os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Eng')
DEBUG = not PRODUCTION
DEVELOPMENT = not PRODUCTION

CFG_DB = db.model.Config.get_primary_db()
