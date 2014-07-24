# -*- coding: utf-8 -*-
import re
class Validations:
    def _alphabetical(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			if re.search("[^a-z, A-Z]", record.name): 
				return False
		return True
	def _no_numbers(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			if re.search("[0-9]", record.name):
				return False
		return True
	def _only_letters(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			if not re.match(u"^[ñA-Za-zÁÉÍÓÚáéíóúü\s]+$", record.name):
				return False
		return True
	def _only_numbers(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			if not re.match("^[0-9]+$", record.code_mrl):
				return False
		return True
