from Products.CMFCore import DirectoryView

GLOBALS = globals()

ATTR = 'Solgema.EnvironmentViewlets'

DirectoryView.registerDirectory('skins', GLOBALS)

import config

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
