import logging
from Products.CMFCore.utils import getToolByName

def reinstall(context):
    portal_quickinstaller = getToolByName(context, 'portal_quickinstaller')
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Solgema.PortletsManager:default')

