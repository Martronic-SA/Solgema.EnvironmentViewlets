from urllib import quote_plus
from cgi import escape

from zope.interface import implements
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.component.hooks import getSite

from zope.i18n import translate
from zope.i18nmessageid.message import Message

from zope.browsermenu.menu import BrowserMenu
from zope.browsermenu.menu import BrowserSubMenuItem

from plone.memoize.instance import memoize

from Acquisition import aq_inner, aq_base

from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.interface import ISelectableBrowserDefault

from Products.CMFPlone.interfaces.structure import INonStructuralFolder
from Products.CMFPlone.interfaces.constrains import IConstrainTypes
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from interfaces import ISolgemaEnvironmentActionsSubMenuItem
from interfaces import ISolgemaEnvironmentActionsMenu

from Products.CMFPlone import utils

from Solgema.EnvironmentViewlets.config import _

from plone.app.content.browser.folderfactories import _allowedTypes

def _safe_unicode(text):
    if not isinstance(text, unicode):
        text = unicode(text, 'utf-8', 'ignore')
    return text


class SolgemaEnvironmentActionsSubMenuItem(BrowserSubMenuItem):
    implements(ISolgemaEnvironmentActionsSubMenuItem)

    title = _(u'label_solgemaenvironmentactions_menu', default=u'Environment')
    description = _(u'title_solgemaenvironmentactions_menu', default=u'Solgema Environment Actions for the current content item')
    submenuId = 'solgema_environment_actions'

    order = 10
    extra = {'id': 'solgema-environment-actions'}

    def __init__(self, context, request):
        BrowserSubMenuItem.__init__(self, context, request)
        self.context_state = getMultiAdapter((context, request), name='plone_context_state')

    def getToolByName(self, tool):
        return getToolByName(getSite(), tool)

    @property
    def action(self):
        folder = self.context
        if not self.context_state.is_structural_folder():
            folder = utils.parent(self.context)
        return folder.absolute_url() + '/folder_contents'

    @memoize
    def available(self):
        actions_tool = self.getToolByName('portal_actions')
        editActions = actions_tool.listActionInfos(object=aq_inner(self.context), categories=('solgemaenvironment_actions',), max=1)
        return len(editActions) > 0

    def selected(self):
        return False


class SolgemaEnvironmentActionsMenu(BrowserMenu):
    implements(ISolgemaEnvironmentActionsMenu)

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []

        portal_state = getMultiAdapter((context, request), name='plone_portal_state')

        actions_tool = getToolByName(aq_inner(context), 'portal_actions')
        editActions = actions_tool.listActionInfos(object=aq_inner(context), categories=('solgemaenvironment_actions',))

        if not editActions:
            return []

        plone_utils = getToolByName(context, 'plone_utils')
        portal_url = portal_state.portal_url()

        for action in editActions:
            if action['allowed']:
                cssClass = 'actionicon-object_buttons-%s' % action['id']
                icon = plone_utils.getIconFor('object_buttons', action['id'], None)
                if icon:
                    icon = '%s/%s' % (portal_url, icon)

                results.append({ 'title'       : action['title'],
                                 'description' : action['description'],
                                 'action'      : action['url'],
                                 'selected'    : False,
                                 'icon'        : icon,
                                 'extra'       : {'id': action['id'], 'separator': None, 'class': cssClass},
                                 'submenu'     : None,
                                 })

        return results

