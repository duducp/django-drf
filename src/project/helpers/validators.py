from django.core.validators import RegexValidator

only_numbers = RegexValidator(
    regex=r'^[0-9]*$',
    message='This field must contain only numbers.'
)

only_letters_and_space = RegexValidator(
    regex=r'^[a-z A-Z]*$',
    message='This field must contain only letters and spaces.'
)
