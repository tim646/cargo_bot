from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone_number", "role"]
    list_filter = ["role"]
    search_fields = ["full_name", "phone_number"]

    class Meta:
        model = User
