from django.contrib import admin

from tasks.models import *


class AdminToDo(admin.ModelAdmin):
    list_display = ["id", "add_mark"]

admin.site.register(ToDo,AdminToDo)
    

admin.site.register(Subject)




admin.site.register(Exam)


