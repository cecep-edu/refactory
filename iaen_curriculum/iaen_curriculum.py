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

class curriculum(osv.osv):
	_name = "curriculum"
	_description = "Registra la Hoja de Vida de los usuarios"
	_columns = {
		"picture": fields.binary("Foto"),
		"partner_id": fields.many2one("res.partner", "Usuario", required=True),
		"civil_status_id": fields.many2one("civil.status", "Estado Civil", required=True),
		"gender_id": fields.many2one("gender", "Género", required=True),
		"blood_type_id": fields.many2one("blood.type", "Tipo de Sangre", required=True),
		"country_id": fields.many2one("res.country", "País de Nacimiento", required=True),
		"birth_city_id": fields.many2one("canton", "Ciudad de Nacimiento", required=True),
		"residence_city_id": fields.many2one("canton", "Ciudad de Residencia", required=True),
		"identification_type_id": fields.many2one("identification.type", u"Tipo de Identificación", required=True),
		"identification_number": fields.char("Número de Identificación", size=13, required=True),
		"nationality_id": fields.many2one("nationality", "Nacionalidad", required=True),
		"home_phone": fields.char("Teléfono Domicilio", size=15, required=True),
		"mobile_phone": fields.char("Teléfono Móvil", size=15, required=True),
		"street_address_1": fields.char("Dirección Calle 1", size=200, required=True),
		"street_address_2": fields.char("Dirección Calle 2", size=200, required=False),
		"house_number": fields.char("Número de Casa", size=7, required=False),
		"location_reference": fields.text(u"Referencia de Ubicación"),
		"disability": fields.boolean("Discapacidad"),
		"disability_id": fields.many2one("type.disability", "Tipo de Discapacidad"), 
		"disability_degree": fields.char("Grado de Discapacidad", size=150), 
		"conadis_number": fields.char("Número del Carnet del CONADIS.", size=10, require=True),
		"ethnic_group_id": fields.many2one("ethnic.group", u"Grupo Étnico", required=True),
		"family_burden_ids": fields.one2many("family.burden", "curriculum_id", 'Carga Familiar', required=False),
		"bank_info_ids": fields.one2many("bank.info", "curriculum_id", "Información Bancaria", required=False),
		"instruction_info_ids" : fields.one2many("instruction.info", "curriculum_id", "Instrucción Académica"),
		"experience_info_ids": fields.one2many("experience.info","curriculum_id", "Experiencia Laboral"),
		"language_studies_ids": fields.one2many("language.studies","curriculum_id","Idiomas estudiados"),
		"info_training_ids": fields.one2many("info.training","curriculum_id","Capacitaciones"),

	}
	def _only_numbers(self, cr, uid, ids):
		for curriculum in self.browse(cr, uid, ids):
			if not (re.search("^-?[0-9]+$", curriculum.identification_number)): return False
		return True 
	def on_disability(self, cr, uid, ids, disability):
		if not disability:
			return {'value':{'disability_id': "", 'disability_degree': ""}}
		else:
			return {}

	_constraints = [(_only_numbers, u"El Número de Identificación debe contener sólo digitos.", ['identification_number'])]

class instruction_info(osv.osv):
    """Clase sobre la informacion de la instruccion academica del usuario"""
    _name="instruction.info"
    _description="Información Académica"
    _order_="instruction_id"
    _columns={
        'instruction_id' : fields.many2one("instruction", "Nivel de Instrucción",required=True),
        'name_institution': fields.char("Nombre de la Institución", size=100, required=True),
        'specialization': fields.char("Especialización", size=200, required=True),
        'title' : fields.char("Título", size=150, required=True),
        'register': fields.char("Registro SENESCYT", size=50),
        'curriculum_id' : fields.many2one("curriculum"),
    }

class experience_info(osv.osv):
    """Clase sobre la información de la experiencia laboral del usuario"""
    _name="experience.info"
    _description="Experiencia Laboral"
    _order_="init_date"
    _columns={
        'init_date' : fields.date("Fecha de Inicio", required=True),
        'end_date': fields.date("Fecha de Fin", required=True),
        'company' : fields.char("Organización/Empresa", size=200, required=True),
        'position': fields.char("Denominación del Puesto", size=200, required=True),
        'functions' : fields.text("Responsabilidades/Actividades/Funciones", required=True),
        'curriculum_id' : fields.many2one("curriculum"),
    }
    def on_date(self, cr, uid, ids, init_date, end_date):
    	if end_date:
	    	if(init_date > end_date): 	    		
				return {'value':{'init_date': "", 'end_date': ""}, 'warning':{'title':'Error de Validación',
						'message':'La Fecha de Inicio debe ser menor que la Fecha de Fin'}}
	    	else:
				return {'value': {}}
	else:
		return {'value': {}}
    #_constraints = [(_date, u"La Fecha de Inicio debe ser menor que la Fecha de Fin", ['init_date', 'end_date'])]

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

class family_burden(osv.osv):    
    _name = "family.burden"
    _description = "Carga Familiar"       
    _order = "last_name"
    #_sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=20, required=True),
	    "last_name": fields.char("Apellido", size=20, required=True),
            "type_id": fields.many2one("identification.type", "Tipo de identificación"),
            "number_id": fields.char("Nro Identificación", size=15, required=True),
            "type_rel_family": fields.many2one("family.relationship","Tipo de Relación"),
            "date_birth": fields.date("Fecha nacimiento", required=True),
            "phone": fields.char("Teléfono", size=10, requiered=True),
            "movil": fields.char("Celular", size=10, requiered=True),            
            "type_instruction": fields.many2one("instruction","Instrucción"),
            "check_contact_sos": fields.boolean("Contacto emergencia", requiered=True),
			"curriculum_id": fields.many2one("curriculum")
    }
    _defaults = {
        "check_contact_sos": False,
        }   

#TIPO DE ESTUDIOS DE LENGUAJE
class language_studies(osv.osv):    
    _name = "language.studies"
    _description = "Lenguajes estudiados"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un tipo de discapacidad con el mismo nombre'))]
    _columns={
	    "language_type_id": fields.many2one("language.type","Idioma"),
            "percentage_listening": fields.char("Nivel Escuchado", size=4, required=True),
            "percentage_spoken": fields.char("Nivel Oral", size=4, required=True),
            "percentage_read": fields.char("Nivel Leído", size=4, required=True),
            "percentage_written": fields.char("Nivel Escrito", size=4, required=True),
	    "native_language": fields.boolean("Lenguaje Nativo", required=True),
            "certificate_proficiency": fields.boolean("Certificado de suficiencia", requiered=True),
            "institution_language": fields.char("Institución que le otorgó", size=30),
	    "curriculum_id": fields.many2one("curriculum")
    }
    def _alphabetical(self, cr, uid, ids):
        for bloody_type in self.browse(cr, uid, ids):
            if not (re.search("[a-z, A-Z]", bloody_type.name)): return False
        return True 

    _constraints = [(_alphabetical, _(u"El Tipo de dato es invalido."), ['name'])]

#CAPACITACION ESPECIFICA
class info_training(osv.osv):    
    _name = "info.training"
    _description = "Clase Capacitacion"       
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))]
    _columns={
            "name": fields.char("Nombre", size=35, required=True),
	    "date_star": fields.date("Fecha inicio", required=True),
	    "date_end": fields.date("Fecha fin", required=True),
            "event_id": fields.many2one("event.type", "Tipo de evento", required=True),
            "certified_for": fields.char("Certificado por", size=10, requiered=True),            
            "duration": fields.char("Duración/horas", size=4, required=True),
            "title_cert": fields.char("Título Certificado", size=30, requiered=True),
            "certified_for": fields.char("Certificado por", size=10, requiered=True),            
            "certified_type_id": fields.many2one("certified.type", "Tipo de Certificado", required=True),
            "country_id": fields.many2one("res.country","Pais"),
	    "curriculum_id": fields.many2one("curriculum"),
    }
    def on_date(self, cr, uid, ids, date_star, date_end):
    	if date_end:
	    	if(date_star > date_end): 	    		
				return {'value':{'date_star': "", 'date_end': ""}, 'warning':{'title':'Error de Validación',
						'message':'La Fecha de Inicio debe ser menor que la Fecha de Fin'}}
	    	else:
				return {'value': {}}
	else:
		return {'value': {}}
