# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import openerp;
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
import openerp.addons.decimal_precision as dp
import openerp.tools.image as imageoerp
import re


class identification_type(osv.osv):
    _name = "identification.type"
    _description = "Identificacion con pasaporte o Cedula de ciudadania"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un tipo de identificación con el mismo nombre'))]
    _columns = {
        "name": fields.char("Nombre", size=100, required=True),
        "description": fields.text("Descripción"),
    }


class ethnic_group(osv.osv):
    _name = "ethnic.group"
    _description = "Almacena los gripos etnicos"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un grupo étnico con el mismo nombre'))]
    _columns = {
        "name": fields.char("Nombre", size=100, required=True),
        "description": fields.text("Descripción"),
    }



class zones(osv.osv):
    _name = "zones"
    _description = "Categoriza zonas por provincias"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', 'Ya existe una zona con el mismo nombre')]
    _columns = {
        "name": fields.char("Zona",size=10, required=True),
        "description": fields.text("Descripción",help="Descripción para la zona."),
        "country_id": fields.many2one("res.country","Pais",required=True),
        }

class res_country_state(osv.osv):
    _inherit = "res.country.state"
    _columns = {
        "zone_id": fields.many2one("zones","Zona",help="Distribución zonal, a la que pertenece la provincia")
    }
    def change_zone_id(self,cr,uid,ids,zone):
        if zone:
            zone_obj = self.pool.get('zones').browse(cr,uid,zone)
            print zone_obj
            country_obj = self.pool.get('res.country').browse(cr,uid,zone_obj.country_id.id)
            print country_obj.id
            #self.write(cr,uid,ids,{'country_id':country_obj[0]})
            return {'value': {'country_id':country_obj.id}}
        else:
            return False
        
#    _order = "name"
#    _sql_constraints = [('name_unique', 'unique(name)', 'Ya existe una zona con el mismo nombre')]

class canton(osv.osv):
    _name = "canton"
    _description = "Cantones/ciudades de una provincia"
    _order = "name"
    _columns = {
        "name": fields.char("Ciudad/Cantón", size=15, required=True),
        "country_id": fields.many2one("res.country.state","Provincia",required=True),
        "description": fields.text("Descripción"),
    }

#class city(osv.osv):
#    _name = "city"
#    _description = "Ciudades a las cuales pertenece cada parroquia"
#    _order = "name"
#    _columns = {
#        "name": fields.char("Ciudad", size=15,required=True),
#        "description": fields.text("Descripción",),
#    }

class parish(osv.osv):
    _name = "parish"
    _description = u'Parroquias que pertenecen a un cantón'
    _order = "name"
    _columns = {
        "name": fields.char("Parroquia", size=15, required=True),
        "canton_id": fields.many2one("canton","Cantón",required=True),
        "description": fields.text("Descripción"),
    }


class blood_type(osv.osv):
	_name = "blood_type"
	_description = "Registra los tipos de sangre"
	_columns = {
		'name': fields.char("Nombre", size=3, required=True),
	}
	_order = "name"
	_sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un Tipo de Sangre con ese nombre.'))]
	def _no_numbers(self, cr, uid, ids):
		for bloody_type in self.browse(cr, uid, ids):
			if re.search("[0-9]", bloody_type.name): return False
		return True 
	_constraints = [(_no_numbers, _(u"El Tipo de Sangre no debe contener números."), ['name'])]

