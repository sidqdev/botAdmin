from django.contrib import admin
from .models import *


admin.site.register(WebUsers)
admin.site.register(Chats)
admin.site.register(WebMessages)
admin.site.register(MessageTypes)
admin.site.register(MessageUpdates)
admin.site.register(HarvestedMessages)




