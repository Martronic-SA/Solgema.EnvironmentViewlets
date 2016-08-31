from collective.sendaspdf.interfaces import ISendAsPDFOptionsMaker
from zope.interface import implements

class SendAsPDFAdpater(object):
    implements(ISendAsPDFOptionsMaker)
    
    def __init__(self, context):
        self.context = context
    
    def overrideAll(self):
        return None
    
    def getOptions(self):
        return {'footer-html'    : self.context.absolute_url()+'/@@printfooter',
                'header-html'    : self.context.absolute_url()+'/@@printlogo'}
