from django.contrib import admin
from .models import Posts, Ratings, TextPost, Shares


admin.site.register(Posts)
admin.site.register(Ratings)
admin.site.register(TextPost)
admin.site.register(Shares)