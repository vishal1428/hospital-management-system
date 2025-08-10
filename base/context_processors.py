from base import models as base_models

def services_processor(request):
    """
    Context processor to make services available globally in all templates
    """
    services = base_models.Service.objects.all()
    return {'services': services} 