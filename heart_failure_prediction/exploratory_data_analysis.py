from objects import *

importer = Importer()
explorer = Explorer()

data = importer.import_dataset('original_dataset')

explorer.visualize_distribution(data['age'], list_of_plots=['violinplot','qqplot'])
