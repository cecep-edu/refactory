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
            "name" : fields.char("Nombre",size=15,required=True),
            "description" : fields.text("Detalle"),
    }
    _order = "name"
    _sql_constraints = [('name_uniq', 'unique(name)', _(u'Ya existe un genero con el mismo nombre'))]
    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if  re.search("[^a-z, A-Z]", bloody_type.name): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es invalido."), ['name'])]
   
            
class zones(osv.osv):
    _name = "zones"
    _description = "Categoriza zonas por provincias"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', 'Ya existe una zona con el mismo nombre')]
    _columns = {
        "name": fields.char("Zona",size=35, required=True),
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
    _name = "estado.civil"
    _description = "Informacion sobre estado civil"
    _order = "name"
    _sql_constraints = [('name_uniq', 'unique(name)', 'Ya existe un Estado Civil con el mismo nombre')]
    _columns = {
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
    }
    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if  re.search("[^a-z, A-Z]", bloody_type.name): return False
        return True 

#    _constraints = [(_alphabetical, _(u"El Tipo de dato es invalido."), ['name'])]

#CARGA FAMILIAR
class family_burden(osv.osv):    
    _name = "family.burden"
    _description = "Carga Familiar"       
    _order = "last_name"
    #_sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=20, required=True),
			"last_name": fields.char("Apellido", size=20, required=True),
            "type_id": fields.many2one("identification.type", "Tipo de identificacion"),
            "number_id": fields.char("Nro Identificacion", size=15, required=True),
            "type_rel_family": fields.many2one("family.relationship","Tipo de Relacion"),
            "date_birth": fields.date("Fecha nacimiento", required=True),
            "phone": fields.char("Telefono", size=10, requiered=True),
            "movil": fields.char("Celular", size=10, requiered=True),            
            "type_instruction": fields.many2one("instruction","Instruccion"),
            "check_contact_sos": fields.boolean("Contacto emergencia", requiered=True),
    }
    _defaults = {
        "check_contact_sos": False,
        }    
#"instruction": fields.many2one("instruction", "Instruccion"),

#    _constraints = [(_no_numbers, _(u"El Tipo de dato es invalido."), ['name'])]

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
    _name="entity.finance"
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

class bank_account_type(osv.osv):
    """Clase de los tipos de cuentas bancarias"""
    _name="bank.account.type"
    _description="Tipo de Cuenta"
    _order="name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un tipo de cuenta bancaria con ese nombre.'))]
    _columns={
            "name" : fields.char("Nombre",size=50,required=True),
    }
    def _no_numbers(self, cr, uid, ids):
        for bank_account_type in self.browse(cr, uid, ids):
            if re.search("[^a-z, A-Z]", bank_account_type.name): return False
        return True 
    _constraints = [(_no_numbers, _(u'Debe contener solo caracteres alfabéticos.'), ['Nombre'])]

class bank_info(osv.osv):
    """Clase de la informacion bancaria de los usuarios"""
    _name="bank.info"
    _description="Informacion bancaria"
    _order="id_entity_finance"
    _sql_constraints = [('name_unique', 'unique(number)', _(u'Ya existe una cuenta con ese numero'))]
    _columns={
            "id_entity_finance": fields.many2one("entity.finance","Entidad Financiera",required=True),
            "id_bank_account": fields.many2one("bank.account.type","Tipo de Cuenta",required=True),
            "number" : fields.char("Número",size=15,required=True),
			"curriculum_id": fields.many2one("curriculum")
    }
    def _no_char(self, cr, uid, ids):
        for bank_info in self.browse(cr, uid, ids):
            if re.search("[^0-9]", bank_info.number): return False
        return True 

    _constraints = [(_no_char, _(u"Debe contener solo números."), ['Numero'])]

#TIPO DE DISCAPACIDAD
class type_disability(osv.osv):    
    _name = "type.disability"
    _description = "Tipo de Discapacidad"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un tipo de discapacidad con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=30, required=True),
            "description": fields.text("Descripcion"),
    }
    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if not (re.search("[a-z, A-Z]", bloody_type.name)): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es invalido."), ['name'])]

#TIPO DE ESTUDIOS DE LENGUAJE
class language_studies(osv.osv):    
    _name = "language.studies"
    _description = "Lenguajes estudiados"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un tipo de discapacidad con el mismo nombre'))]
    _columns={
            "name": fields.char("Idioma", size=15, required=True),
            "percentage_listening": fields.char("Nivel Escuchado", size=4, required=True),
            "percentage_spoken": fields.char("Nivel Oral", size=4, required=True),
            "percentage_read": fields.char("Nivel Leido", size=4, required=True),
            "percentage_written": fields.char("Nivel Escrito", size=4, required=True),
            "certificate_proficiency": fields.boolean("Certificado de suficiencia", requiered=True),
            "institution_language": fields.char("Institucion que le otorgó", size=30, required=True),                        
    }
    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if not (re.search("[a-z, A-Z]", bloody_type.name)): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es invalido."), ['name'])]

#TIPO DE EVENTO
class event_type(osv.osv):    
    _name = "event.type"
    _description = "Tipo de Evento "       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=20, required=True),
            "description": fields.text("Descripcion"),
    }
    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if  re.search("[^a-z, A-Z]", bloody_type.name): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es invalido."), ['name'])]

#CAPACITACION ESPECIFICA
class info_training(osv.osv):    
    _name = "info.training"
    _description = "Capacitacion"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=20, required=True),
	    "date_star": fields.date("Fecha inicio", required=True),
	    "date_end": fields.date("Fecha fin", required=True),
            "event_id": fields.many2one("event.type", "Tipo de evento", required=True),
            "sponsor": fields.char("Auspiciante", size=30, required=True),
            "duration": fields.char("Duracion/horas", size=4, required=True),
            "title_cert": fields.char("Titulo Certificado", size=30, requiered=True),
            "certified_for": fields.char("Certificado por", size=10, requiered=True),            
            "certified_type_id": fields.many2one("certified.type", "Tipo de evento", required=True),
            "country_id": fields.many2one("res.country","Pais"),
    }
 

class certified_type(osv.osv):    
    _name = "certified.type"
    _description = "Tipo de Certificado"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=15, required=True),
            "description": fields.text("Descripcion"),
    }
    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if  re.search("[^a-z, A-Z]", bloody_type.name): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es invalido."), ['name'])]
