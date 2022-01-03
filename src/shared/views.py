from django.http import HttpRequest, JsonResponse
from .helpers.postal_codes import postal_code_index

from .forms import PostalCodeForm


def search_postal_code(request: HttpRequest) -> JsonResponse:
    form = PostalCodeForm(request.GET)

    if form.is_valid():
        result = sorted(
            (key, value.decode())
            for key, value in postal_code_index.search(form.cleaned_data["q"])
        )

        if limit := form.cleaned_data["limit"]:
            result = result[:limit]

        return JsonResponse({"result": result})
    return JsonResponse({"error": True, "reason": form.errors}, status=400)
