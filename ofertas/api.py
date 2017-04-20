# coding=utf-8
#!/usr/bin/env python

from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.endpoints import PagesAPIEndpoint

api_router = WagtailAPIRouter('ofertasapi')

api_router.register_endpoint('pages', PagesAPIEndpoint)
