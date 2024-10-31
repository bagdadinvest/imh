"""
Create or customize your page models here.
"""

from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedWebPage
from modelcluster.fields import ParentalKey


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"


class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["website.EventIndexPage"]
    template = "coderedcms/pages/event_page.html"


class EventIndexPage(CoderedEventIndexPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "website.EventPage"

    # Only allow EventPages beneath this page.
    subpage_types = ["website.EventPage"]

    template = "coderedcms/pages/event_index_page.html"


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class LocationPage(CoderedLocationPage):
    """
    A page that holds a location.  This could be a store, a restaurant, etc.
    """

    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["website.LocationIndexPage"]


class LocationIndexPage(CoderedLocationIndexPage):
    """
    A page that holds a list of locations and displays them with a Google Map.
    This does require a Google Maps API Key in Settings > CRX Settings
    """

    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from coderedcms.models import CoderedWebPage
from wagtail import blocks
from django.db import models

class MasseurPage(CoderedWebPage):
    template = "coderedcms/masseur_page.html"

    # Basic information fields
    name = models.CharField(max_length=255, help_text="Full name of the masseur")
    experience_years = models.CharField(max_length=50, help_text="Experience in years")
    description = RichTextField(blank=True)

    # Contact information
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    whatsapp = models.CharField(max_length=20, blank=True, help_text="WhatsApp contact number")
    user_name = models.CharField(max_length=255, help_text="Name of the profile owner")
    membership_date = models.DateField(help_text="Membership date")
    user_profile_url = models.URLField(blank=True, help_text="URL to view all listings by the user")
    location = models.CharField(max_length=255, blank=True, help_text="Location of the masseur")

    # Image gallery (up to 5 images)
    image_gallery = StreamField([
        ('image', ImageChooserBlock()),
    ], max_num=5, blank=True, help_text="Add up to 5 images for the masseur")

    # Service options
    service_types = StreamField([
        ('service', blocks.CharBlock()),
    ], blank=True, help_text="Types of massages offered")

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('name'),
        FieldPanel('experience_years'),
        FieldPanel('description'),
        FieldPanel('phone'),
        FieldPanel('whatsapp'),
        FieldPanel('user_name'),
        FieldPanel('membership_date'),
        FieldPanel('user_profile_url'),
        FieldPanel('location'),  # Newly added field for location
        FieldPanel('image_gallery'),
        FieldPanel('service_types'),
    ]

    class Meta:
        verbose_name = "Masseur Page"
        verbose_name_plural = "Masseur Pages"


from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from coderedcms.models import CoderedWebPage

class MasseurIndexPage(CoderedWebPage):
    template = "coderedcms/masseur_index_page.html"  # Template to be added later

    # Optional fields for the index page
    intro_text = RichTextField(blank=True, help_text="Introduction text for the Masseur Index Page")
    featured_masseur = models.ForeignKey(
        'MasseurPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Highlight a specific masseur on the index page"
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('intro_text'),
        FieldPanel('featured_masseur'),
    ]

    # Configure allowed subpage types for MasseurIndexPage
    subpage_types = ['MasseurPage']

    # Optional: Custom method to get all MasseurPage children
    def get_masseur_pages(self):
        return MasseurPage.objects.live().descendant_of(self).order_by('-first_published_at')

    class Meta:
        verbose_name = "Masseur Index Page"
        verbose_name_plural = "Masseur Index Pages"
