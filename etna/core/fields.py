from datetime import date
from typing import Optional, Sequence, Union

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .validators import PositiveIntegerStringValidator
from .widgets import DateInputWidget

END_OF_MONTH = "END_OF_MONTH"


class DateInputField(forms.MultiValueField):
    """
    .. _Date input: https://design-system.service.gov.uk/components/date-input/

    Copied from crispy-forms-gds, and extended to support default value substitution
    for individual date segments when only a partial date is entered. We are also
    using a more specific validator for each sub-field to catch any obvious issues
    before attempting to combine the values.

    The original definition can be found at:
    https://github.com/wildfish/crispy-forms-gds/blob/master/src/crispy_forms_gds/fields.py
    """

    widget = DateInputWidget

    def __init__(
        self,
        default_day: Optional[Union[int, str]] = None,
        default_month: Optional[int] = None,
        default_year: Optional[int] = None,
        **kwargs,
    ):
        # Default field values are stored in a 3-item tuple, in an order that
        # corresponds with the field's sub-fields: day, month and year.
        # Values are here may be int or None values, or in the case of `default_day`,
        # an "END_OF_MONTH" could be provided, which substitues a missing day value
        # for the end of the entered/substituted month value.
        self.default_values = (default_day, default_month, default_year)
        if default_day or default_month or default_year:
            kwargs["require_all_fields"] = False
        else:
            kwargs["require_all_fields"] = True

        fields = (
            forms.CharField(
                label=_("Day"),
                error_messages={"incomplete": "Enter the day of the month"},
                validators=[
                    PositiveIntegerStringValidator(
                        min=1,
                        max=31,
                        msg="Entered date must be a real date, for example 23 9 2017.",
                    )
                ],
                required=default_day is None,
            ),
            forms.CharField(
                label=_("Month"),
                error_messages={"incomplete": "Entered date must include a Month."},
                validators=[
                    PositiveIntegerStringValidator(
                        min=1,
                        max=12,
                        msg="Entered date must be a real date, for example 23 9 2017.",
                    )
                ],
                required=default_month is None,
            ),
            forms.CharField(
                label=_("Year"),
                error_messages={"incomplete": "Entered date must include a Year."},
                validators=[
                    PositiveIntegerStringValidator(
                        msg="Entered date must be a real date, for example 23 9 2017."
                    )
                ],
                required=default_year is None,
            ),
        )

        super().__init__(fields=fields, **kwargs)

    def clean(self, value):
        """
        Validate the values entered into the day, month and year fields.

        Validate every value in the given list. A value is validated against
        the corresponding Field in self.fields.

        Normally, all errors are reported at the level of the MultiValueField.
        However the Design System requires that the Error Summary has links to
        tie an error to a specific field. To make that work the ValidationErrors
        for each field (day, month and year) are added to a list on the respective
        widgets as well as the error list on the (bound) field. This was the easiest
        way to get access to the errors for a specific field when the DateInputWidget
        on the MultiValueField is rendered.

        Args:
            value (list, tuple): the values entered into each field. The values are
                in the order the fields are added to the ``fields`` attribute.

        Raises:
            ValidationError: if any of the values fail validation.

        Returns:
             the value converted to a ``date``.

        """
        clean_data = []
        errors = []
        if self.disabled and not isinstance(value, list):
            value = self.widget.decompress(value)

        if not value or isinstance(value, (list, tuple)):
            if not value or not [v for v in value if v not in self.empty_values]:
                # If all sub-field values are empty, don't attempt to fill in any blanks
                if self.required:
                    raise ValidationError(
                        self.error_messages["required"], code="required"
                    )
                else:
                    return self.compress((None, None, None))
        else:
            raise ValidationError(self.error_messages["invalid"], code="invalid")

        for i, field in enumerate(self.fields):
            field.widget.errors = []
            try:
                field_value = value[i]
            except IndexError:
                field_value = None
            if field_value in self.empty_values:
                if self.required and self.require_all_fields:
                    # Raise a 'required' error if the MultiValueField is
                    # required and all sub-fields are required.
                    raise ValidationError(
                        self.error_messages["required"], code="required"
                    )

                if (
                    i == 1
                    and self.default_values[i]
                    and value[0]
                    and value[2]
                    and not value[1]
                ):
                    # Validate empty month input (overrid default month) when day, year are input
                    msg = "Entered date must include a Month."
                    errors.append(msg)
                    # copy the error to the field's widget
                    field.widget.errors.append(msg)
                    continue
                else:
                    if default := self.default_values[i]:
                        # Supplement the missing sub-field value the a default
                        # provided to __init__()
                        if default == END_OF_MONTH:
                            # leave string in-tact to allow handling in compress()
                            clean_data.append(default)                       
                        else:
                            # immitate cleaning by always converting the default
                            # value to an int
                            clean_data.append(int(default))
                        continue  # skip the cleaning step below
                    elif field.required:
                        if field.error_messages["incomplete"] not in errors:
                            # add an 'incomplete' error to the collection
                            errors.append(field.error_messages["incomplete"])
                            # copy the error to the field's widget
                            field.widget.errors.append(
                                field.error_messages["incomplete"]
                            )
                        continue  # skip the cleaning step below
            try:
                clean_data.append(field.clean(field_value))
            except ValidationError as e:
                # add unique validation errors to the collection
                errors.extend(m for m in e.error_list if m not in errors)
                # copy the error to the field's widget
                field.widget.errors.extend(
                    m for m in e.messages if m not in field.widget.errors
                )

        if errors:
            # Raise collected errors all at once
            # Make unique message when using same error message in validators
            m = []
            e = []
            for error in errors:
                if isinstance(error, str):
                    msg = error
                elif isinstance(error, ValidationError):
                    msg = error.message
                if msg not in m:
                    m.append(msg)
                    e.append(error)
            raise ValidationError(e)

        try:
            out = self.compress(clean_data)
        except ValueError:
            # When Day, Month belong to correct range and Year is 0, then error-value "year 0 is out of range"
            msg = "Entered date must be a real date, for example 23 9 2017."
            self.fields[0].widget.errors.append(msg)
            raise ValidationError(msg)

        self.validate(out)
        self.run_validators(out)
        return out

    def compress(self, raw_values: Sequence[str]):
        """
        Convert the entered values into a ``date`` object, or return ``None``
        if no values have been entered or substituted with defaults.
        """
        day, month, year = raw_values

        if not day and not month and not year:
            return None

        # Special handling for 'END_OF_MONTH' day value, which automatically
        # defaults to the end of the user-provided (or substituted) month
        if day == END_OF_MONTH:
            for day in (31, 30, 29, 28):
                try:
                    return date(day=day, month=int(month), year=int(year))
                except ValueError:
                    continue

        return date(day=int(day), month=int(month), year=int(year))
