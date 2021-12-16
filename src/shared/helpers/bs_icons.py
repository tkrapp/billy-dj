from django.utils.safestring import mark_safe


def bsicon(name: str) -> str:
    return mark_safe(f'<i class="bi-{name}" aria-hidden="true"></i>')
