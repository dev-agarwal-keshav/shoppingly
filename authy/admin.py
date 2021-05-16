from django.contrib import admin
from .models import NewUser, Address

# Register your models here.


@admin.register(NewUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_active",'address')

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "email",
                    "password",
                )
            },
        ),
        ("Personal", {"fields": ("phone",)}),
        ("Important dates", {"fields": ("last_login", "start_date")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )

    def address(self,obj):
        address=Address.objects.filter(user=obj)
        return address[0].address,address[0].state,address[0].pin

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "address","state","pin")
    list_filter=('state','pin',)