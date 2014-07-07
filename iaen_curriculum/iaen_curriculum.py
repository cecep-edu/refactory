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
	_order = ""
	_columns = {
		"estado_civil_id": fields.many2one("estado_civil", u"Estado Civil", required=True),
		"gender_id": fields.many2one("gender", u"Género", required=True),
		"blood_type_id": fields.many2one("blood.type", u"Tipo de Sangre", required=True),
		"country_id": fields.many2one("res.country", u"País de Nacimiento", required=True),
		"birth_city_id": fields.many2one("canton", u"Ciudad de Nacimiento", required=True),
		"residence_city_id": fields.many2one("canton", u"Ciudad de Residencia", required=True),
		"identification_type_id": fields.many2one("identification.type", u"Tipo de Identificación", required=True),
		"nationality_id": fields.many2one("nationality", u"Nacionalidad", required=True),
		"home_phone": fields.char("Teléfono Domicilio", size=15, required=True),
		"mobile_phone": fields.char("Teléfono Móvil", size=15, required=True),
		"street_address_1": fields.char("Dirección Calle 1", size=200, required=True),
		"street_address_2": fields.char("Dirección Calle 2", size=200, required=False),
		"house_number": fields.char("Número de Casa", size=7, required=False),
		"location_reference": fields.text(u"Referencia de Ubicación"),
		"disability": fields.boolean("Discapacidad"),
		"disability_id": fields.many2one("disability", "Tipo de Discapacidad", required=True),
		"disability_degree": fields.char("Grado de Discapacidad", size=150, required=False),
		"conadis_number": fields.char("Número del Carnet del CONADIS.", size=10, required=False),
		"ethnic_group_id": fields.many2one("ethnic_group", u"Grupo Étnico", required=True),
		"family_burden": fields.char("Carga Familiar"),
		"bank_info_id": fields.many2one("bank_info", "Información Bancaria", required=False)
	}
