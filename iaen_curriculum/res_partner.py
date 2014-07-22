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

class res_partner(osv.osv):
        _inherit = "res.partner"
        _columns = {
                "civil_status_id": fields.many2one("civil.status", "Estado Civil", required=True),
                "type_sex_id": fields.many2one("type.sex", "Sexo", required=True),
                "blood_type_id": fields.many2one("blood.type", "Tipo de Sangre", required=True),
                "country_id": fields.many2one("res.country", "País de Nacimiento", required=True),
                "birth_city_id": fields.many2one("canton", "Ciudad de Nacimiento", required=True),
                "residence_city_id": fields.many2one("canton", "Ciudad de Residencia", required=True),
                "identification_type_id": fields.many2one("identification.type", u"Tipo de Identificación", required=True),
                "identification_number": fields.char("Número de Identificación", size=13, required=True,help="Cedula de Identidad, Pasaporte, CCI, DNI"),
                "nationality_id": fields.many2one("nationality", "Nacionalidad", required=True),
                "house_number": fields.char("Número de Casa", size=7, required=False),
                "location_reference": fields.text("Referencia de Ubicación"),
                "disability": fields.boolean("Discapacidad"),
                "disability_id": fields.many2one("type.disability", "Tipo de Discapacidad"), 
                "disability_degree": fields.char("Grado de Discapacidad", size=150), 
                "conadis_number": fields.char("N° Carnet del CONADIS", size=10, require=True),
                "ethnic_group_id": fields.many2one("ethnic.group", u"Grupo Étnico", required=True),
                "family_burden_ids": fields.one2many("family.burden", "partner_id", 'Carga Familiar', required=False),
                "bank_info_ids": fields.one2many("bank.info", "partner_id", "Información Bancaria", required=False),
                "instruction_info_ids" : fields.one2many("instruction.info", "partner_id", "Instrucción Académica"),
                "experience_info_ids": fields.one2many("experience.info","partner_id", "Experiencia Laboral"),
                "language_studies_ids": fields.one2many("language.studies","partner_id","Idiomas estudiados"),
                "info_training_ids": fields.one2many("info.training","partner_id","Capacitaciones"),
                
        }
        
        def on_disability(self, cr, uid, ids, disability):
                if not disability:
                        return {'value':{'disability_id': "", 'disability_degree': ""}}
                else:
                        return {}
                        
        def city_change(self, cr, uid, ids, city, context=None):
                value = {}
                value['residence_city_id'] = city
                if city:
                        city_obj = self.pool.get('canton').browse(cr, uid, city)
                        if city_obj:
                                value['state_id'] = city_obj.country_state_id.id
                                value['country_id'] = city_obj.country_state_id.country_id.id
                return {'value':value}
