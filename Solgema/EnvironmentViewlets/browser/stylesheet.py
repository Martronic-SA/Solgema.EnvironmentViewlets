import logging
from Products.Five import BrowserView
from Solgema.EnvironmentViewlets.viewlets.common import BackgroundViewlet

LOG = logging.getLogger('SEV')

class SolgemaEnvironmentViewletsCSS(BrowserView):

    def backgroundsList(self):
        viewlet = BackgroundViewlet(self.context, self.request, self)
        viewlet.update()
        return viewlet.backgroundsList()

    def backgroundClass(self):
        backgrounds = self.backgroundsList()
        LOG.info(backgrounds)
        if not backgrounds:
            return ''
        background = backgrounds[0]
        cssClass = background['cssClass']
        out = 'body {\n'
        out += '    background-image:url('+background['url']+') !important;\n'
        out += '    background-position:'+background['align']+' top !important;\n'
        out += '    background-repeat:'+background['repeat']+' !important;\n'
        if 'backgroundExtend' in cssClass:
            out += '    background-size:cover !important;\n'
        if 'backgroundFixed' in cssClass:
            out += '    background-attachment:fixed !important;\n'
            
        out += '}\n'
        return out

    def __call__(self):
        return"""

"""+self.backgroundClass()
