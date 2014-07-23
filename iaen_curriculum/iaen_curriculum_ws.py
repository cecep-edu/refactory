from suds.client import Client
from suds.wsse import *
from suds.sax.element import Element
from suds.sax.attribute import Attribute
from suds.xsd.sxbasic import Import

class IaenCurriculumWs:

	def __init__(self, usuario=None):
		# Usuario para consultar el servicio de permiso
		self.ws_user = '1103635445' 
		# Url del servicio de permiso
		self.auth_client = Client(url='https://www.bsg.gob.ec/sw/STI/BSGSW08_Acceder_BSG?wsdl')
		# El tipo de Dato validarPermisoPeticion
		self.request = self.auth_client.factory.create('validarPermisoPeticion')

	def find_identification_info(self, identification):
		response = self.get_authorization('https://www.bsg.gob.ec/sw/RC/BSGSW01_Consultar_Cedula?wsdl')
		wss_header = self.generate_header_authentication(response)
		client = Client(url='https://www.bsg.gob.ec/sw/RC/BSGSW01_Consultar_Cedula?wsdl')
		client.set_options(soapheaders=wss_header)
		client_response = client.service.BusquedaPorCedula(identification, 'testroot', 'Sti1DigS21')
		data = {
			"address_1": str(client_response['CalleDomicilio']),
			"house_number": str(client_response['NumeroDomicilio']),
			"state_residency": str(client_response['Domicilio'].split('/')[0]).capitalize(),
			"city_residency": str(client_response['Domicilio'].split('/')[1]).capitalize(),
			"parish_residency": str(client_response['Domicilio'].split('/')[2]).capitalize(),
			"state_birth": str(client_response['LugarNacimiento'].split('/')[0]).capitalize(),
			"city_birth": str(client_response['LugarNacimiento'].split('/')[1]).capitalize(),
			"parish_birth": str(client_response['LugarNacimiento'].split('/')[2]).capitalize(),
			"civil_status": str(client_response['EstadoCivil']).capitalize(),
			"birth_date": str(client_response['FechaNacimiento']),
			"gender": str(client_response['Genero']).capitalize(),
			"nationality": str(client_response['Nacionalidad']),
			"name": str(client_response['Nombre'])
		}

		return data


	def find_instruction_info(self, identification):
		response = self.get_authorization('https://www.bsg.gob.ec/sw/SENESCYT/BSGSW01_Consultar_Titulos?wsdl')
		wss_header = self.generate_header_authentication(response)
		client = Client(url='https://www.bsg.gob.ec/sw/SENESCYT/BSGSW01_Consultar_Titulos?wsdl')
		client.set_options(soapheaders=wss_header)
		client_response = client.service.consultaTitulo(identification)

		data = {}

		if client_response:
			index = 0
			for title_level in client_response['niveltitulos']:
				for title in title_level.titulo:
					title_data = {index:{
						"level": title_level["nivel"].encode('UTF-8'),
						"institution_name": title["ies"].encode('UTF-8'),
						"title_name": title["nombreTitulo"].encode('UTF-8'),
						"register_number": title["numeroRegistro"].encode('UTF-8'),
						"register_date": title["fechaRegistro"].encode('UTF-8')
					}}
					data.update(title_data)
					index+=1
		return data



	def find_disability_info(self, identification):
		response = self.get_authorization('https://www.bsg.gob.ec/sw/MSP/BSGSW01_Consultar_Discapacidad?wsdl')
		wss_header = self.generate_header_authentication(response)
		client = Client(url='https://www.bsg.gob.ec/sw/MSP/BSGSW01_Consultar_Discapacidad?wsdl')
		client.set_options(soapheaders=wss_header)
		client_response = client.service.BuscarPersonaConDiscapacidad(identification,'WS-SNAP','StiDig02')

		data = {}
		try: # and not client_response["Mensaje"]
			data = {
				"conadis_id": str(client_response['CodigoConadis']),
				"type": str(client_response['DeficienciaPredomina']),
				"degree": str(client_response['GradoDiscapacidad'])
			}
		except AttributeError:
			data = {}
		except KeyError:
			data = {}

		#print data
		return data


	
	def get_authorization(self, url):
		self.request.Cedula = self.ws_user
		self.request.Urlsw = url
		return self.auth_client.service.ValidarPermiso(self.request)
		

	def generate_header_authentication(self, response):
		"""
		Se construye la estructura XML para la autorizacion WS-Security
		que luego se insertara en el header de la peticion SOAP
		"""
		wss = ('wss', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')
		wsu = ('wsu', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd')
		#print response
		username_token = Element('UsernameToken', ns=wss).setText('')
		username = Element('Username', ns=wss).setText(self.ws_user)

		nonce = Element('Nonce', ns=wss).setText(response['Nonce'])
		nonce.append(Attribute('EncodingType', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary'))

		password = Element('Password', ns = wss).setText(response['Digest'])
		password.append(Attribute('Type', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest'))

		create = Element('Created', ns = wsu).setText(response['Fecha'])

		created = Element('Created', ns = wsu).setText(response['Fecha'])
		expires = Element('Expires', ns = wsu).setText(response['FechaF'])

		timestamp = Element('Timestamp', ns=wsu).setText('')
		timestamp.append(Attribute('wsu:Id', 'Timestamp-2'))

		username_token.insert(username)
		username_token.insert(password)
		username_token.insert(nonce)
		username_token.insert(create)

		timestamp.insert(expires)
		timestamp.insert(created)

		wss_element = Element('Security', ns=wss).insert(timestamp)
		wss_element.insert(username_token)

		return wss_element
