# -*- coding: utf-8 -*-
import re

class Validations:
    def _alphabetical(self, cr, uid, ids):
		for record in self.browse(cr, uid, ids):
			if re.search("[^a-z, A-Z]", record.name): return False
		return True 
