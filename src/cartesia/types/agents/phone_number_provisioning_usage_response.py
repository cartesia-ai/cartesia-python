# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["PhoneNumberProvisioningUsageResponse"]


class PhoneNumberProvisioningUsageResponse(BaseModel):
    """Cartesia-managed phone number provisioning usage for the current month."""

    monthly_limit: Optional[int] = None
    """Maximum phone numbers that can be provisioned during the current month.

    `null` means the plan has no monthly limit.
    """

    monthly_usage: int
    """Number of phone numbers provisioned during the current month.

    This includes active numbers and numbers deleted during the month.
    """

    remaining: Optional[int] = None
    """Phone numbers that can still be provisioned during the current month.

    `null` means the plan has no monthly limit.
    """
