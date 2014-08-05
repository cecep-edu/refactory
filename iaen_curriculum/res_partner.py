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
from iaen_curriculum_ws import IaenCurriculumWs 

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
        def on_identification(self, cr, uid, ids, identification_number, identification_type_id):
			values = {}
			if identification_number and identification_type_id:
				id_type = self.pool.get('identification.type').browse(cr, uid, identification_type_id)
				if id_type.name.lower().find(u"cédula")>=0:
					if identification_number.__len__() == 10:
						ws = IaenCurriculumWs()
						data = ws.find_identification_info(identification_number)
						data_disc = ws.find_disability_info(identification_number)
						data_diplo = ws.find_instruction_info(identification_number)

						if(data):
							values['name'] = data['name']
							values['street'] = str(data['address_1'])
							values['birth_city_id'] = self.get_ids(cr, uid, ids, 'canton', str(data['city_birth']))
							values['residence_city_id'] = self.get_ids(cr, uid, ids, 'canton', str(data['city_residency']))
							values['state_id'] = self.get_ids(cr, uid, ids, 'res.country.state', str(data['state_residency']))
							values['country_id'] = self.get_ids(cr, uid, ids, 'res.country', 'Ecuador')
							values['nationality_id'] = self.get_ids(cr, uid, ids, 'nationality', str(data['nationality']))
							values['type_sex_id'] =  self.get_ids(cr, uid, ids, 'type.sex', str(data['gender']))
							values['civil_status_id'] =  self.get_ids(cr, uid, ids, 'civil.status', str(data['civil_status']))
							if data_disc.items():
								values['disability'] = True
								values['disability_id'] = self.get_ids(cr, uid, ids, 'type.disability', str(data_disc['type']))
								values['conadis_number'] = data_disc['conadis_id']
								values['disability_degree'] = data_disc['degree']
							else:
								values['disability'] = False
								values['disability_id'] = None
								values['conadis_number'] = None
								values['disability_degree'] = None
							
							if data_diplo and data_diplo.items():
								values['instruction_info_ids'] = []
								for title in data_diplo:
									#pdb.set_trace()
									instruction_id = data_diplo[title]['level'].split(' ')[2]
									print data_diplo[title]['level'].split(' ')[2]
									state = "otro"
									if data_diplo[title]['level'].split(' ')[2].lower().find('cuarto')>=0:
										state="cuarto"
									else:
										if data_diplo[title]['level'].split(' ')[2].lower()=='nivel':
											instruction_id = "técnico" 
										state="otro"

									val = [{
										#gender_id = self.get.pool('gender').search(cr,uid,[('name','ilike','casado')])
										"instruction_id" : self.get_ids(cr, uid, ids, 'instruction', str(instruction_id)),
										"state": state,
										"name_institution":str(data_diplo[title]['institution_name']),
										"title": str(data_diplo[title]['title_name']),
										"register": str(data_diplo[title]['register_number'])
									}]
									values['instruction_info_ids'] += val
								return {'value': values}
							else:
								return {'value': {}}
						else:
							return {'value': values, 'warning': {'title': 'Error de Cédula', 'message': 'La cédula ingresada no es válida o no existe.'}}
					else:
						return {'value': {}}
				else:
					return {'value': {}}
			else:
				return {'value': {}}

        def get_ids(self, cr, uid, ids, model, name):
			domain = [('name','ilike',name)]
			obj = self.pool.get(model).search(cr, uid, domain)
			#pdb.set_trace()

			try:
				return obj[0]
			except IndexError:
				return None
		
        def city_change(self, cr, uid, ids, city, context=None):
                value = {}
                value['residence_city_id'] = city
                if city:
                        city_obj = self.pool.get('canton').browse(cr, uid, city)
                        if city_obj:
                                value['state_id'] = city_obj.country_state_id.id
                                value['country_id'] = city_obj.country_state_id.country_id.id
                return {'value':value}

        """"
        def default_get(self,cr,uid,fields,context=None):
                if not context.has_key('action_uid'):
                        return super(res_partner, self).default_get(cr, uid, fields, context=context)
                partner_id = self.search(cr, uid,[('user_id.id','=',uid)])
                values = {}
                if partner_id:
                        cur_dict = self.browse(cr, uid, partner_id)[0]
                        
                        burder_ids = []
                        for burder in cur_dict.family_burden_ids:
                                burder_ids.append(burder.id)
            
                        bank_ids = []
                        for bank in cur_dict.bank_info_ids:
                                bank_ids.append(bank.id)
            
                        instruction_ids = []
                        for instruction in cur_dict.instruction_info_ids:
                                instruction_ids.append(instruction.id)

                        experience_ids = []
                        for experience in cur_dict.experience_info_ids:
                                experience_ids.append(experience.id)

                        language_ids = []
                        for language in cur_dict.language_studies_ids:
                                language_ids.append(language.id)

                        training_ids = []

                        for training in cur_dict.info_training_ids:
                                training_ids.append(training.id)
                                
                        values = {
                                "name": cur_dict.name,
                                "email": cur_dict.email,
                                "image": cur_dict.image,
                                "civil_status_id": cur_dict.civil_status_id.id,
                                "gender_id": cur_dict.gender_id.id,
                                "blood_type_id": cur_dict.blood_type_id.id,
                                "country_id":  cur_dict.country_id.id,
                                "birth_city_id":  cur_dict.birth_city_id.id,
                                "residence_city_id":  cur_dict.residence_city_id.id,
                                "identification_type_id":  cur_dict.identification_type_id.id,
                                "identification_number":  cur_dict.identification_number,
                                "nationality_id":  cur_dict.nationality_id.id,
                                "phone":  cur_dict.phone,
                                "mobile":  cur_dict.phone,
                                "street":  cur_dict.street,
                                "street2":  cur_dict.street2,
                                "location_reference":  cur_dict.location_reference,
                                "disability":  cur_dict.disability,
                                "disability_id":  cur_dict.disability_id.id,
                                "disability_degree":  cur_dict.disability_degree,
                                "conadis_number":  cur_dict.conadis_number,
                                "ethnic_group_id":  cur_dict.ethnic_group_id.id,
                                "family_burden_ids": burder_ids, 
                                "bank_info_ids":  bank_ids,
                                "instruction_info_ids" :  instruction_ids,
                                "experience_info_ids":  experience_ids,
                                "language_studies_ids": language_ids,
                                "info_training_ids": training_ids,
                        }
                return values

        def create(self,cr,uid,fields,context=None):
                print
                if not context.has_key('action_uid'):
                        return super(res_partner, self).create(cr, uid, fields, context=context)
                else:
                        partner_id = self.search(cr, uid,[('user_id.id','=',context['action_uid'])])
                        self.write(cr,uid,partner_id,fields)
                        #return {'type': 'ir.actions.act_window_close'}
                        

                return False
        """
