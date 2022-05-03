from django.contrib import admin
from profiles.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'rol', 'email',)
    ordering = ('first_name', 'last_name', 'rol', )
    search_fields = ('first_name', 'last_name', 'rol', 'email',)
    list_display_links = ('first_name', )
    list_filter = ('rol',)
    list_per_page = 10

admin.site.register(Profile, ProfileAdmin)