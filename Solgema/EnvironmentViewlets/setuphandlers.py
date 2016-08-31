from StringIO import StringIO

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions import StandardModifiers
from Products.CMFEditions.VersionPolicies import ATVersionOnEditPolicy
from Products.CMFPlone.utils import getFSVersionTuple
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.component import adapter, getUtility, getAdapters, getMultiAdapter, getSiteManager

from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.CMFCore import permissions
from zope.component import getUtility, getAdapters
from zope.component import getMultiAdapter
from zope.component import getSiteManager

from plone.portlets.interfaces import IPortletManager
security = ClassSecurityInfo()


from zope.interface.interfaces import IInterface
#from zope.interface.interfaces import InterfaceClass

from Products.CMFCore.permissions import ManagePortal
from plone.browserlayer import utils

from Solgema.EnvironmentViewlets import interfaces
from Products.GenericSetup.interfaces import IProfileImportedEvent

#from Solgema.Immo.Extensions.install import setup_types

def setupSolgemaEnvironmentViewlets(context):
    """various things to do while installing..."""
    if context.readDataFile('solgemaenvironmentviewlets_various.txt') is None:
        return
    site = context.getSite()
    out = StringIO()
    sm = site.getSiteManager()

    setup = getToolByName(site, 'portal_setup')
    if getFSVersionTuple()[0] == 4:
        setup.runAllImportStepsFromProfile('profile-Solgema.EnvironmentViewlets:plone4')
    else:
        setup.runAllImportStepsFromProfile('profile-Solgema.EnvironmentViewlets:plone5')

    print >> out, "Installing Solgema Environment Viewlets Settings Utility"

@adapter(IProfileImportedEvent)
def handleProfileImportedEvent(event):
    context = event.tool
    portal_quickinstaller = getToolByName(context, 'portal_quickinstaller')
    if portal_quickinstaller.isProductInstalled('Solgema.EnvironmentViewlets') and 'to500' in event.profile_id and event.full_import:
        portal_setup = getToolByName(context, 'portal_setup')
        portal_setup.runAllImportStepsFromProfile('profile-Solgema.EnvironmentViewlets:uninstallplone4')
        portal_setup.runAllImportStepsFromProfile('profile-Solgema.EnvironmentViewlets:plone5')
