

def joinCommand(source,dest,split1,split2,data1,data2):

    c = r'ogr2ogr -f "GPKG" -sql "select split.*, data.* from split left join data '
    c+= r'on split.\"{split1}\"=data.\"{data1}\" and split.\"{split2}\"=data.\"{data2}\""{dest}" "{source}"'

    return c.format(split1=split2,split2=split2,data1=data1,data2=data2,source=source,dest=dest)



#ogr2ogr -f "ESRI Shapefile" -sql "select split.*, data.* from split left join data on split.\"sect_label\"=data.\"SectionID\" and split.\"subsection_id\"=data.\"Sample Unit Id\"" "C:/Users/drew.bennett/Documents/area 14 tool/geopackage approach/joined.shp" "C:/Users/drew.bennett/Documents/area 14 tool/geopackage approach/testImport.gpkg" split


source = r'C:/Users/drew.bennett/Documents/area 14 tool/geopackage approach/testImport.gpkg'
dest = r'C:/Users/drew.bennett/Documents/area 14 tool/geopackage approach/joined.shp'

print(joinCommand(source,dest,split1='sect_label',split2='subsection_id',data1='SectionID',data2='Sample Unit Id'))
