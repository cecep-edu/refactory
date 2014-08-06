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


class instruction_info(osv.osv):
    """Clase sobre la informacion de la instruccion academica del usuario"""
    _name="instruction.info"
    _description="Información Académica"
    _order_="instruction_id"
    
    _columns={
        'instruction_id' : fields.many2one("instruction", "Nivel de Instrucción",required=True),
        'specialization_type': fields.selection([('2','Diplomado'),('3', 'Especialidad'),('4', 'Maestria')
            ,('5', 'Doctorado')],'Tipo de Especialización', readonly=True, states={'cuarto':[('readonly',False), ('required',True)]}),
        'name_institution': fields.char("Nombre de la Institución", size=100, required=True),
        'specialization': fields.char("Especialización", size=200),
        'title' : fields.char("Título", size=150, required=True),
        'register': fields.char("Registro SENESCYT", size=50),
        'graduate': fields.boolean("Egresado", requiered=True),
        'year_semester':fields.selection([('1','Años'),('2', 'Semestre')],'Periodo de Estudio',requiered=True),
        'partner_id' : fields.many2one("res.partner"),
        'state': fields.selection([('cuarto', 'cuarto'),('otro', 'otro')], invisible=True)
    }
    _defaults = {
        'state':'otro'
    }
    def on_quart(self, cr, uid, ids, id_level):
		if id_level:
			obj = self.pool.get('instruction').browse(cr,uid,id_level)
			if obj.name.lower().find('cuarto')>=0:
				return {'value':{'state':'cuarto'}}
			else:
				return {'value':{'state':'otro', 'specialization_type': ''}}
		else:
			return {'value': {}}

class experience_info(osv.osv):
    """Clase sobre la información de la experiencia laboral del usuario"""
    _name="experience.info"
    _description="Experiencia Laboral"
    _order_="init_date"
    _columns={
        'init_date' : fields.date("Fecha de Inicio", required=True),
        'end_date': fields.date("Fecha de Fin", required=True),
        'entity_type_id': fields.many2one("entity.type", "Tipo de Institución", required=True),
        'company' : fields.char("Organización/Empresa", 
            size=200, 
            #invisible=False,
            states={
                'p':[('required',False),('readonly','True')],
                'o':[('required',True)]
            }),
        'entity_public_id': fields.many2one("entity.public", "Entidad Pública", 
            readonly=True,
            states={
                'p':[('readonly','False'),('required',True)],
            }),
        'job' : fields.char("Denominación de Puesto", required=True),
        'sp': fields.many2one("sp.type", "Escala Remuneración", 
             states={
                'p':[('required',True),('readonly',False)],
                'o':[('required',True), ('readonly',True)]
            }),
        'functions' : fields.text("Responsabilidades/Actividades/Funciones"),
        'input_motive_id': fields.many2one("input.motive", "Motivo de Entrada", required=True),
        'output_motive_id': fields.many2one("output.motive", "Motivo de Salida", required=True),
        'partner_id' : fields.many2one("res.partner"),
        'state': fields.selection([('p', 'p'),('o', 'o')], invisible=True)
    }
    _defaults = {
        'state':'o',
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

    def on_entity(self, cr, uid, ids, entity_id):
        if entity_id:
            obj = self.pool.get('entity.type').browse(cr,uid,entity_id)
            if obj.name.upper() == u"PÚBLICA":
                return {'value':{'state':'p'}}
            else:
                return {'value':{'state':'o'}}


class bank_info(osv.osv):
    """Clase de la informacion bancaria de los usuarios"""
    _name="bank.info"
    _description="Informacion bancaria"
    #_order="id_entity_finance"
    _sql_constraints = [('name_unique', 'unique(number)', _(u'Ya existe una cuenta con ese número'))]
    _columns={
        "id_entity_finance": fields.many2one("entity.finance","Entidad Financiera",required=True),
        "id_bank_account": fields.many2one("bank.account.type","Tipo de Cuenta",required=True),
        "number" : fields.char("Número",size=15,required=True),
		"partner_id": fields.many2one("res.partner")
    }
    
class family_burden(osv.osv, validation):    
    _name = "family.burden"
    _description = "Carga Familiar"       
    _order = "last_name"
    #_sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un parentesco con el mismo nombre'))]
    _columns={
        "name": fields.char("Nombre", size=20, required=True),
        "last_name": fields.char("Apellido", size=20, required=True),
        "type_id": fields.many2one("identification.type", "Tipo de identificación", required=True),
        "number_id": fields.char("Nro Identificación", size=15, required=True),
        "type_rel_family": fields.many2one("family.relationship","Tipo de Relación"),
        "date_birth": fields.date("Fecha nacimiento", required=True),
        "phone": fields.char("Teléfono", size=10, requiered=True),
        "movil": fields.char("Celular", size=10, requiered=True),            
        "type_instruction": fields.many2one("instruction","Instrucción"),
        "check_contact_sos": fields.boolean("Contacto emergencia", requiered=True),
		"partner_id": fields.many2one("res.partner")
    }
    _defaults = {
        "check_contact_sos": False,
    }  

#TIPO DE ESTUDIOS DE LENGUAJE
class language_studies(osv.osv):    
    _name = "language.studies"
    _description = "Lenguajes estudiados"       
    _columns={
	    "language_type_id": fields.many2one("language.type","Idioma"),
	    "percentage_listening": fields.integer("Nivel Escuchado", size=3, required=True),
	    "percentage_spoken": fields.integer("Nivel Oral", size=3, required=True),
	    "percentage_read": fields.integer("Nivel Leído", size=3, required=True),
	    "percentage_written": fields.integer("Nivel Escrito", size=3, required=True),
	    "native_language": fields.boolean("lengua materna"),
        "certificate_proficiency": fields.boolean("Certificado de suficiencia", requiered=True),
	    "institution_language": fields.char("Institución que le otorgó", size=30),
	    "partner_id": fields.many2one("res.partner")
	    }
    def on_percentage(self, cr, uid, ids, listening, spoken, read, written):
	    a = False
	    if(listening > 100 or listening < 0):
		    a = True
		    return {'value':{'percentage_listening': ""}, 'warning':{'title':'Error de Validación',
									     'message':'El porcentaje ingresado sobrepasa el 100%'}}		    
	    if(spoken > 100 or listening < 0): 	    		
		    a = True
		    return {'value':{'percentage_spoken': ""}, 'warning':{'title':'Error de Validación',
									  'message':'El porcentaje ingresado sobrepasa el 100%'}}
	    if(read > 100 or listening < 0): 
		    a = True	    		
		    return {'value':{'percentage_read': ""}, 'warning':{'title':'Error de Validación',
									'message':'El porcentaje ingresado sobrepasa el 100%'}}
	    if (a == False):
		    return {'value': {}}

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
		"duration": fields.char("Duración/horas", size=4, required=True),		
		"certified_type_id": fields.many2one("certified.type", "Tipo de Certificado", required=True),
		"country_id": fields.many2one("res.country","Pais"),
		"partner_id": fields.many2one("res.partner"),
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

