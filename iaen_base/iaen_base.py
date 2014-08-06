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
from validation import validation

class identification_type(osv.osv):
    _name = "identification.type"
    _description = u'Identificacion con pasaporte o Cédula de ciudadania'
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

#CLASE PARA TIPO DE SEXO
class type_sex(osv.osv):    
    _name="type.sex"
    _description="Tipos de sexo"
    _order = "name"        
    _columns={
            "name" : fields.char("Nombre",size=15,required=True),
            "code_mrl" : fields.char("Código MRL",size=3, required=True),
    }
    _defaults = {
        "code_mrl":"NONE",
        }
    _order = "name"
    _sql_constraints = [('name_uniq', 'unique(name)', _(u'Ya existe un genero con el mismo nombre'))]

            
class zones(osv.osv):
    """
    CRUD con la división política por zonas para el Ecuador
    name: 
    description:
    country_id:
    """
    _name = "zones"
    _description = "Categoriza zonas por provincias"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', 'Ya existe una zona con el mismo nombre')]
    _columns = {
        "name": fields.char("Zona",size=35, required=True),
        "description": fields.text("Descripción",help="Descripción para la zona."),
        "country_id": fields.many2one("res.country","Pais",required=True),
        }

class res_country(osv.osv):
    """
    Herencia para la creación del CRUD para paices, heredado desde la tabla res_country
    code_mrl:
    """
    _inherit = "res.country"
    _columns = {
        "code_mrl": fields.integer("Código MRL"),
    }

class res_country_state(osv.osv):
    """
    Herencia para la creación del CRUD para los estados o provincias, heredado desde la tabla res_country_state
    code_mrl:
    zone_id:
    """
    _inherit = "res.country.state"
    _columns = {
        "code_mrl": fields.integer("Código MRL"),
        "zone_id": fields.many2one("zones","Zona",help="Distribución zonal, a la que pertenece la provincia")
    }

    def change_zone_id(self,cr,uid,ids,zone):
        """
        Función para la selección automática del pais, segú la zona seleccionada
        """
        if zone:
            zone_obj = self.pool.get('zones').browse(cr,uid,zone)
            print zone_obj
            country_obj = self.pool.get('res.country').browse(cr,uid,zone_obj.country_id.id)
            print country_obj.id
            #self.write(cr,uid,ids,{'country_id':country_obj[0]})
            return {'value': {'country_id':country_obj.id}}
        else:
            return False
        
class canton(osv.osv):
    """
    CRUD para la generación e ingreso de los cantones y/o ciudades de una provincia
    name:
    code_mrl:
    country_state_id:
    """
    _name = "canton"
    _description = "Cantones/ciudades de una provincia"
    _order = "name"
    _columns = {
        "name": fields.char("Ciudad/Cantón", size=15, required=True),
        "code_mrl": fields.integer("Código MRL"),
        "country_state_id": fields.many2one("res.country.state","Provincia",required=True),
    }


class parish(osv.osv):
    """
    CRUD para la generación de parroquieas que pertenecen a un cantón
    name:
    code_mrl:
    canton_id:
    description:
    """
    _name = "parish"
    _description = u'Parroquias que pertenecen a un cantón'
    _order = "name"
    _columns = {
        "name": fields.char("Parroquia", size=15, required=True),
        "code_mrl": fields.integer("Código MRL"),
        "canton_id": fields.many2one("canton","Cantón",required=True),
        "description": fields.text("Descripción"),
    }


class blood_type(osv.osv, validation):
	""" Clase para los Tipos de Sangre """ 
	_name = "blood.type"
	_description = "Registra los tipos de sangre"
	_columns = {
		'name': fields.char("Nombre", size=3, required=True),
		'code_mrl': fields.char('Código MRL', size=3)
	}
	_order = "name"
	_sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un Tipo de Sangre con ese nombre.')),
			('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese Código Mrl'))]
	_constraints = [(validation.no_numbers, _(u"El Tipo de Sangre no debe contener números."), ['name'])]


class civil_status(osv.osv):
    _name = "civil.status"
    _description = "Informacion sobre estado civil"
    _order = "name"
    _sql_constraints = [
            ('name_uniq', 'unique(name)', 'Ya existe un Estado Civil con el mismo nombre'),
            ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
            ]
    _columns = {
        'code_mrl' : fields.integer("Codigo MRL", size=3),
        'name' : fields.char("Nombre", size=50, required=True),
    }


#PARENTESCO FAMILIAR
class family_relationship(osv.osv):    
    _name = "family.relationship"
    _description = "Parentesco Familiar"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=20, required=True),
            "description": fields.text("Descripcion"),
            "code_mrl": fields.char("Código MRL", size=3),
    }
    _defaults = {
        "code_mrl":"NONE",
        }

    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if  re.search("[^a-z, A-Z]", bloody_type.name): return False
        return True 

#    _constraints = [(_alphabetical, _(u"El Tipo de dato es invalido."), ['name'])]


class nationality(osv.osv, validation):
	""" Clase para las Nacionalidades """
	_name = "nationality"
	_description = "Registra las nacionalidades"
	_columns = {
		'name': fields.char("Nombre", size=45, required=True),
		'code_mrl': fields.char("Código MRL", size=3, required=False)
	}
	_order = "name"
	_sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe una Nacionalidad con ese nombre.')),
			('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese Código Mrl'))]
	_constraints = [(validation.only_letters, _(u"La Nacionalidad debe contener letras únicamente"), ['name'])]

class instruction(osv.osv):
	#"""Clase para las Instrucciones"""
    _name = "instruction"
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Ya existe un Registro con el mismo nombre'),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _description = "Registra las instrucciones"
    _columns = {
        'code_mrl': fields.integer("Código MRL"),
        'name': fields.char("Nombre", size=200, required=True),
        'description': fields.text("Descripción"),

    }
    _order = "name"
	
class entity_finance(osv.osv):
    """Clase de los diferentes entidades financieras existentes en Ecuador"""
    _name="entity.finance"
    _description="Entidad Financiera"
    _order="name"
    _sql_constraints = [
            ('name_unique', 'unique(name)', _(u'Ya existe una Entidad Financiera con ese nombre.')),
            ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
        ]
    _columns={
            "code_mrl" : fields.integer("Codigo MRL", size=3),
            "name" : fields.char("Nombre",size=50,required=True),
    }

class bank_account_type(osv.osv):
    """Clase de los tipos de cuentas bancarias"""
    _name="bank.account.type"
    _description="Tipo de Cuenta"
    _order="name"
    _sql_constraints = [
            ('name_unique', 'unique(name)', _(u'Ya existe un tipo de cuenta bancaria con ese nombre.')),
            ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
        ]
    _columns={
             "code_mrl" : fields.integer("Codigo MRL", size=3),
            "name" : fields.char("Nombre",size=50,required=True),
    }

#TIPO DE DISCAPACIDAD
class type_disability(osv.osv, validation):    
    _name = "type.disability"
    _description = "Tipo de Discapacidad"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un tipo de discapacidad con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=30, required=True),
            "description": fields.text("Descripcion"),
            "code_mrl": fields.char("Código MRL", size=3),
    }
    _constraints = [(validation.only_letters, _(u"El Tipo de dato es inválido."), ['code_mrl'])]


#TIPO DE EVENTO
class event_type(osv.osv, validation):    
    _name = "event.type"
    _description = "Tipo de Evento "       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=20, required=True),
            "description": fields.text("Descripcion"),
            "code_mrl": fields.char("Código MRL", size=3),
    }
    _defaults = {
        "code_mrl":"NONE",
        }

"""    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if  re.search("[^a-z, A-Z]", bloody_type.name): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es inválido."), ['name'])]"""

 

class certified_type(osv.osv):    
    _name = "certified.type"
    _description = "Tipo de Certificado"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=40, required=True),
            "description": fields.text("Descripcion"),
            "code_mrl": fields.char("Código MRL", size=3),
    }
    _defaults = {
        "code_mrl":"NONE",
        }

"""    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if  re.search("[^a-z, A-Z]", bloody_type.name): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es invalido."), ['name'])]"""


class hr_job(osv.osv): 
    """Clase heredada del modulo de recursos humanos para la creacion de puestos de trabajo"""   
    _inherit = "hr.job"
    _sql_constraints = [('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))]
    _columns={
           "code_mrl": fields.integer("Código MRL"),
    }

#CLASE PARA IDIOMAS
class language_type(osv.osv):    
    _name="language.type"
    _description="Tipos de lenguajes"
    _order = "name"        
    _sql_constraints = [('name_uniq', 'unique(name)', _(u'Ya existe un campo con el mismo nombre'))]
    _columns={
        "cod_language" : fields.char("Detalle", size=25, required=True),
        "name" : fields.char("Nombre",size=30,required=True),        
    }


class input_motive(osv.osv):    
    _name="input.motive"
    _description="Motivos de Entrada Laboral"
    _order = "name"        
    _sql_constraints = [
        ('name_uniq', 'unique(name)', _(u'Ya existe un registro con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))]
    _columns={
        "code_mrl": fields.integer("Codigo MRL"),
        "name" : fields.char("Nombre",size=100,required=True), 
        "description": fields.text("Descripción")       
    }

class output_motive(osv.osv):    
    _name="output.motive"
    _description="Motivos de Salida Laboral"
    _order = "name"        
    _sql_constraints = [
        ('name_uniq', 'unique(name)', _(u'Ya existe un registro con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))]
    _columns={
        "code_mrl": fields.integer("Codigo MRL"),
        "name" : fields.char("Nombre",size=100,required=True), 
        "description": fields.text("Descripción")       
    }

class entity_type(osv.osv):
    _name="entity.type"
    _description="Tipos de Entidades"
    _order = "name"        
    _sql_constraints = [
        ('name_uniq', 'unique(name)', _(u'Ya existe un registro con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))]
    _columns={
        "code_mrl": fields.integer("Código MRL"),
        "name" : fields.char("Nombre",size=100,required=True), 
        "description": fields.text("Descripción")       
    }

#CLASE: NOTARIAS
class name_notary(osv.osv):    
    _name = "name.notary"
    _description = "Notarias del Ecuador"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un campo con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=30, required=True),
            "code_mrl": fields.char("Código MRL", size=3),
    }
    _defaults = {
        "code_mrl":"NONE",
        }

    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if not (re.search("[a-z, A-Z]", bloody_type.name)): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es inválido."), ['name'])]

#CLASE: Nacionalidad Indigena
class indian_nationality(osv.osv):    
    _name = "indian.nationality"
    _description = "Nacionalidad indigena"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un campo con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=30, required=True),
            "code_mrl": fields.char("Código MRL", size=3),
    }
    _defaults = {
        "code_mrl":"NONE",
        }

    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if not (re.search("[a-z, A-Z]", bloody_type.name)): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es inválido."), ['name'])]
