import sys
PATH = "./scripts/articles/"
sys.path.append("PATH")
import runpy

runpy.run_path(PATH + 'landing_zone.py')
runpy.run_path(PATH + 'formated_zone.py')
runpy.run_path(PATH + 'trusted_zone.py')
