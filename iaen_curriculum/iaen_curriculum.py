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
		"partner_id": fields.many2one("res.partner", u"Usuario", required=True),
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
		"family_burden_ids": fields.one2many("family.burden", "curriculum_id", 'Carga Familiar', required=False),
		"bank_info_ids": fields.one2many("bank.info", "curriculum_id", "Información Bancaria", required=False)
	}
	def _only_numbers(self, cr, uid, ids):
		for curriculum in self.browse(cr, uid, ids):
			if not (re.search("^-?[0-9]+$", curriculum.identification_number)): return False
		return True 

	_constraints = [(_only_numbers, u"El Número de Identificación debe contener sólo digitos.", ['identification_number'])]


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
    _order = "lastName"
    _columns={
            "name": fields.char("Nombre", size=12, required=True),
			"lastName": fields.char("Apellido", size=12, required=True),
            "typeId": fields.many2one("identification.type", "Tipo de identificacion"),
            "numberId": fields.char("Nro Identificacion", size=15, required=True),
            "typeRelFamily": fields.many2one("family.relationship","Tipo de Relacion"),
            "dateBirth": fields.date("Fecha nacimiento", required=True),
            "phone": fields.char("Telefono", size=10, requiered=True),
            "movil": fields.char("Celular", size=10, requiered=True),            
            "checkContactSos": fields.boolean("Contacto emergencia", requiered=True),
			"curriculum_id": fields.many2one("curriculum")
    }
    _defaults = {
        "checkContactSos": False,
        }
