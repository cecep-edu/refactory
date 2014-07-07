# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
import logging

import openerp
from openerp.modules.registry import RegistryManager
from ..res_users import SignupError

_logger = logging.getLogger(__name__)

class Controller(openerp.addons.web.http.Controller):
    _cp_path = '/auth_iaen'

    @openerp.addons.web.http.jsonrequest
    def signup(self, req, dbname, token, **values):
        """sign up a user (new or existing)"""
        try:
            self._signup_with_values(req, dbname, token, values)
        except SignupError, e:
            return {'error': openerp.tools.exception_to_unicode(e)}
        return {}

    def _signup_with_values(self, req, dbname, token, values):
        registry = RegistryManager.get(dbname)
        with registry.cursor() as cr:
            res_users = registry.get('res.users')
            res_users.signup(cr, openerp.SUPERUSER_ID, values, token)
            res_users.action_send_mail(cr, openerp.SUPERUSER_ID, values, token)


    @openerp.addons.web.http.jsonrequest
    def active_user(self, req, dbname,**values):
        try:
            self._active_user_sys(req, dbname, values['token'])
        except SignupError, e:
            return {'error': openerp.tools.exception_to_unicode(e)}
        return {}
        

    def _active_user_sys(self, req, dbname, token):
        registry = RegistryManager.get(dbname)
        with registry.cursor() as cr:
            res_users = registry.get('res.users')
            if res_users.active_user(cr, openerp.SUPERUSER_ID, token):
                return True
            else:
                return False
            #res_users.action_send_mail(cr, openerp.SUPERUSER_ID, values, token)

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
