# csv2xml.py
# FB - 201010107
# First row of the csv file must be header!

# example CSV file: myData.csv
# id,code name,value
# 36,abc,7.6
# 40,def,3.6
# 9,ghi,6.3
# 76,def,99

import csv

csvFile = 'salida.csv'
xmlFile = 'output_motive_data.xml'

csvData = csv.reader(open(csvFile))
xmlData = open(xmlFile, 'w')
xmlData.write('<?xml version="1.0"  encoding="utf-8"?>' + "\n")
# there must be only one top-level tag
xmlData.write('<openerp>' + "\n" + '<data noupdate="1">' + "\n")

rowNum = 0

#estado = ("azuay","bolivar","canar","carchi","chimborazo","cotopaxi","oro","esmeraldas","galapagos","guayas","imbabura","loja","rios","manabi","morona","napo","orellana","pastaza","pichincha","santa","tsachilas","sucumbios","tungurahua","zamora")

for row in csvData:
    xmlData.write('<record model="output.motive" id="motive_%s">'%str(row[0]) + "\n")
    xmlData.write('<field name="cod_mrl">%s</field>'%row[1] + "\n")
    xmlData.write('<field name="name">%s</field>'%row[2] + "\n")
    xmlData.write('<field name="description"></field>' + "\n")
    xmlData.write('</record>'+ "\n")

xmlData.write("\n" + '</data>' + "\n" + '</openerp>')
xmlData.close()
