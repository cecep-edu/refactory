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
{
    'name' : 'IAEN base',
    'version' : '1.0',
    'author' : 'IAEN',
    'category' : 'configuraciones',
    'description' : """
    Ingreso de todas los parametros que son necesarios
    para la creación de la hoja de vida.
    """,
    'website': 'http://www.iaen.edu.ec',
    'data': [
        'views/iaen_base_views.xml',
        'views/iaen_base_actions.xml',
        'views/iaen_base_menus.xml',
        'data/ethnic_group_data.xml',
        'data/identification_type_data.xml',
        'data/civil_status_data.xml',
        'data/type_sex_data.xml',
        'data/family_relationship_data.xml',
        'data/type_disability.xml',
        'data/blood_type_data.xml',
        'data/bank_account_type_data.xml',
        'data/entity_finance_data.xml',
        'data/nationality_data.xml',
        'data/zones_data.xml',
        'data/res_country_data.xml',
        'data/res_country_state_data.xml',
        'data/canton_data.xml',
        'data/parish_data.xml',
        'data/event_type_data.xml',
        'data/instruction_data.xml',
        'data/language_data.xml',
        'data/certified_type_data.xml',
        'data/input_motive_data.xml',
        'data/output_motive_data.xml',
        'data/entity_type_data.xml',
        'data/notary_data.xml',
        'data/Indian_nationality_data.xml',
        'data/entity_public_data.xml',
        'data/sp_type_data.xml',
    ],
    'update_xml': [
        'data/users_data.xml',
        'security/ir.model.access.csv'
    ],
    'depends': [
        'hr',
    ],
    'images' : ['images/iaen_base.jpeg'],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
