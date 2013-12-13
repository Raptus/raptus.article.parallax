from zope import interface, component

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

try: # Plone 4 and higher
    from Products.ATContentTypes.interfaces.image import IATImage
except: # BBB Plone 3
    from Products.ATContentTypes.interface.image import IATImage

from raptus.article.core import interfaces, RaptusArticleMessageFactory as _

class IParallax(interface.Interface):
    """ Marker interface for the teaser left viewlet
    """

class Component(object):
    """ Component which shows the teaser image of an article on the left side
    """
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)

    title = _(u'Image left')
    description = _(u'Image of the article on the left side.')
    image = '++resource++teaser_left.gif'
    interface = IParallax
    viewlet = 'raptus.article.teaser.left'

    def __init__(self, context):
        self.context = context

class Viewlet(ViewletBase):
    """ Viewlet showing the teaser image of an article on the left side
    """
    index = ViewPageTemplateFile('teaser.pt')
    css_class = "componentLeft teaser-left"
    type = "left"







from Acquisition import aq_inner
from zope import interface, component

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

from raptus.article.core import RaptusArticleMessageFactory as _
from raptus.article.core import interfaces
from raptus.article.teaser.interfaces import ITeaser

class ITeaserLeft(interface.Interface):
    """ Marker interface for the teaser left viewlet
    """

class ComponentLeft(object):
    """ Component which shows the teaser image of an article on the left side
    """
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)

    title = _(u'Image left')
    description = _(u'Image of the article on the left side.')
    image = '++resource++teaser_left.gif'
    interface = ITeaserLeft
    viewlet = 'raptus.article.teaser.left'

    def __init__(self, context):
        self.context = context

class ViewletLeft(ViewletBase):
    """ Viewlet showing the teaser image of an article on the left side
    """
    index = ViewPageTemplateFile('teaser.pt')
    css_class = "componentLeft teaser-left"
    type = "left"

    """ if the property are set the caption-text will display below the teaser-image
        as p.dicreet html tag
    """
    @property
    @memoize
    def show_caption(self):
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty('teaser_%s_caption' % self.type, False)

    @property
    @memoize
    def caption(self):
        provider = ITeaser(self.context)
        return provider.getCaption()

    @property
    @memoize
    def caption_non_default(self):
        provider = ITeaser(self.context)
        return provider.getCaption(non_default = True)

    @property
    @memoize
    def image(self):
        provider = ITeaser(self.context)
        return provider.getTeaser(size=self.type)

    @property
    @memoize
    def url(self):
        provider = ITeaser(self.context)
        w, h = self.context.Schema()['image'].getSize(self.context)
        tw, th = provider.getSize(self.type)
        if (not tw or tw >= w) and (not th or th >= h):
            return None
        return provider.getTeaserURL(size="popup")

class ITeaserRight(interface.Interface):
    """ Marker interface for the teaser right viewlet
    """

class ComponentRight(object):
    """ Component which shows the teaser image of an article on the right side
    """
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)

    title = _(u'Image right')
    description = _(u'Image of the article on the right side.')
    image = '++resource++teaser_right.gif'
    interface = ITeaserRight
    viewlet = 'raptus.article.teaser.right'

    def __init__(self, context):
        self.context = context

class ViewletRight(ViewletLeft):
    """ Viewlet showing the teaser image of an article on the right side
    """
    css_class = "componentRight teaser-right"
    type = "right"

class ITeaserFull(interface.Interface):
    """ Marker interface for the teaser full viewlet
    """

class ComponentFull(object):
    """ Component which shows the teaser image of an article over the whole width
    """
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)

    title = _(u'Image')
    description = _(u'Image of the article over the whole width.')
    image = '++resource++teaser_full.gif'
    interface = ITeaserFull
    viewlet = 'raptus.article.teaser.full'

    def __init__(self, context):
        self.context = context

class ViewletFull(ViewletLeft):
    """ Viewlet showing the teaser image of an article over the whole width
    """
    css_class = "componentFull teaser-full"
    type = "full"
