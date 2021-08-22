from objects import *
# Defining needed Classes
importer = Importer()
explorer = Explorer()
#importing dataset
data = importer.import_dataset('original_dataset')
#renaming columns
data.rename(column_rename_mapping, axis = "columns", inplace=True)