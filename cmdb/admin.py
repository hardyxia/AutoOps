from django.contrib import admin
from cmdb import models

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from cmdb.models import UserProfile


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','is_staff', 'is_admin')
    list_filter = ('is_admin','is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('堡垒机主机授权', {'fields': ('bind_hosts','host_groups')}),
        ('Permissions', {'fields': ('is_admin','is_staff','user_permissions','groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('user_permissions','groups','bind_hosts','host_groups')

# Now register the new UserAdmin...
admin.site.register(models.UserProfile, UserProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)



class BindUserAdmin(admin.ModelAdmin):
    list_display = ('username','ssh_type','password')


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','user','task_type','content','date']


class TaskLogDetailAdmin(admin.ModelAdmin):
    list_display = ['id','task','bind_host','result','status','start_date','end_date']


admin.site.register(models.InstanceInfo)
admin.site.register(models.InstanceGroup)
admin.site.register(models.BindHost)
admin.site.register(models.BindUser,BindUserAdmin)
admin.site.register(models.IDC)
admin.site.register(models.Region)
# admin.site.register(models.Session)
admin.site.register(models.Task,TaskAdmin)
admin.site.register(models.TaskLogDetail,TaskLogDetailAdmin)

