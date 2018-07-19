from django.core.exceptions import ValidationError


def clean_text(value):
    """ Creating custom validation to check for 'Due Date:' """
    text = value
    if "Python" not in text:
        raise ValidationError('Missing "Python"')
    return value