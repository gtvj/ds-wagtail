from django import template

register = template.Library()


@register.inclusion_tag("includes/gtm-datalayer.html", takes_context=True)
def render_gtm_datalayer(context, obj) -> dict:
    """
    Render the datalayer for an instance of a ``DataLayerMixin`` subclass.
    https://developers.google.com/tag-manager/devguide
    """
    try:
        data = obj.get_datalayer_data(context["request"])
    except AttributeError:
        data = {}

    # Add a json serialized version of the data for output
    return {"data": data}
