import logging
from Acquisition import aq_inner, aq_parent, aq_base
from zope.interface import implements, alsoProvides
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.viewlet.interfaces import IViewlet
from zope.deprecation.deprecation import deprecate
from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode
from Products.ATContentTypes.interface import IATFolder
import sys, os
import Globals

from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import PathBarViewlet as newPathBarViewlet
from plone.app.layout.viewlets.common import PersonalBarViewlet as newPersonalBarViewlet
from plone.app.layout.viewlets.content import DocumentActionsViewlet as newDocumentActionsViewlet
from plone.app.layout.viewlets.content import WorkflowHistoryViewlet as newWorkflowHistoryViewlet
from plone.app.layout.icons.icons import PloneSiteContentIcon as newPloneSiteContentIcon
from plone.app.contentmenu.view import ContentMenuProvider as newContentMenuProvider
from Solgema.EnvironmentViewlets.interfaces import IBackgroundContent
try:
    from plone.app.contenttypes.interfaces import IDocument, IImage
    from plone.namedfile.scaling import ImageScaling
    has_dx = True
except:
    has_dx = False

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile, BoundPageTemplate

from plone.memoize import instance, view, ram
from time import time

from Products.Five import BrowserView
LOG = logging.getLogger('Solgema.EnvironmentViewlets')

class ObjectView(BrowserView):

    def __init__( self, context, request, templatename ):
        self.context = context
        self.request = request
        pt = ViewPageTemplateFile(templatename)
        self.template = BoundPageTemplate(pt, self)

    def __call__(self):
        return self.template()

class BandeauManagerViewlet(ViewletBase):
    index = ViewPageTemplateFile('bandeauManager.pt')

class EnvironmentViewlet(ViewletBase):

    def getItems(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        folder = context_state.folder()
        folder_path = '/'.join(folder.getPhysicalPath())
        itemsBrains = catalog.searchResults(object_provides=self.marker, review_state=['published','visible','',None], sort_on='getObjPositionInParent')
        items = [a for a in itemsBrains if '/'.join(a.getPath().split('/')[0:-1]) in folder_path]
        items_paths = [a.getPath() for a in items]
        items.sort(lambda x, y : cmp (len(x.getPath().split('/')), len(y.getPath().split('/'))))
        items.reverse()
        banners = []
        for item in items:
            if getattr(item, 'stopAcquisitionEnvironment', False):
                banners = []
                parentPath = '/'.join(item.getPath().split('/')[0:-1])
                for nitem in items:
                    if parentPath in nitem.getPath():
                        if getattr(nitem, 'localEnvironment', False) and folder_path != '/'.join(nitem.getPath().split('/')[0:-1]):
                            continue
                        banners.append(aq_inner(nitem))
                    else:
                        break
                break
            elif getattr(item, 'localEnvironment', False) and folder_path != '/'.join(item.getPath().split('/')[0:-1]):
                banners.append(aq_inner(item))
            elif not getattr(item, 'localEnvironment', False):
                banners.append(aq_inner(item)) 
        banners.sort(lambda x, y : cmp (items_paths.index(x.getPath()), items_paths.index(y.getPath())))
        return banners
        
class BandeauViewlet(EnvironmentViewlet):
    index = ViewPageTemplateFile('bandeau.pt')
    marker = 'Solgema.EnvironmentViewlets.interfaces.IBandeauMarker'

    def getSolgemaBandeaux(self):
        bandeaux = self.getItems()
        bandeauxList = []
        base_ajax_content_load = self.request.get('ajax_content_load')
        base_ajax_load = self.request.get('ajax_load')
        setattr(self.request, 'ajax_content_load', 1)
        setattr(self.request, 'ajax_load', 1)
        for bandeau in bandeaux:
            bdict = {}
            if getattr(bandeau, 'image_sizes', None):
                height = str(bandeau.image_sizes['base'][1])
                url = str(bandeau.getPath()+'/image')
                try:
                    title = str(bandeau.Description)
                except:
                    try:
                        title = str(bandeau.Description.encode('utf-8'))
                    except:
                        try:
                            title = str(bandeau.Description.decode('utf-8'))
                        except:
                            title = safe_unicode(bandeau.Description)
                if getattr(bandeau, 'bannerImageLink', ''):
                    link = str(self.context.absolute_url()+'/resolveuid/'+bandeau.bannerImageLink)
                else:
                    link = None
                repeat = getattr(bandeau, 'backgroundRepeat', None)
                if not repeat:
                    repeat = 'no-repeat'
                repeat = str(repeat)
                align = getattr(bandeau, 'backgroundAlign', None)
                if not align:
                    align = 'left'
                align = str(align)
                cssClass = 'bandeau_image'
                cssStyle = 'position:relative;'
                if getattr(bandeau, 'backgroundExtend', False):
                    cssClass += ' backgroundExtend'
                if getattr(bandeau, 'backgroundFixed', False):
                    cssClass += ' backgroundFixed'
                if len(bandeauxList) == 0:
                    cssClass += ' '+bandeau.id.replace('.','_')+' carousel-banner-content selected'
                    cssStyle += ' display:block;'
                else:
                    cssClass += ' '+bandeau.id.replace('.','_')+' carousel-banner-content'
                    cssStyle += ' display:none;'
                
                if link:
                    backgrounddiv = '<a style="display:block; height:%spx; width:100%%; background:transparent url(%s) %s %s top;" title="%s" class="%s" href="%s"></a>' % (height, url, repeat, align, title, cssClass, link)
                else:
                    backgrounddiv = '<div style="height:%spx; width:100%%; background:transparent url(%s) %s %s top;" title="%s" class="%s"></div>' % (height, url, repeat, align, title, cssClass)
#                bandeauxList.append({'id':bandeau.id, 'content':bandeau.tag(title=bandeau.Description())})
                bdict = {'id':bandeau.id, 'content':backgrounddiv, 'cssClass':cssClass, 'cssStyle':cssStyle, 'url':url, 'link':link, 'align':align, 'repeat':repeat}
            else:
                bandeau = bandeau.getObject()
                if (has_dx and IImage.providedBy(bandeau)) or hasattr(bandeau, 'tag'):
                    if hasattr(bandeau, 'getHeight'):
                        height = bandeau.getHeight()
                    else:
                        height = ImageScaling(bandeau, self.request).scale().height
                    if has_dx and IImage.providedBy(bandeau):
                        url = bandeau.absolute_url()
                    else:
                        url = str(bandeau.absolute_url()+'/image')
                    title = bandeau.title
                    bkg = IBackgroundContent(bandeau, None)
                    repeat = getattr(bkg, 'backgroundRepeat', None)
                    if not repeat:
                        repeat = 'no-repeat'
                    align = getattr(bkg, 'backgroundAlign', None)
                    if not align:
                        align = 'left'
                    align = str(align)
                    cssClass = 'bandeau_image'
                    cssStyle = 'position:relative;'
                    if getattr(bkg, 'backgroundExtend', False):
                        cssClass += ' backgroundExtend'
                    if getattr(bkg, 'backgroundFixed', False):
                        cssClass += ' backgroundFixed'
                    if len(bandeauxList) == 0:
                        cssClass += ' '+bandeau.id.replace('.','_')+' carousel-banner-content selected'
                        cssStyle += ' display:block;'
                    else:
                        cssClass += ' '+bandeau.id.replace('.','_')+' carousel-banner-content'
                        cssStyle += ' display:none;'
                    
                    if getattr(bkg, 'bannerImageLink', ''):
                        link = str(self.context.absolute_url()+'/resolveuid/'+bkg.bannerImageLink)
                    else:
                        link = None
                    if link:
                        backgrounddiv = '<a style="display:block; height:%spx; width:100%%; background:transparent url(%s) %s %s top;" title="%s" class="%s" href="%s"></a>' % (height, url, repeat, align, title, cssClass, link)
                    else:
                        backgrounddiv = '<div style="height:%spx; width:100%%; background:transparent url(%s) %s %s top;" title="%s" class="%s"></div>' % (height, url, repeat, align, title, cssClass)
                    bdict = {'id':bandeau.id, 'content':backgrounddiv, 'cssClass':cssClass, 'cssStyle':cssStyle, 'url':url, 'link':link, 'align':align, 'repeat':repeat}
                elif has_dx and IDocument.providedBy(bandeau):
                    bdict['id'] = bandeau.id
                    bdict['content'] = bandeau.text and bandeau.text.raw or ''
                elif hasattr(bandeau, 'getText') and not bandeau.portal_type in ['Topic', 'Collection']:
                    try:
                        bdict['id'] = bandeau.id
                        bdict['content'] = bandeau.getText()
                    except:
                        raise ValueError('error with: '+str(bandeau))
                elif bandeau.portal_type == 'Collage':
                    bdict['id'] = bandeau.id
                    bdict['content'] = ObjectView(bandeau, self.request,'collage_renderer.pt' )
                elif bandeau.portal_type == 'FlashMovie':
                    bdict['id'] = bandeau.id
                    bdict['content'] = ObjectView(bandeau, self.request,'flashmovie_macro_flashobject.pt' )
                elif bandeau.portal_type == 'Folder':
                    bdict['id'] = bandeau.id
                    bdict['content'] = ObjectView(bandeau, self.request,'folder_renderer.pt' )
                else:
                    bdict['id'] = bandeau.id
                    bdict['content'] = bandeau()
            bandeauxList.append(bdict)
        if not base_ajax_content_load:
            delattr(self.request, 'ajax_content_load')
        if not base_ajax_load:
            delattr(self.request, 'ajax_load')
        return bandeauxList

    @view.memoize
    def bandeauxList(self):
        return self.getSolgemaBandeaux()

    def update(self):
        super(BandeauViewlet, self).update()
        self.portal_title = self.portal_state.portal_title()

class FooterManagerViewlet(ViewletBase):
    index = ViewPageTemplateFile('footerManager.pt')

class FooterViewlet(BandeauViewlet):
    index = ViewPageTemplateFile('footer.pt')
    marker = 'Solgema.EnvironmentViewlets.interfaces.IFooterMarker'

    @view.memoize
    def footer(self):
        return self.getSolgemaBandeaux()

class PrintFooterManagerViewlet(ViewletBase):
    index = ViewPageTemplateFile('printfooterManager.pt')

class PrintFooterViewlet(BandeauViewlet):
    index = ViewPageTemplateFile('printfooter.pt')
    marker = 'Solgema.EnvironmentViewlets.interfaces.IPrintFooterMarker'

    @view.memoize
    def printFooter(self):
        return self.getSolgemaBandeaux()

class LogoViewlet(BandeauViewlet):
    index = ViewPageTemplateFile('logo.pt')
    marker = 'Solgema.EnvironmentViewlets.interfaces.ILogoMarker'

    def getItems(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        folder = context_state.folder()
        folder_path = '/'.join(folder.getPhysicalPath())
        itemsBrains = catalog.searchResults(object_provides=self.marker, review_state=['published','visible','',None], sort_on='getObjPositionInParent')
        items = [a for a in itemsBrains if '/'.join(a.getPath().split('/')[0:-1]) in folder_path]
        items_paths = [a.getPath() for a in items]
        items.sort(lambda x, y : cmp (len(x.getPath().split('/')), len(y.getPath().split('/'))))
        items.reverse()
        if items:
            return items[0]
        return []

    def logo(self):
        logo = self.getItems()
        if not logo:
            return None
        if getattr(logo, 'image_sizes', None):
            sizes = logo.image_sizes['base']
            return {'id':logo.getId, 'content':'<img width="%s" height="%s" title="%s" alt="%s" src="%s"/>'%(str(sizes[0]), str(sizes[1]), logo.Description, logo.Title, logo.getPath())}
        else:
            logo = logo.getObject()
            if has_dx and IImage.providedBy(logo):
                return {'id':logo.id, 'content':ImageScaling(logo, self.request).tag(title=logo.Description())}
            elif hasattr(logo, 'tag'):
                return {'id':logo.id, 'content':logo.tag(title=logo.Description())}
            elif has_dx and IDocument.providedBy(logo):
                return {'id':logo.id, 'content':logo.text and logo.text.raw or ''}
            elif hasattr(logo, 'getText'):
                return {'id':logo.id, 'content':logo.getText()}
            elif logo.portal_type == 'FlashMovie':
                return {'id':logo.id, 'content':ObjectView(logo, self.request,'flashmovie_macro_flashobject.pt' )}
        return None

    @view.memoize
    def wholeLogoHTML(self):
        logo = self.logo()
        if not logo:
            return ''
        link = '/Members' in self.request.get('URL') and self.site_url or self.navigation_root_url
        return '<a id="portal-logo" href="%s" accesskey="1" class="visualNoPrint">%s</a>' % (link, logo['content'])

class PrintLogoViewlet(LogoViewlet):
    index = ViewPageTemplateFile('printlogo.pt')
    marker = 'Solgema.EnvironmentViewlets.interfaces.IPrintLogoMarker'

    @view.memoize
    def printLogo(self):
        logo = self.getItems()
        if not logo:
            return None
        if getattr(logo, 'image_sizes', None):
            sizes = logo.image_sizes['base']
            return {'id':logo.getId, 'content':'<img width="%s" height="%s" title="%s" alt="%s" src="%s"/>'%(str(int(int(sizes[0])*0.6)), str(int(int(sizes[1])*0.6)), logo.Description, logo.Title, logo.getPath())}
        else:
            logo = logo.getObject()
            if hasattr(logo, 'tag'):
                img_width, img_height = logo.getField('image').getSize(logo)
                return {'id':logo.id, 'content':logo.tag(title=logo.Description(), width=img_width*0.6, height=img_height*0.6)}
            elif hasattr(logo, 'getText'):
                return {'id':logo.id, 'content':logo.getText()}
            elif logo.portal_type == 'Collage':
                return {'id':logo.id, 'content':ObjectView(logo, self.request,'collage_renderer.pt' )}
        return ''

class BackgroundViewlet(BandeauViewlet):
    index = ViewPageTemplateFile('background.pt')
    marker = 'Solgema.EnvironmentViewlets.interfaces.IBackgroundMarker'

    @view.memoize
    def backgroundsList(self):
        return self.getSolgemaBandeaux()

class PrintFooterPage(BrowserView):
    
    def viewlet(self):
        viewlet = PrintFooterViewlet(self.context, self.request, self)
        viewlet.update()
        return viewlet.render()

class PrintLogoPage(BrowserView):
    
    def viewlet(self):
        viewlet = PrintLogoViewlet(self.context, self.request, self)
        viewlet.update()
        return viewlet.render()
