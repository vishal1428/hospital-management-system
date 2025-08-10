from base import models as base_models

def services_processor(request):
    """
    Context processor to make services available globally in all templates
    """
    try:
        services = base_models.Service.objects.all()
    except:
        services = []
    return {'services': services} 