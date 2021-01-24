from django.contrib import admin
from .models import Profile,Relationship

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass



@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    pass