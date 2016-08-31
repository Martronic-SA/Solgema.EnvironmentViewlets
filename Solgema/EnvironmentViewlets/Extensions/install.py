"""
$Id: install.py 2615 2009-05-22 14:42:00Z dholth $
"""
from Acquisition import aq_inner, aq_parent, aq_base
from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.utils import shasattr
from Products.CMFPlone.utils import _createObjectByType
from zope.interface import alsoProvides, directlyProvides, directlyProvidedBy
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.event import notify
from zope.component.hooks import setSite
from zope.component.interfaces import ISite
from zope.component.factory import Factory
from zope.component.interfaces import IFactory
import zope.component
from Products.Five.utilities import marker
from Products.CMFDefault.permissions import ManagePortal

from Solgema.EnvironmentViewlets import interfaces

oldContentsInterfaces = {'Bandeau':interfaces.IBandeauMarker,
               'Logo':interfaces.ILogoMarker,
               'PrintLogo':interfaces.IPrintLogoMarker,}

def install( self, reinstall=False ):
    out = StringIO()
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Solgema.EnvironmentViewlets:default', purge_old=False)
    if not reinstall:
        portal = getToolByName( self, 'portal_url').getPortalObject()
        wftool = getToolByName(portal, 'portal_workflow')
        for oldPortalType in oldContentsInterfaces.keys():
            oldContents = portal.portal_catalog.searchResults({'portal_type':oldPortalType,})
            for oldContent in oldContents:
                bandeau = oldContent.getObject()
                baseid = bandeau.id
                baseimage = bandeau.getImage()
                basetitle = bandeau.pretty_title_or_id()
                basedescription = bandeau.Description()
                basewf = wftool.getInfoFor(bandeau, 'review_state')

                parent = aq_parent(aq_inner(bandeau))

                parent.manage_delObjects(baseid)

                _createObjectByType('Image', parent, id=baseid,
                                title=basetitle,
                                description=basedescription, 
                                image=baseimage, 
                                excludeFromNav=True,
                                excludeFromContent=True,)

                newBandeau = getattr(parent, baseid)
                newBandeau.setLanguage('fr')
                newBandeau.unmarkCreationFlag()
                marker.mark( newBandeau, oldContentsInterfaces[oldPortalType] )
                newBandeau.reindexObject()

                if basewf == 'published':
                    wftool.doActionFor(newBandeau, 'publish')
                if basewf == 'visible':
                    wftool.doActionFor(newBandeau, 'show')

        oldCoordonnees = portal.portal_catalog.searchResults({'portal_type':'Coordonnees'})
        for oldContent in oldCoordonnees:
            bandeau = oldContent.getObject()
            baseiddisplay = bandeau.id
            basedisplay = bandeau.getCoordonnees_display()
            basetitledisplay = bandeau.pretty_title_or_id()+' Affichage'
            baseidprint = bandeau.id+'_print'
            baseprint = bandeau.getCoordonnees_print()
            basetitleprint = bandeau.pretty_title_or_id()+' Impression'
            basedescription = bandeau.Description()
            basewf = wftool.getInfoFor(bandeau, 'review_state')

            parent = aq_parent(aq_inner(bandeau))

            parent.manage_delObjects(baseiddisplay)

            _createObjectByType('Document', parent, id=baseiddisplay,
                            title=basetitledisplay,
                            description=basedescription, 
                            text=basedisplay, 
                            excludeFromNav=True,
                            excludeFromContent=True,)

            _createObjectByType('Document', parent, id=baseidprint,
                            title=basetitleprint,
                            description=basedescription, 
                            text=baseprint, 
                            excludeFromNav=True,
                            excludeFromContent=True,)

            newCoordDisplay = getattr(parent, baseiddisplay)
            newCoordDisplay.setLanguage('fr')
            newCoordDisplay.unmarkCreationFlag()
            marker.mark( newCoordDisplay, interfaces.IFooterMarker )
            newCoordDisplay.reindexObject()

            if basewf == 'published':
                wftool.doActionFor(newCoordDisplay, 'publish')
            if basewf == 'visible':
                wftool.doActionFor(newCoordDisplay, 'show')

            newCoordPrint = getattr(parent, baseidprint)
            newCoordPrint.setLanguage('fr')
            newCoordPrint.unmarkCreationFlag()
            marker.mark( newCoordPrint, interfaces.IPrintFooterMarker )
            newCoordPrint.reindexObject()

            if basewf == 'published':
                wftool.doActionFor(newCoordPrint, 'publish')
            if basewf == 'visible':
                wftool.doActionFor(newCoordPrint, 'show')

def uninstall( self ):
    out = StringIO()

    print >> out, "Removing Solgema Bandeau"

    return out.getvalue()

