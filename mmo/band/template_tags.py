from django import template

register = template.Library()

# Custom filteres are just Python functions that take one or two arguments
# For example, in the filter {{ var|foo:"bar" }}, the filter foo would be passed the variable var and the argument "bar"