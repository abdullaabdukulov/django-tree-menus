from django import template
from django.utils.safestring import mark_safe

from apps.menus.models import Menu

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context.get("request")
    if not request:
        return ""

    menu_data = Menu.objects.get_menu_tree(menu_name, request.path)
    if not menu_data:
        return ""

    def render_tree(items, parent_is_active=False):
        if not items:
            return ""

        html = "<ul>"
        for item in items:
            css_class = item.get_css_classes()
            css_attr = f' class="{css_class}"' if css_class else ""
            show_children = item.should_show_children(parent_is_active)

            html += (
                f'<li{css_attr}><a href="{item.get_url()}">{item.title}</a>'
            )

            if item._has_children:
                child_html = render_tree(item._children, item._is_active)
                if not show_children:
                    html += child_html.replace(
                        "<ul>", '<ul style="display: none;">', 1
                    )
                else:
                    html += child_html

            html += "</li>"
        html += "</ul>"
        return html

    return mark_safe(render_tree(menu_data["root_items"]))
