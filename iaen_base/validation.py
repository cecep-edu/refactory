# -*- coding: utf-8 -*-
import re

class Validation:

	def only_numbers(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			if not re.match("^[0-9]+$", record.code_mrl): return False
		return True

	def alphabetical(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			if re.search("[^a-Z, A-Z]", record.name): return False
		return True

	def no_numbers(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			if re.search("[0-9]", record.name): return False
		return True

	def only_letters(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			if not re.match(u"^[ñA-Za-zÁÉÍÓÚáéíóúü\s]+$", record.name): return False
		return True
