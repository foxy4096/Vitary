from django.core.paginator import Paginator


is_htmx_request = lambda request: request.headers.get("HX-Request") == "true"


def paginate(request, qs, limit=5):
    paginated_qs = Paginator(qs, limit, orphans=5)
    page_no = request.GET.get("page")
    return paginated_qs.get_page(page_no)
