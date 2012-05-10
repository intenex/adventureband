from django import template

register = template.Library()

# Custom filteres are just Python functions that take one or two arguments
# For example, in the filter {{ var|foo:"bar" }}, the filter foo would be passed the variable var and the argument "bar"

# ridiculously specialized - find a more general solution later
def print_char_value(char_id, field):
    """ Takes in a character id and returns desired field value """
    character = Character.objects.get(id=char_id)
    return character.field

register.filter('print_char_value', print_char_value)