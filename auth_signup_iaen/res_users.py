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
from datetime import datetime, timedelta
import random
from urllib import urlencode
from urlparse import urljoin

from openerp.osv import osv, fields
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from ast import literal_eval
from openerp.tools.translate import _

class SignupError(Exception):
    pass

def now(**kwargs):
    dt = datetime.now() + timedelta(**kwargs)
    return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

class res_users(osv.Model):
    _inherit = 'res.users'

    def action_send_mail(self, cr, uid, login, token, context=None):
        #res_users_obj = self.pool.get('res.users').search(cr, uid, [('login','=',login['login'])])
        res_partner_ids = self.pool.get('res.partner').search(cr,uid,[('email','=',login['email'])])
        print res_partner_ids 
        if res_partner_ids:
            res_users_obj = self.pool.get('res.users').search(cr, uid, [('partner_id','=',res_partner_ids[0])])
            print res_users_obj
        res_partner = self.pool.get('res.partner')
        partner_ids = [user.partner_id.id for user in self.browse(cr, uid, res_users_obj, context)]
        res_partner.signup_prepare(cr, uid, partner_ids, signup_type="signup", expiration=now(days=+1), context=context)
        ids = res_users_obj
        print ids
        if not context:
            context = {}

        # send email to users with their signup url
        self.write(cr,uid,ids,{
            'active':False
        })
        template = False
        template = self.pool.get('ir.model.data').get_object(cr, uid, 'auth_signup_iaen', 'set_password_email_iaen')
        mail_obj = self.pool.get('mail.mail')
        assert template._name == 'email.template'
        for user in self.browse(cr, uid, ids, context):
            if not user.email:
                raise osv.except_osv(_("No se puede enviar el correo, la cuenta de usuario y/o cotraseña no es correcta."), user.name)
            print template
            mail_id = self.pool.get('email.template').send_mail(cr, uid, template.id, user.id, True, context=context)
            mail_state = mail_obj.read(cr, uid, mail_id, ['state'], context=context)
            if mail_state and mail_state['state'] == 'exception':
                raise osv.except_osv(_("Cannot send email: no outgoing email server configured.\nYou can configure it under Settings/General Settings."), user.name)
            else:
                return True


    def active_user(self, cr, uid, token, context=None):
        partner_id = self.pool.get('res.partner').search(cr, uid, [('signup_token', '=', token)])
        if partner_id:
            #partner_obj = self.pool.get('res.partner').browse(cr, uid, partner_id)
            print partner_id[0]
            user_id = self.search(cr, uid, [('partner_id.id', 'in', partner_id),('active','=',False)])
            self.pool.get('res.partner').write(cr,uid,partner_id, {'user_id': user_id[0]})
            if user_id:
                self.write(cr, uid, user_id, {'active': True})
                return True
            else:
                return False
