from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin

from core import models


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('id', 'email', 'nickname', 'password')}),
        (_('Personal Info'), {"fields": ('first_name',
                                         'last_name',
                                         'phone_number')}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            )}
         ),
        (_('Important dates'), {'fields': ('last_login',
                                           'date_joined',
                                           'modified_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ("wide",),
            'fields': (
                'email',
                'nickname',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                )}),
    )
    ordering = ['id']
    list_display = ['email', 'nickname', 'is_staff']
    readonly_fields = ['last_login', 'date_joined', 'modified_at', 'id']


admin.site.register(models.User, UserAdmin)

admin.site.register(models.Country)
admin.site.register(models.County)
admin.site.register(models.City)
admin.site.register(models.Address)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.Favorite)
admin.site.register(models.ChatRoom)
admin.site.register(models.Message)
admin.site.register(models.DirectTransaction)
admin.site.register(models.Review)

admin.site.register(models.Category, DraggableMPTTAdmin)
