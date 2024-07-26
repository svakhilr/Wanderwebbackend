from django.contrib import admin
from .models import TripPackage,PackageItnary,TripInclusion,TripExclusion



class  TripItnaryPackageAdmin(admin.TabularInline):
    model = PackageItnary
    extra =0

class TripInclusionAdmin(admin.TabularInline):
    model= TripInclusion
    extra =0

class TripExclusionAdmin(admin.TabularInline):
    model = TripExclusion
    extra = 0

@admin.register(TripPackage)
class TripPackageAdmin(admin.ModelAdmin):
    inlines = [TripItnaryPackageAdmin,TripInclusionAdmin,TripExclusionAdmin]
