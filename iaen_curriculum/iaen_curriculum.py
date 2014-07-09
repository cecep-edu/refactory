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
		"user_id": fields.many2one("res.users", u"Usuario", required=True),
		"estado_civil_id": fields.many2one("estado.civil", u"Estado Civil", required=True),
		"gender_id": fields.many2one("gender", u"Género", required=True),
		"blood_type_id": fields.many2one("blood.type", u"Tipo de Sangre", required=True),
		"country_id": fields.many2one("res.country", u"País de Nacimiento", required=True),
		"birth_city_id": fields.many2one("canton", u"Ciudad de Nacimiento", required=True),
		"residence_city_id": fields.many2one("canton", u"Ciudad de Residencia", required=True),
		"identification_type_id": fields.many2one("identification.type", u"Tipo de Identificación", required=True),
		"identification_number": fields.char("Número de Identificación", size=13, required=True),
		"nationality_id": fields.many2one("nationality", u"Nacionalidad", required=True),
		"home_phone": fields.char("Teléfono Domicilio", size=15, required=True),
		"mobile_phone": fields.char("Teléfono Móvil", size=15, required=True),
		"street_address_1": fields.char("Dirección Calle 1", size=200, required=True),
		"street_address_2": fields.char("Dirección Calle 2", size=200, required=False),
		"house_number": fields.char("Número de Casa", size=7, required=False),
		"location_reference": fields.text(u"Referencia de Ubicación"),
		"disability": fields.boolean("Discapacidad"),
		"disability_id": fields.many2one("type.disability", "Tipo de Discapacidad", required=True), 
		"disability_degree": fields.char("Grado de Discapacidad", size=150, required=True), 
		"conadis_number": fields.char("Número del Carnet del CONADIS.", size=10, require=True),
		"ethnic_group_id": fields.many2one("ethnic.group", u"Grupo Étnico", required=True),
		"family_burden": fields.char("Carga Familiar"),
		"bank_info_id": fields.many2one("bank.info", "Información Bancaria", required=False),
		"instruction_info_ids" : fields.one2many("instruction.info", "curriculum_id", "Instrucción Académica"),
		"experience_info_ids": fields.one2many("experience.info","curriculum_id", "Experiencia Laboral"),
	}
	def _only_numbers(self, cr, uid, ids):
		for curriculum in self.browse(cr, uid, ids):
			if not (re.search("^-?[0-9]+$", curriculum.identification_number)): return False
		return True 

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
