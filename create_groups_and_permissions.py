# create_groups_and_permissions.py
import django
from django.contrib.auth.models import Group, Permission
from django.db import models

django.setup()

# Your models
from tasks.models import ToDo, Subject, Student, Exam

# Create a Leader group and assign appropriate permissions
leader_group, created = Group.objects.get_or_create(name='Leader')

# Assign add, change, and delete permissions for all models
for model in [ToDo, Subject, Student, Exam]:
    permissions = Permission.objects.filter(content_type__app_label=model._meta.app_label)
    leader_group.permissions.add(*permissions)
