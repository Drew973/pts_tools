import processing

layer = QgsProject.instance().mapLayersByName('data')[0]

#params = { 'INPUT' : layer, 'FIELDS': ['sect_label','subsection_id'] }
params = { 'INPUT' : layer, 'FIELDS': ['SectionID','Sample Unit Id'] }


processing.run('PTS tools:concatenate_fields',params)


