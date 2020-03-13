from django.urls import path
from .views import marcarPonto
from .views import marcacaoRealizada
from .views import confirmarMarcacao
from .views import visualizarMarcacoes
from .views import pontoManual
from .views import marcacaoManual
from .views import export_xls
from .views import pageExportExcel
from .views import filtro_export_xls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', marcarPonto),
    path('marcacaoRealizada', marcacaoRealizada),
    path('confirmarMarcacao', confirmarMarcacao),
    path('marcarPonto', marcarPonto),
    path('visualizarMarcacoes', visualizarMarcacoes),
    path('pontoManual', pontoManual),
    path('marcacaoManual', marcacaoManual),
    path('export_xls', export_xls),
    path('filtro_export_xls', filtro_export_xls),
    path('pageExportExcel', pageExportExcel),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
