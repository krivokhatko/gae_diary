# -*- coding: utf-8 -*-
import endpoints

import api.service
import config

api = endpoints.api_server([api.service.UsersApi], debug=config.DEBUG)
