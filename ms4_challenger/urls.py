"""
challenger URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from accounts import urls as urls_accounts
from challenges import urls as urls_challenges
from checkout import urls as urls_checkout
from products import urls as urls_products
from submissions import urls as urls_entries
from ratings import urls as urls_ratings
from home.views import index
from django.conf.urls.static import static
from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('accounts/', include(urls_accounts)),
    path('challenges/', include(urls_challenges)),
    path('checkout/', include(urls_checkout)),
    path('products/', include(urls_products)),
    path('submissions/', include(urls_entries)),
    path('ratings/', include(urls_ratings)),

]

