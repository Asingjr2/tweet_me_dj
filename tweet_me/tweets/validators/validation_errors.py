from django.core.exceptions import ValidationError


def clean_text(value):
    """ Creating custom validation to check for 'Due Date:' """
    text = value
    if "django" not in text:
        raise ValidationError('Missing "Due Date:"')
    return value