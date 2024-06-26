from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ..utils import enviar_alertas_documentos_faltantes

@csrf_exempt
@require_POST
def enviar_alertas_view(request, id_ficha):
    if request.method == 'POST':
        try:
            enviar_alertas_documentos_faltantes(id_ficha)
            return JsonResponse({'message': 'Alertas enviadas correctamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
