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


import openerp
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

#CLASE DE IDENTIDAD DE GENERO
class gender(osv.osv):    
    _name="gender"
    _description="Tipos de identidad de genero"
    _order = "name"        
    _columns={
            "name" : fields.char("Nombre",size=10,required=True),
            "description" : fields.text("Detalle"),
    }
    _order = "name"
    _sql_constraints = [('name_uniq', 'unique(name)', _(u'Ya existe un genero con el mismo nombre'))]
    def _no_numbers(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if not (re.search("[a-z, A-Z]", bloody_type.name)): return False
        return True 
    _constraints = [(_no_numbers, _(u"El Tipo de dato es invalido."), ['name'])]
   
            
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
	_name = "blood.type"
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

class estado_civil(osv.osv):
    _name = "estado_civil"
    _description = "Informacion sobre estado civil"
    _order = "name"
    _sql_constraints = [('name_uniq', 'unique(name)', 'Ya existe un Estado Civil con el mismo nombre')]
    _columns = {
        'name' : fields.char("Nombre", size=50, required=True),
    }


#CLASE FAMILIAR
class gender(osv.osv):    
    _name="family_burden"
    _description="Carga familiar"
    _order = "name"        
    _columns={
		"name" : fields.char("Nombre",size=10,required=True),
		"description" : fields.text("Descripcion"),
    }
    _order = "name"
    _sql_constraints = [('name_uniq', 'unique(name)', _(u'Ya existe un genero con el mismo nombre'))]
    def _no_numbers(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if not (re.search("[a-z, A-Z]", bloody_type.name)): return False
        return True 
    _constraints = [(_no_numbers, _(u"El Tipo de dato es invalido."), ['name'])]

class nationality(osv.osv):
	_name = "nationality"
	_description = "Registra las nacionalidades"
	_columns = {
		'name': fields.char("Nombre", size=45, required=True),
	}
	_order = "name"
	_sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe una Nacionalidad con ese nombre.'))]
	def _only_letters(self, cr, uid, ids):
		for nationality in self.browse(cr, uid, ids):
			if not re.match(u"^[ñA-Za-zÁÉÍÓÚáéíóú\s]+$", nationality.name): return False
		return True 
	_constraints = [(_only_letters, _(u"La Nacionalidad debe contener letras únicamente"), ['name'])]

class instruction(osv.osv):
	_name = "instruction"
	_description = "Registra las instrucciones"
	_columns = {
		'name': fields.char("Nombre", size=200, required=True),
		'description': fields.text("Descripción")
	}
	_order = "name"
	_sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe una Instrucción con ese nombre.'))]
	def _only_letters(self, cr, uid, ids):
		for instruction in self.browse(cr, uid, ids):
			if not re.match(u"^[ñA-Za-zÁÉÍÓÚáéíóú\s]+$", instruction.name): return False
		return True 
	_constraints = [(_only_letters, _(u"La Nacionalidad debe contener letras únicamente"), ['name'])]

class entity_finance(osv.osv):
    """Clase de los diferentes entidades financieras existentes en Ecuador"""
    _name="entity_finance"
    _description="Entidad Financiera"
    _order="name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe una Entidad Financiera con ese nombre.'))]
    _columns={
            "name" : fields.char("Nombre",size=50,required=True),
    }
    def _no_caracter(self, cr, uid, ids):
        for entity_finance in self.browse(cr, uid, ids):
            if (re.search("[^a-z, ^A-Z, ^0-9]", entity_finance.name)): return False
        return True 
    _constraints = [(_no_caracter, _(u"No debe contener caracteres especiales"), ['Nombre'])]

class bankaccount_type(osv.osv):
    """Clase de los tipos de cuentas bancarias"""
    _name="bankaccount_type"
    _description="Tipo de Cuenta"
    _order="name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un tipo de cuenta bancaria con ese nombre.'))]
    _columns={
            "name" : fields.char("Nombre",size=50,required=True),
    }
    def _no_numbers(self, cr, uid, ids):
        for bankaccount_type in self.browse(cr, uid, ids):
            if re.search("[^a-z, A-Z]", bankaccount_type.name): return False
        return True 
    _constraints = [(_no_numbers, _(u"Debe contener solo caracteres alfabéticos."), ['Nombre'])]

class bank_info(osv.osv):
    """Clase de la informacion bancaria de los users"""
    _name="bank_info"
    _description="Informacion bancaria"
    _order="id_entity_finance"
    _sql_constraints = [('name_unique', 'unique(number)', _(u'Ya existe una cuenta con ese numero'))]
    _columns={
            "id_entity_finance": fields.many2one("entity_finance","Entidad Financiera",required=True),
            "id_bankaccount": fields.many2one("bankaccount_type","Tipo de Cuenta",required=True),
            "number" : fields.char("Número",size=15,required=True),
    }
    def _no_char(self, cr, uid, ids):
        for bank_info in self.browse(cr, uid, ids):
            if re.search("[^0-9]", bank_info.number): return False
        return True 
    _constraints = [(_no_char, _(u"Debe contener solo números."), ['Numero'])]
