"""Descriptor classes building off of Field which restrict Numbers"""

from .fields import RealNumber, Field
from .interval import Interval


class RealNumberWithinInterval(RealNumber):
    def __init__(
        self,
        interval: str | Interval,
        *,
        auto_convert: bool = True,
    ):
        if isinstance(interval, str):
            self.interval = Interval(interval)
        else:
            Field.validate_type(
                interval, Interval, "interval", allow_none=False
            )
            self.interval = interval

        def validate_num_in_interval(value, name):
            if value not in self.interval:
                raise ValueError(
                    f"Required value {name} to be in interval {self.interval}",
                    f"Instead, {name} = {value}",
                )

        super().__init__(
            validators=[validate_num_in_interval],
            preprocessors=[],
            auto_convert=auto_convert,
        )
