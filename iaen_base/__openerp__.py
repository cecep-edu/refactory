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
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
