from django.contrib import admin
from entity.models import Entity
from entity.models import Property


class EntityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Entity, EntityAdmin)


class PropertyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Property, PropertyAdmin)
