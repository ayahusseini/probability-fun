"""Descriptors used for validating Fields"""

from numbers import Real
from typing import Any, Callable, Iterable


class Field:
    """
    Base descriptor for validated attributes.

    expected_type : type | tuple[type, ...] | None
        Enforced via isinstance() if provided
    allow_none : bool
        Whether None is permitted as a value
    override_type_validator: bool
        If True, then don't use the Field.validate_type() logic

    validators : Iterable[Callable[[Any, str], None]] | None
        Additional validation functions. Each must raise
        TypeError or ValueError if validation fails.

    preprocessors : Iterable[Callable[[Any, str], Any]] | Any
        Optional preprocessing functions. Must return some value.
    """

    def __init__(
        self,
        *,
        expected_type: type | tuple[type, ...] | None = None,
        allow_none: bool = False,
        override_type_validator: bool = False,
        validators: Iterable[Callable[[Any, str], None]] | None = None,
        preprocessors: Iterable[Callable[[Any, str], Any]] | None = None,
    ):
        self.expected_type = expected_type
        self.allow_none = allow_none
        self.validators = list(validators) if validators else []
        self.preprocessors = list(preprocessors) if preprocessors else []
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
        value = self.preprocess(value)
        self.validate(value)
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        """Delete an attribute name from the instance dictionary"""
        if instance is None:
            return
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

    @staticmethod
    def validate_type(
        value: Any, exp_type: Any, name: str, allow_none: bool
    ) -> None:
        """Raise a TypeError if value is of the wrong type

        - value: Value to validate
        - exp_type: the expected Type
        - name: The name of the variable (used for the error message).
        - allow_none: optionally allow None as a value
        """
        if exp_type is None:
            return

        if value is None:
            if allow_none:
                return
            raise TypeError(f"{name} cannot be None")

        if not isinstance(value, exp_type):
            raise TypeError(
                f"{name} must be of type {exp_type}, "
                f"got {type(value).__name__}"
            )

    def preprocess(self, value) -> Any:
        """
        Preprocess a value
        """
        for preprocessor in self.preprocessors:
            value = preprocessor(value, self.name)
        return value

    def validate(self, value) -> None:
        """
        Runs all validation checks.
        """
        if not self.override_type_validator:
            self.validate_type(
                value,
                exp_type=self.expected_type,
                name=self.name,
                allow_none=self.allow_none,
            )

        for validator in self.validators:
            validator(value, self.name)


class RealNumber(Field):
    @staticmethod
    def preprocess_str_to_real(val, name):
        """Attempt to convert a string to a real number. Returns the
        Preprocessed value. Doesn't raise an error as
        validation is handled elsewhere."""

        if isinstance(val, str):
            try:
                return float(val.replace(" ", ""))
            except ValueError:
                return val
        return val

    def __init__(
        self,
        *,
        allow_none: bool = False,
        validators: Iterable[Callable[[Any, str], None]] = None,
        preprocessors: Iterable[Callable[[Any, str], Any]] | None = None,
        auto_convert: bool = True,
    ):
        if auto_convert:
            preprocessors = [self.preprocess_str_to_real] + (
                preprocessors or []
            )

        super().__init__(
            expected_type=Real,
            allow_none=allow_none,
            validators=validators,
            preprocessors=preprocessors,
        )
