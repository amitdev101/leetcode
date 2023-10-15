from django.contrib import admin

# Register your models here.
# from django.contrib import admin
from .models import Command  # replace 'YourModel' with the name of your model

class CommandAdmin(admin.ModelAdmin):
    list_display = ('command_text', 'executed', 'timestamp')

admin.site.register(Command, CommandAdmin)

