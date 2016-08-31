## Script (Python) "atctListAlbum"
##title=Helper method for photo album view
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
try:
    return context.restrictedTraverse('@@body_style')()
except:
    return ''


