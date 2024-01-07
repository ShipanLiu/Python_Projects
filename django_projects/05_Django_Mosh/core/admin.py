from store.models import Product
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin, ProductImageInline
from tags.models import TaggedItem
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import User


# we need to register a admin model for managing the users
# and we need to extend the "UserAdmin"
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # here we want have possiability to input the email of user:
    # overwrite the "add_fieldsets" from "BaseUserAdmin"
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )






class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem



# this class will inheriate the ProductAdmin from store app
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
