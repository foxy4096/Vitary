from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

IMAGE_FILE_EXTENSION = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
)


@register.filter(name="image_tag", is_safe=True)
@stringfilter
def image_tag(value: str):
    return [
        f'<img src="{text}" class="vit_image" />'
        for text in value.split()
        if text.startswith(("http://", "https://"))
        and any(ext in text for ext in IMAGE_FILE_EXTENSION)
    ]


@register.filter(name="remove_image_link", is_safe=True)
@stringfilter
def remove_image_link(value: str):
    for text in value.split():
        if text.startswith(("http://", "https://")) and any(
            ext in text for ext in IMAGE_FILE_EXTENSION
        ):
            value = value.replace(text, "")
    return value
