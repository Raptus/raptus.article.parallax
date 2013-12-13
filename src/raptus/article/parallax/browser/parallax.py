from zope import interface, component

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

try: # Plone 4 and higher
    from Products.ATContentTypes.interfaces.image import IATImage
except: # BBB Plone 3
    from Products.ATContentTypes.interface.image import IATImage

from raptus.article.core.config import MANAGE_PERMISSION
from raptus.article.core import interfaces, RaptusArticleMessageFactory as _
from raptus.article.images.interfaces import IImages, IImage


class IParallax(interface.Interface):
    """ Marker interface for the parallax viewlet
    """


class Component(object):
    """ Component which shows the parallax effect of an image
    """
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)

    title = _(u'Parallax effect')
    description = _(u'Images contained in the article are used for a parallax effect.')
    image = '++resource++parallax.gif'
    interface = IParallax
    viewlet = 'raptus.article.parallax'

    def __init__(self, context):
        self.context = context


class Viewlet(ViewletBase):
    """ Viewlet showing the parallax effect of an image
    """
    index = ViewPageTemplateFile('parallax.pt')
    css_class = "parallax"
    component = "parallax"
    thumb_size = "original"
    type = ""

    @property
    @memoize
    def images(self):
        provider = IImages(self.context)
        manageable = interfaces.IManageable(self.context)
        mship = getToolByName(self.context, 'portal_membership')
        if mship.checkPermission(MANAGE_PERMISSION, self.context):
            items = provider.getImages()
        else:
            items = provider.getImages(component=self.component)
        items = manageable.getList(items, self.component)
        i = 0
        l = len(items)
        for item in items:
            img = IImage(item['obj'])
            item.update({'caption': img.getCaption(),
                         'img': img.getImageURL(self.thumb_size),
                         'description': item['brain'].Description})
            if item.has_key('show') and item['show']:
                item['class'] += ' hidden'
            w, h = item['obj'].getSize()
            tw, th = img.getSize(self.thumb_size)
            #if (tw < w and tw > 0) or (th < h and th > 0):
                #item['rel'] = 'lightbox[%s]' % self.css_class
            i += 1
        return items


class IParallaxTeaser(interface.Interface):
    """ Marker interface for the teaser parallax viewlet
    """


class ComponentTeaser(object):
    """ Component which shows the teaser parallax effect of an image
    """
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)

    title = _(u'Teaser parallax effect')
    description = _(u'Images contained in the article are used for a teaser parallax effect.')
    image = '++resource++parallax_teaser.gif'
    interface = IParallaxTeaser
    viewlet = 'raptus.article.parallax.teaser'

    def __init__(self, context):
        self.context = context


class ViewletTeaser(Viewlet):
    """ Viewlet showing the teaser parallax effect of an image
    """

    component = "parallax.teaser"