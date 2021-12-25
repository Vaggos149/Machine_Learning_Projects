from objects import Importer, Explorer
import settings

# Defining needed Classes
importer = Importer()
explorer = Explorer()
#importing dataset
data = importer.import_dataset('original_dataset')
#renaming columns
data.rename(settings.column_rename_mapping, axis ="columns", inplace=True)