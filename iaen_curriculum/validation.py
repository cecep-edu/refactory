# -*- coding: utf-8 -*-
import re

class validation:
	def only_letters(self, cr, uid, ids):
		""" Valida que una cadena contenga únicamente letras, incluyendo tildes y ñ solamente """
		for record in self.browse(cr, uid, ids):
			if not re.match(u"^[ñA-Za-zÁÉÍÓÚáéíóúü\s]+$", record.name): return False
		return True

	def no_numbers(self, cr, uid, ids):
		""" Valida que una cadena de caracteres no contenga dígitos """
		for record in self.browse(cr, uid, ids):
			if re.search("[0-9]", record.name): return False
		return True

	def only_numbers(self, cr, uid, ids):
		""" Valida que una cadena contenga únicamente dígitos. """
		for record in self.browse(cr, uid, ids):
			if not re.match("^[0-9]+$", record.code_mrl): return False
		return True