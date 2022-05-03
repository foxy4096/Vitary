from .models import DocumentationCategory

def get_documentation_categories(request):
    """
    Returns the Documentation Categories
    """
    return {"doc_category": DocumentationCategory.objects.all()}