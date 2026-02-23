from .fields import Field
from typing import Callable, Any


class CallableField(Field):
    """Descriptor for validating callables"""

    def __init__(self, *, allow_none=False):
        super().__init__(
            expected_type=Callable,
            allow_none=allow_none,
            # we override to check with callable()
            override_type_validator=True,
            validators=[self._validate_callable],
        )

    @staticmethod
    def _validate_callable(value: Any, name: str) -> None:
        if not callable(value):
            raise TypeError(
                f"{name} must be a callable, got {type(value).__name__}"
            )
