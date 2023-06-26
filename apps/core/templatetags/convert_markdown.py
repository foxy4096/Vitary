import markdown
import bleach
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
extensions = [
    "markdown.extensions.admonition",
    "pymdownx.extra",
    "pymdownx.tasklist",
    "pymdownx.magiclink",
    "pymdownx.emoji",
    "pymdownx.details",
    "pymdownx.superfences",
    "markdown.extensions.toc",
]

extension_configs = {
    "pymdownx.tasklist": {
        "custom_checkbox": True,
    },
}


@register.filter(name="convert_markdown", is_safe=True)
@stringfilter
def convert_markdown(value, user=None):
    if user and user.profile.verified:
        return markdown.markdown(
            text=value, extensions=extensions, extension_configs=extension_configs
        )
    return markdown.markdown(
        text=bleach.clean(value),
        extensions=extensions,
        extension_configs=extension_configs,
    )
