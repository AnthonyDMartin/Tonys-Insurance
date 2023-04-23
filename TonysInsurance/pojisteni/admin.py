from django.contrib import admin
from .models import Customer, Policy, Category, PolicyRecord, Question

admin.site.register(Customer)
admin.site.register(Policy)
admin.site.register(Category)
admin.site.register(PolicyRecord)
admin.site.register(Question)
