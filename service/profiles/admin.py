from django.contrib import admin
from profiles.models import Profile, CategorySkill, Skill

class ProfileInline(admin.TabularInline):
    model = CategorySkill

class CategorySkillInline(admin.TabularInline):
    model = CategorySkill
    extra = 0
    show_change_link = True


# class SkillInline(admin.TabularInline):
#     model = Skill
#     extra = 0
#     fields = ('name', 'level')
#     show_change_link = True

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'rol', 'email', 'id', )
    ordering = ('first_name', 'last_name', 'rol', )
    search_fields = ('first_name', 'last_name', 'rol', 'email',)
    list_display_links = ('first_name', )
    list_filter = ('rol',)
    list_per_page = 10
    inlines = [
            CategorySkillInline
        ]

class CategorySkillAdmin(admin.ModelAdmin):
    list_display = ('name_category', 'profile' )
    ordering = ('name_category', )
    search_fields = ('name_category',)
    list_display_links = ('name_category',)
    list_per_page = 10

    # inlines = [
    #     SkillInline,
    # ]

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',  'level', )
    ordering = ('name', )
    search_fields = ('name', 'level',)
    list_display_links = ('name',)
    list_per_page = 10


admin.site.register(Profile, ProfileAdmin)
admin.site.register(CategorySkill, CategorySkillAdmin)
admin.site.register(Skill, SkillAdmin)