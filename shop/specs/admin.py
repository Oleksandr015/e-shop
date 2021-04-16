from django.contrib import admin
from .models import  *

admin.site.registration(ProductFeatures)
admin.site.registration(CategoryFeature)
admin.site.registration(FeatureValidator)


