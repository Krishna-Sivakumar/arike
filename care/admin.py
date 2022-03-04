from django.contrib import admin
import care.models

# Register your models here.

admin.site.register(care.models.State)
admin.site.register(care.models.District)
admin.site.register(care.models.LSGBody)
admin.site.register(care.models.Ward)
admin.site.register(care.models.Facility)
admin.site.register(care.models.Patient)
admin.site.register(care.models.FamilyDetails)
admin.site.register(care.models.Disease)
admin.site.register(care.models.PatientDisease)
admin.site.register(care.models.VisitSchedule)
admin.site.register(care.models.VisitDetails)
admin.site.register(care.models.Treatment)
admin.site.register(care.models.TreatmentNotes)
admin.site.register(care.models.TemporaryLink)
