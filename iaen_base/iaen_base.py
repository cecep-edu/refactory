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

class identification_type(osv.osv, validation):
    _name = "identification.type"
    _description = u'Identificacion con pasaporte o Cédula de ciudadania'
    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe un tipo de identificación con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns = {
        "code_mrl": fields.char("Código MRL", size=3),
        "name": fields.char("Nombre", size=100, required=True),
        "description": fields.text("Descripción"),
    }
    _constraints = [
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]

class ethnic_group(osv.osv, validation):
    _name = "ethnic.group"
    _description = "Almacena los grupos etnicos"
    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe un grupo étnico con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns = {
        "code_mrl": fields.char("Código MRL", size=3),
        "name": fields.char("Nombre", size=100, required=True),
        "description": fields.text("Descripción"),
    }
    _constraints = [
        (validation.no_numbers, _(u"El Grupos Étnicos no debe contener números."), ['name']),
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]



#CLASE PARA TIPO DE SEXO
class type_sex(osv.osv, validation):    
    _name="type.sex"
    _description="Tipos de sexo"
    _order = "name"        
    _columns={
        "name" : fields.char("Nombre",size=15,required=True),
        "code_mrl": fields.char("Código MRL", size=3),
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', _(u'Ya existe un genero con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _constraints = [
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]

            
class zones(osv.osv, validation):
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

class res_country(osv.osv, validation):
    """
    Herencia para la creación del CRUD para paices, heredado desde la tabla res_country
    code_mrl:
    """
    _inherit = "res.country"
    _columns = {
        "code_mrl": fields.char("Codigo MRL", size=3),
    }
    _sql_constraints = [
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _constraints = [
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]

class res_country_state(osv.osv, validation):
    """
    Herencia para la creación del CRUD para los estados o provincias, heredado desde la tabla res_country_state
    code_mrl:
    zone_id:
    """
    _inherit = "res.country.state"
    _columns = {
        "code_mrl": fields.char("Código MRL", size=3),
        "zone_id": fields.many2one("zones","Zona",help="Distribución zonal, a la que pertenece la provincia")
    }
    _sql_constraints = [
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _constraints = [
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]

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
        
class canton(osv.osv, validation):
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
        "code_mrl": fields.char("Código MRL", size=3),
        "country_state_id": fields.many2one("res.country.state","Provincia",required=True),
    }
    _sql_constraints = [
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _constraints = [
        #(validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]


class parish(osv.osv, validation):
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
        "code_mrl": fields.char("Código MRL", size=3),
        "canton_id": fields.many2one("canton","Cantón",required=True),
        "description": fields.text("Descripción"),
    }
    _sql_constraints = [
        #('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _constraints = [(validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])]


class blood_type(osv.osv, validation):
   #""" Clase para los Tipos de Sangre """ 
    _name = "blood.type"
    _description = "Registra los tipos de sangre"
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Ya existe un Registro con el mismo nombre'),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns = {
        'name': fields.char("Nombre", size=3, required=True),
        'code_mrl': fields.char('Código MRL', size=3)
    }
    _order = "name"
    _constraints = [
        (validation.no_numbers, _(u"El nombre del Tipo de Sangre debe contener solo letras."), ['name']),
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]


class civil_status(osv.osv, validation):
    _name = "civil.status"
    _description = "Informacion sobre estado civil"
    _order = "name"
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Ya existe un Estado Civil con el mismo nombre'),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns = {
        'code_mrl': fields.char('Código MRL', size=3),
        'name' : fields.char("Nombre", size=50, required=True),
    }
    _constraints = [
        (validation.no_numbers, _(u"El Estado Civil no debe contener números."), ['name']),
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]

#PARENTESCO FAMILIAR
class family_relationship(osv.osv, validation):    
    _name = "family.relationship"
    _description = "Parentesco Familiar"       
    _order = "name"
    _columns={
        "code_mrl": fields.char("Código MRL", size=3),
        "name": fields.char("Nombre", size=20, required=True),
        "description": fields.text("Descripción"),
    }
    _sql_constraints = [
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl')),
        ('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))
    ]
    _constraints = [
       (validation.no_numbers, _(u"El Parentesco Familiar no debe contener números."), ['name']),
       #(validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]


class nationality(osv.osv, validation):
	""" Clase para las Nacionalidades """
	_name = "nationality"
	_description = "Registra las nacionalidades"
	_columns = {
		'name': fields.char("Nombre", size=45, required=True),
		'code_mrl': fields.char("Código MRL", size=3)
	}
	_order = "name"
	_sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe una Nacionalidad con ese nombre.')),
		('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese Código Mrl'))
    ]
	_constraints = [
        (validation.only_letters, _(u"La Nacionalidad debe contener letras únicamente"), ['name']),
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]

class instruction(osv.osv, validation):
	#"""Clase para las Instrucciones"""
    _name = "instruction"
    _order = "name"
    _description = "Registra las instrucciones"
    _columns = {
        'code_mrl': fields.char("Código MRL", size=3),
        'name': fields.char("Nombre", size=200, required=True),
        'description': fields.text("Descripción"),
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Ya existe un Registro con el mismo nombre'),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _constraints = [
        (validation.only_letters, _(u"Los Niveles de Instrucciones deben contener letras únicamente"), ['name']),
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]
	
class entity_finance(osv.osv, validation):
    """Clase de los diferentes entidades financieras existentes en Ecuador"""
    _name="entity.finance"
    _description="Entidad Financiera"
    _order="name"
    _sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe una Entidad Financiera con ese nombre.')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns={
        'code_mrl': fields.char("Código MRL", size=3),
        "name" : fields.char("Nombre",size=50,required=True),
    }
    _constraints = [
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl']),
    ]
  
class bank_account_type(osv.osv, validation):
    """Clase de los tipos de cuentas bancarias"""
    _name="bank.account.type"
    _description="Tipo de Cuenta"
    _order="name"
    _sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe un tipo de cuenta bancaria con ese nombre.')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns={
       'code_mrl': fields.char("Código MRL", size=3),
        "name" : fields.char("Nombre",size=50,required=True),
    }
    _constraints = [(validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])]
    
#TIPO DE DISCAPACIDAD
class type_disability(osv.osv, validation):    
    _name = "type.disability"
    _description = "Tipo de Discapacidad"       
    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe un tipo de discapacidad con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns={
        "name": fields.char("Nombre", size=30, required=True),
        "description": fields.text("Descripcion"),
        "code_mrl": fields.char("Código MRL", size=3),
    }
    _constraints = [
        (validation.only_letters, _(u"El Tipo de Discapacidad debe contener solo letras."), ['name']),
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]


#TIPO DE EVENTO
class event_type(osv.osv, validation):    
    _name = "event.type"
    _description = "Tipo de Evento "       
    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns={
        "name": fields.char("Nombre", size=20, required=True),
        "description": fields.text("Descripcion"),
        "code_mrl": fields.char("Codigo MRL", size=3),
    }
    _constraints = [
        (validation.only_letters, _(u"El Tipo de Evento debe contener solo letras."), ['name']),
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]
    
class certified_type(osv.osv,validation):    
    _name = "certified.type"
    _description = "Tipo de Certificado"       
    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns={
            "name": fields.char("Nombre", size=20, required=True),
            "description": fields.text("Descripcion"),
            "code_mrl": fields.char("Código MRL", size=3),
    }
    _constraints = [
        (validation.only_letters, _(u"El Tipo de Certificado debe contener solo letras."), ['name']),
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]


class hr_job(osv.osv, validation): 
    """Clase heredada del modulo de recursos humanos para la creacion de puestos de trabajo"""   
    _inherit = "hr.job"
    _sql_constraints = [
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns={
        "code_mrl": fields.char("Codigo MRL", size=3),
    }
    _constraints = [(validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])]
  
#CLASE PARA IDIOMAS
class language_type(osv.osv, validation):
    """Clase para los diferentes tipos de Idiomas"""    
    _name="language.type"
    _description="Tipos de lenguajes"
    _order = "name"        
    _sql_constraints = [('name_uniq', 'unique(name)', _(u'Ya existe un campo con el mismo nombre'))]
    _columns={
        "cod_language" : fields.char("Detalle", size=25, required=True),
        "name" : fields.char("Nombre",size=30,required=True),        
    }
    _constraints = [
        #(validation.only_letters, _(u"El Tipo de lenguajes debe contener solo letras."), ['name'])
    ]


class input_motive(osv.osv, validation):
    """Clase de los difrentes motivos para la entrada a un puesto de trabajo"""    
    _name="input.motive"
    _description="Motivos de Entrada Laboral"
    _order = "name"        
    _sql_constraints = [
        ('name_uniq', 'unique(name)', _(u'Ya existe un registro con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))]
    _columns={
        "code_mrl": fields.char("Codigo MRL", size=3),
        "name" : fields.char("Nombre",size=100,required=True), 
        "description": fields.text("Descripción")       
    }
    _constraints = [(validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])]
  
class output_motive(osv.osv, validation): 
    """Clase de los difrentes motivos para la salida de un puesto de trabajo"""      
    _name="output.motive"
    _description="Motivos de Salida Laboral"
    _order = "name"        
    _sql_constraints = [
        ('name_uniq', 'unique(name)', _(u'Ya existe un registro con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))]
    _columns={
        "code_mrl": fields.char("Codigo MRL", size=3),
        "name" : fields.char("Nombre",size=100,required=True), 
        "description": fields.text("Descripción"),       
    }
    _constraints = [(validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])]

class entity_type(osv.osv, validation):
    """Clase de los tipos de entidades de trabajo en el Ecuador"""      
    _name="entity.type"
    _description="Tipos de Entidades"
    _order = "name"        
    _sql_constraints = [
        ('name_uniq', 'unique(name)', _(u'Ya existe un registro con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))]
    _columns={
        "code_mrl": fields.char("Codigo MRL", size=3),
        "name" : fields.char("Nombre",size=100,required=True), 
        "description": fields.text("Descripción"),       
    }
    _constraints = [(validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])]

class entity_public(osv.osv, validation):
    """Clase de las entidades publicas que existen en el Ecuador"""      
    _name="entity.public"
    _description="Entidades Publicas"
    _order = "name" 
    _sql_constraints = [
        ('name_uniq', 'unique(name)', _(u'Ya existe un registro con el mismo nombre')),
        #('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]       
    _columns={
        #"code_mrl": fields.char("Codigo MRL", size=3),
        "ruc": fields.char("R.U.C.",size=13), 
        "name" : fields.char("Nombre",size=100,required=True), 
        "description": fields.text("Descripción"),       
    }

#CLASE: NOTARIAS
class name_notary(osv.osv, validation):   
    """Clase de Notarias publicas en el Ecuador""" 
    _name = "name.notary"
    _description = "Notarias del Ecuador"       
    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe un campo con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns={
        "name": fields.char("Nombre", size=30, required=True),
        "code_mrl": fields.char("Codigo MRL", size=3),
    }
    _constraints = [
        #(validation.only_letters, _(u"El nombre de la Notaria debe contener solo letras."), ['name']),
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]


#CLASE: Nacionalidad Indigena
class indian_nationality(osv.osv, validation):    
    _name = "indian.nationality"
    _description = "Nacionalidad indigena"       
    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe un campo con el mismo nombre')),
        ('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns={
        "name": fields.char("Nombre", size=30, required=True),
        "code_mrl": fields.char("Codigo MRL", size=3),
    }
    _constraints = [
        (validation.only_letters, _(u"El nombre de la Nacionalidad indigena debe contener solo letras."), ['name']),
        (validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]
    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if not (re.search("[a-z, A-Z]", bloody_type.name)): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es inválido."), ['name'])]

#CLASE: Remuneraciones
class sp_type(osv.osv, validation):   
    """Clase de las remuneraciones economicas en el sector publico""" 
    _name = "sp.type"
    _description = "Escalas Remuneraciones"       
    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique(name)', _(u'Ya existe un campo con el mismo nombre')),
        #('cod_unique', 'unique(code_mrl)', _(u'Ya existe un Registro con ese código Mrl'))
    ]
    _columns={
        "name": fields.char("Nombre", size=50, required=True),
        "grade": fields.char("Grado", size=5,),
        "rmu": fields.float('RMU', digits=(6,2)),
        "description": fields.text("Descripción"),  
        #"code_mrl": fields.char("Codigo MRL", size=3),
    }
    _constraints = [
        #(validation.only_letters, _(u"El nombre de la Notaria debe contener solo letras."), ['name']),
        #(validation.only_numbers, _(u"El Código MRL debe contener solo números."), ['code_mrl'])
    ]
