import sys
import runpy

PATH = "./scripts/"
PATH_ARTICLES = PATH + "articles/"
PATH_LACIUDADALDIA = PATH + "laciudadaldia/"


print("Running ARTICLES scripts")
#TODO: Iñigo cambiar las rutas de absolutas a relativas
runpy.run_path(PATH_ARTICLES + 'landing_zone.py')
runpy.run_path(PATH_ARTICLES + 'formated_zone.py')
runpy.run_path(PATH_ARTICLES + 'trusted_zone.py')

print("Running LACIUDADALDIA scripts")
runpy.run_path(PATH_LACIUDADALDIA +"landing_zone.py")
runpy.run_path(PATH_LACIUDADALDIA + "formatted_zone.py")
runpy.run_path(PATH_LACIUDADALDIA + "trusted_zone.py")

print("Running EXPLOITATION ZONE scripts")
runpy.run_path(PATH + "exploitation_zone/concept_1.py")
runpy.run_path(PATH + "exploitation_zone/concept_2.py")

print("The Data Pipeline run successfully")
