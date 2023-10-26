import sys
import runpy


PATH = "./scripts/articles/"
sys.path.append("PATH")

print("Running ARTICLES scripts")
#TODO: Iñigo cambiar las rutas de absolutas a relativas
runpy.run_path(PATH + 'landing_zone.py')
runpy.run_path(PATH + 'formated_zone.py')
runpy.run_path(PATH + 'trusted_zone.py')

print("Running LACIUDADALDIA scripts")
runpy.run_path("scripts/laciudadaldia/landing_zone.py")
runpy.run_path("scripts/laciudadaldia/formatted_zone.py")
runpy.run_path("scripts/laciudadaldia/trusted_zone.py")

print("Running EXPLOITATION ZONE scripts")
runpy.run_path("scripts/exploitation_zone/concept_1.py")
runpy.run_path("scripts/exploitation_zone/concept_2.py")

print("The Data Pipeline run successfully")
