from django.utils.safestring import mark_safe
from django.forms.widgets import Textarea
from apps.core.templatetags.convert_markdown import convert_markdown
from apps.feed.templatetags.mention import user_mention


class MarkdownWidget(Textarea):
    """
    Custom widget for a textarea with HTMX attributes for live Markdown conversion.
    Additionally, it wraps the textarea in a <div> container.

    Args:
        hx_vars (str, optional): The value of the `hx-vars` attribute for HTMX configuration.
        *args: Additional positional arguments passed to the parent class constructor.
        **kwargs: Additional keyword arguments passed to the parent class constructor.

    Attributes:
        hx_vars (str): The value of the `hx-vars` attribute for HTMX configuration.

    Usage:
        This widget can be used to render a textarea with HTMX attributes for live Markdown conversion.

        Example:
        ```
        bio_widget = MarkdownWidget(
            hx_vars="name:'bio'"
        )
        ```
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )
        self.attrs.update(
            {
                "hx-target": "#mdout",
                "hx-trigger": "keyup delay:500ms changed, insertMarkdown",
                "hx-post": "/convert/",
                "style": "font-family: monospace; width: 650px; height: 200px;",
            }
        )

    def render(self, name, value, attrs=None, renderer=None):
        """
        Render the widget.

        Args:
            name (str): The name of the HTML input element.
            value (str): The current value of the input.
            attrs (dict, optional): Additional HTML attributes for the input element.
            renderer (str, optional): The renderer for rendering the widget.

        Returns:
            str: The HTML rendering of the widget.
        """
        attrs.update({"hx-vars": f"name:'{name}'", "id": f"id_{name}"})
        rendered_textarea = super().render(name, value, attrs)
        initials = user_mention(convert_markdown(value or ""))
        div_element = f'<div class="content" id="mdout">{initials}</div>'
        return mark_safe(f"<div>{rendered_textarea} {div_element}</div>")
