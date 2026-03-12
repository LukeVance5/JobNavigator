from enum import Enum
from pydantic import BaseModel, model_validator, field_validator
from pydantic.fields import Field

class SalaryRate(str, Enum):
    HOURLY = "hourly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class SalaryRange(BaseModel):
    min: int
    max: int
    currency: str
    rate: SalaryRate
    @field_validator("rate", mode="before")
    @classmethod
    def validate_rate(cls, v: str):
        v = v.lower().strip()
        synonyms = {
                "hr": SalaryRate.HOURLY,
                "mo": SalaryRate.MONTHLY,
                "yr": SalaryRate.YEARLY,
                "annually": SalaryRate.YEARLY,
                "annum": SalaryRate.YEARLY,
            }
        return synonyms.get(v, v)

    @model_validator(mode="after")
    def validate_range(self):
        if self.min > self.max:
            raise ValueError("min salary cannot be greater than max salary")
        return self

    