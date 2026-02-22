"""Descriptors used for validating Fields"""

from typing import Any, Callable, Iterable


class Field:
    """
    Base descriptor for validated attributes.

    expected_type : type | tuple[type, ...] | None
        Enforced via isinstance() if provided
    allow_none : bool
        Whether None is permitted as a value
    override_type_validator: bool
        If True, then don't use the Field._validate_type() logic

    validators : Iterable[Callable[[Any, str], None]] | None
        Additional validation functions. Each must raise
        TypeError or ValueError if validation fails.
    """

    def __init__(
        self,
        *,
        expected_type: type | tuple[type, ...] | None = None,
        allow_none: bool = False,
        override_type_validator: bool = False,
        validators: Iterable[Callable[[Any, str], None]] | None = None,
    ):
        self.expected_type = expected_type
        self.allow_none = allow_none
        self.validators = list(validators) if validators else []
        self.override_type_validator = override_type_validator

    def __set_name__(self, owner, name) -> None:
        """Sets the class attribute name"""
        self.name = name

    def __get__(self, instance, owner) -> Any:
        """Retrieves the class attribute, given the instance.
        If the instance is None, then the attribute has been
        accessed on the Class (e.g. ExampleClass.x). In this case,
        return the descriptor itself.

        """
        if instance is None:
            return self

        if self.name not in instance.__dict__:
            raise AttributeError(f"{self.name} has not been set")

        return instance.__dict__.get(self.name)

    def __set__(self, instance, value) -> None:
        """Set an instance attribute to value after validating"""
        self._validate(value)
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        """Delete an attribute name from the instance dictionary"""
        if instance is None:
            return
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

    def _validate_type(self, value) -> None:
        """Raise a TypeError if value is of the wrong type"""
        if self.expected_type is None:
            return

        if value is None:
            if self.allow_none:
                return
            raise TypeError(f"{self.name} cannot be None")

        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be of type {self.expected_type}, "
                f"got {type(value).__name__}"
            )

    def _validate(self, value) -> None:
        """
        Runs all validation checks.
        """
        if not self.override_type_validator:
            self._validate_type(value)

        # Custom validators
        for validator in self.validators:
            validator(value, self.name)
