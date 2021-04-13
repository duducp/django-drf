import re

from django.core.validators import RegexValidator

from project.helpers.validators import only_letters_and_space, only_numbers


class TestValidators:

    def test_should_validate_parameters_passed_to_regex_when_only_number_called(  # noqa
        self,
    ):
        value = only_numbers
        assert isinstance(value, RegexValidator)
        assert value.regex == re.compile('^[0-9]*$')
        assert value.message == 'This field must contain only numbers.'

    def test_should_validate_parameters_passed_to_regex_when_only_letters_and_space_called(  # noqa
        self
    ):
        value = only_letters_and_space
        assert isinstance(value, RegexValidator)
        assert value.regex == re.compile('^[a-z A-Z]*$')
        assert (
            value.message == 'This field must contain only letters and spaces.'
        )
