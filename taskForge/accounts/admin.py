from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Profile
from .choices import UserRoleChoices

User = get_user_model()


class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInLine,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_filter = ('profile__role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def get_role(self, obj):
        return obj.profile.get_role_display()

    get_role.short_description = 'Role'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.profile.role == UserRoleChoices.MANAGER:
            obj.is_staff = True
            obj.save()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', )
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    ordering = ('user__username',)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'role':
            if not request.user.is_superuser:
                kwargs['choices'] = [
                    (UserRoleChoices.DEVELOPER, 'Developer'),
                    (UserRoleChoices.END_USER, 'End User')
                ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
