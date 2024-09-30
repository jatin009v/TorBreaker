from django.contrib import admin
from .models import Pipeline
from .models import ActiveScan
from .models import Result
from .models import Fingerprint
from .models import NetworkScan
from .models import WhiteBoxResult

admin.site.register(Pipeline)
admin.site.register(ActiveScan)
admin.site.register(Result)
admin.site.register(Fingerprint)
admin.site.register(NetworkScan)
admin.site.register(WhiteBoxResult)
