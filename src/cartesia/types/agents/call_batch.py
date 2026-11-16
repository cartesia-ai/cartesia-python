# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["CallBatch", "Recipient"]


class Recipient(BaseModel):
    """One recipient within a batch and its current status.

    Returned only on batch detail reads.
    """

    id: str
    """The unique identifier for the recipient within the batch."""

    created_at: datetime
    """When the recipient was queued."""

    status: str
    """The recipient's current status.

    Before dispatch it reflects the queue state; after dispatch it reflects the
    latest call attempt.

    | Status       | Meaning                                                                          |
    | ------------ | -------------------------------------------------------------------------------- |
    | `queued`     | Waiting for the dispatcher                                                       |
    | `dispatched` | Handed to the dialer; no call attempt has connected or finished yet              |
    | `started`    | Call connected and in progress                                                   |
    | `completed`  | Call connected and ended successfully                                            |
    | `failed`     | The call could not be placed (see `error_message`), or the latest attempt failed |
    | `cancelled`  | Batch was cancelled before this recipient was dialed                             |
    """

    to_number: str
    """Destination phone number, in E.164 format (e.g., `+14155559876`)."""

    agent_call_id: Optional[str] = None
    """
    The agent call ID, used to fetch per-call information via
    [Get Call](/api-reference/agents/calls/get-call). Set once the call has been
    dispatched.
    """

    end_reason: Optional[
        Literal[
            "agent_hangup",
            "voicemail_detected",
            "client_hangup",
            "api_cancelled",
            "max_duration",
            "call_inactivity",
            "client_inactivity",
            "client_disconnected",
            "dial_no_answer",
            "dial_busy",
            "dial_failed",
            "dial_timeout",
            "concurrency_limit",
            "agent_error",
            "network_error",
            "config_error",
            "error",
        ]
    ] = None
    """The reason why the call ended."""

    error_message: Optional[str] = None
    """Why the request failed before a call could be placed.

    Returned in place of `agent_call_id` when the recipient never reached a dial
    attempt.
    """


class CallBatch(BaseModel):
    id: str
    """The unique identifier for the batch."""

    agent_id: str
    """The identifier of the agent that handles the batch's calls."""

    created_at: datetime
    """When the batch was created."""

    from_number_id: str
    """The identifier of the phone number the batch dials from."""

    last_updated_at: datetime
    """When the batch was last updated."""

    name: str
    """The batch's label."""

    region: Literal["US", "EU", "APAC"]
    """The region that handles the batch."""

    retry_count: int
    """Number of times the batch has been retried. `0` until the first retry."""

    status: Literal["pending", "in_progress", "completed", "failed", "cancelled"]
    """The batch's lifecycle status, derived at read time from dispatch progress.

    | Status        | Meaning                                    |
    | ------------- | ------------------------------------------ |
    | `pending`     | No calls dispatched yet                    |
    | `in_progress` | Some calls dispatched, not all             |
    | `completed`   | All recipients dispatched                  |
    | `failed`      | All recipients failed before dialing       |
    | `cancelled`   | Cancelled before every call was dispatched |
    """

    target_concurrency_limit: int
    """Maximum number of calls from this batch dialed concurrently."""

    total_calls_dispatched: int
    """
    Recipients handed to the dialer so far, including those that failed before a
    call could be placed.
    """

    total_calls_finished: int
    """
    Recipients whose latest call attempt reached a terminal state (completed or
    failed), including pre-dial failures.
    """

    total_calls_scheduled: int
    """Total recipients queued in the batch."""

    admitted_at: Optional[datetime] = None
    """The actual dispatch time, in RFC3339 UTC format.

    The batch may stay unadmitted in the queue due to scheduling or unavailable
    concurrency.
    """

    recipients: Optional[List[Recipient]] = None
    """The batch's recipients.

    Returned only on `GET /agents/calls/batches/{batch_id}`.
    """

    scheduled_at: Optional[datetime] = None
    """The scheduled dispatch time, in RFC3339 UTC format.

    Omitted for batches that dispatch immediately.
    """
