from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Champion)
admin.site.register(Ability)
admin.site.register(Effect)
admin.site.register(CostType)
admin.site.register(EffectType)
admin.site.register(ScalingType)
