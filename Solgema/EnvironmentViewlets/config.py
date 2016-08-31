GLOBALS = globals()

PROJECT_NAME = 'Solgema.EnvironmentViewlets'
from os.path import join
import Globals
PACKAGE_HOME = Globals.package_home(GLOBALS)

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('Solgema.EnvironmentViewlets')

def testMe(txt):
    path_temp_csv = join(PACKAGE_HOME,'out.txt')
    file = open(path_temp_csv, 'a')
    file.write(str(txt))
    file.close()
