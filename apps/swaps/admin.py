from django.contrib import admin

from .models import SwapRequest, Swap

admin.site.register(SwapRequest)
admin.site.register(Swap)
