# -*- coding: utf-8 -*-
import endpoints

import api.service

api = endpoints.api_server([api.service.UsersApi])
