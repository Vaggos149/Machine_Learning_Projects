import objects
import utils
import settings
# Defining needed Classes
importer = objects.Importer()
explorer = objects.Explorer()
#importing dataset
data = importer.import_dataset('original_dataset')
#renaming columns
data.rename(settings.column_rename_mapping, axis ="columns", inplace=True)