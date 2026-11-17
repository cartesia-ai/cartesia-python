# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx

from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
from .providers import (
    ProvidersResource,
    AsyncProvidersResource,
    ProvidersResourceWithRawResponse,
    AsyncProvidersResourceWithRawResponse,
    ProvidersResourceWithStreamingResponse,
    AsyncProvidersResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.agents import (
    phone_number_list_params,
    phone_number_import_params,
    phone_number_update_params,
    phone_number_provision_params,
)
from ....types.agents.phone_number import PhoneNumber
from ....types.agents.phone_number_list_response import PhoneNumberListResponse
from ....types.agents.phone_number_provision_response import PhoneNumberProvisionResponse
from ....types.agents.phone_number_provisioning_usage_response import PhoneNumberProvisioningUsageResponse

__all__ = ["PhoneNumbersResource", "AsyncPhoneNumbersResource"]


class PhoneNumbersResource(SyncAPIResource):
    @cached_property
    def providers(self) -> ProvidersResource:
        return ProvidersResource(self._client)

    @cached_property
    def with_raw_response(self) -> PhoneNumbersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return PhoneNumbersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PhoneNumbersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return PhoneNumbersResourceWithStreamingResponse(self)

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumber:
        """
        Returns the details of a specific phone number

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/agents/phone-numbers/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PhoneNumber,
        )

    def update(
        self,
        id: str,
        *,
        agent_id: Optional[str] | Omit = omit,
        label: str | Omit = omit,
        provider: phone_number_update_params.Provider | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumber:
        """
        Update a phone number's label, agent assignment, or provider

        Args:
          agent_id: Assign an agent to answer inbound calls to this number, or `null` to unassign.

          label: A new human-readable name.

          provider: Change the provider. Pass `{ "id": "..." }` for an existing provider, or pass
              Twilio account fields for lookup convenience. For Twilio, the phone number must
              exist in the target provider account. For SIP trunk providers, Cartesia handles
              reassignment between SIP providers. Switching between provider types is not
              supported; delete and re-import the number instead.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            path_template("/agents/phone-numbers/{id}", id=id),
            body=maybe_transform(
                {
                    "agent_id": agent_id,
                    "label": label,
                    "provider": provider,
                },
                phone_number_update_params.PhoneNumberUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PhoneNumber,
        )

    def list(
        self,
        *,
        agent_id: str | Omit = omit,
        ending_before: Optional[str] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        provider_id: str | Omit = omit,
        q: str | Omit = omit,
        starting_after: Optional[str] | Omit = omit,
        type: Literal["twilio", "cartesia", "sip_trunk"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumberListResponse:
        """
        List Phone Numbers

        Args:
          agent_id: Filter by assigned agent ID.

          ending_before: A cursor to use in pagination. `ending_before` is a phone number ID that defines
              your place in the list. For example, if you make a `/agents/phone-numbers`
              request and receive 20 objects, starting with `pn_abc123`, your subsequent call
              can include `ending_before=pn_abc123` to fetch the previous page of the list.

          limit: (Pagination option) The number of phone numbers to return per page, ranging
              between 1 and 100. The default page limit is 10.

          provider_id: Filter by provider ID.

          q: Search by phone number, label, or agent name.

          starting_after: A cursor to use in pagination. `starting_after` is a phone number ID that
              defines your place in the list. For example, if you make a
              `/agents/phone-numbers` request and receive 20 objects, ending with `pn_abc123`,
              your subsequent call can include `starting_after=pn_abc123` to fetch the next
              page of the list.

          type: Filter by provider type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/agents/phone-numbers",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "ending_before": ending_before,
                        "limit": limit,
                        "provider_id": provider_id,
                        "q": q,
                        "starting_after": starting_after,
                        "type": type,
                    },
                    phone_number_list_params.PhoneNumberListParams,
                ),
            ),
            cast_to=PhoneNumberListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete Phone Number

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template("/agents/phone-numbers/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def import_(
        self,
        *,
        label: str,
        number: str,
        provider: phone_number_import_params.Provider,
        agent_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumber:
        """
        Import Phone Number

        Args:
          label: A human-readable name for the phone number.

          number: The phone number in E.164 format.

          provider: Reference to the provider. Pass `{ "id": "..." }` for an existing provider, or
              `{ "type": "twilio", "account_sid": "...", "region": "..." }` to look up by
              account.

          agent_id: Optionally assign an agent to answer inbound calls to this number. Omit to keep
              the number outbound-only.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/agents/phone-numbers",
            body=maybe_transform(
                {
                    "label": label,
                    "number": number,
                    "provider": provider,
                    "agent_id": agent_id,
                },
                phone_number_import_params.PhoneNumberImportParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PhoneNumber,
        )

    def provision(
        self,
        *,
        label: str,
        agent_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumberProvisionResponse:
        """
        Provision a new Cartesia-managed US phone number

        Args:
          label: A human-readable name for the phone number.

          agent_id: Optionally assign an agent to answer inbound calls to this number. Omit to keep
              the number outbound-only.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/agents/phone-numbers/provision",
            body=maybe_transform(
                {
                    "label": label,
                    "agent_id": agent_id,
                },
                phone_number_provision_params.PhoneNumberProvisionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PhoneNumberProvisionResponse,
        )

    def provisioning_usage(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumberProvisioningUsageResponse:
        """
        Returns Cartesia-managed phone number provisioning usage for the current month.
        Active numbers and numbers deleted during the current month count toward usage.
        """
        return self._get(
            "/agents/phone-numbers/provision",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PhoneNumberProvisioningUsageResponse,
        )


class AsyncPhoneNumbersResource(AsyncAPIResource):
    @cached_property
    def providers(self) -> AsyncProvidersResource:
        return AsyncProvidersResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPhoneNumbersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPhoneNumbersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPhoneNumbersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncPhoneNumbersResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumber:
        """
        Returns the details of a specific phone number

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/agents/phone-numbers/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PhoneNumber,
        )

    async def update(
        self,
        id: str,
        *,
        agent_id: Optional[str] | Omit = omit,
        label: str | Omit = omit,
        provider: phone_number_update_params.Provider | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumber:
        """
        Update a phone number's label, agent assignment, or provider

        Args:
          agent_id: Assign an agent to answer inbound calls to this number, or `null` to unassign.

          label: A new human-readable name.

          provider: Change the provider. Pass `{ "id": "..." }` for an existing provider, or pass
              Twilio account fields for lookup convenience. For Twilio, the phone number must
              exist in the target provider account. For SIP trunk providers, Cartesia handles
              reassignment between SIP providers. Switching between provider types is not
              supported; delete and re-import the number instead.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            path_template("/agents/phone-numbers/{id}", id=id),
            body=await async_maybe_transform(
                {
                    "agent_id": agent_id,
                    "label": label,
                    "provider": provider,
                },
                phone_number_update_params.PhoneNumberUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PhoneNumber,
        )

    async def list(
        self,
        *,
        agent_id: str | Omit = omit,
        ending_before: Optional[str] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        provider_id: str | Omit = omit,
        q: str | Omit = omit,
        starting_after: Optional[str] | Omit = omit,
        type: Literal["twilio", "cartesia", "sip_trunk"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumberListResponse:
        """
        List Phone Numbers

        Args:
          agent_id: Filter by assigned agent ID.

          ending_before: A cursor to use in pagination. `ending_before` is a phone number ID that defines
              your place in the list. For example, if you make a `/agents/phone-numbers`
              request and receive 20 objects, starting with `pn_abc123`, your subsequent call
              can include `ending_before=pn_abc123` to fetch the previous page of the list.

          limit: (Pagination option) The number of phone numbers to return per page, ranging
              between 1 and 100. The default page limit is 10.

          provider_id: Filter by provider ID.

          q: Search by phone number, label, or agent name.

          starting_after: A cursor to use in pagination. `starting_after` is a phone number ID that
              defines your place in the list. For example, if you make a
              `/agents/phone-numbers` request and receive 20 objects, ending with `pn_abc123`,
              your subsequent call can include `starting_after=pn_abc123` to fetch the next
              page of the list.

          type: Filter by provider type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/agents/phone-numbers",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "agent_id": agent_id,
                        "ending_before": ending_before,
                        "limit": limit,
                        "provider_id": provider_id,
                        "q": q,
                        "starting_after": starting_after,
                        "type": type,
                    },
                    phone_number_list_params.PhoneNumberListParams,
                ),
            ),
            cast_to=PhoneNumberListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete Phone Number

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template("/agents/phone-numbers/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def import_(
        self,
        *,
        label: str,
        number: str,
        provider: phone_number_import_params.Provider,
        agent_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumber:
        """
        Import Phone Number

        Args:
          label: A human-readable name for the phone number.

          number: The phone number in E.164 format.

          provider: Reference to the provider. Pass `{ "id": "..." }` for an existing provider, or
              `{ "type": "twilio", "account_sid": "...", "region": "..." }` to look up by
              account.

          agent_id: Optionally assign an agent to answer inbound calls to this number. Omit to keep
              the number outbound-only.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/agents/phone-numbers",
            body=await async_maybe_transform(
                {
                    "label": label,
                    "number": number,
                    "provider": provider,
                    "agent_id": agent_id,
                },
                phone_number_import_params.PhoneNumberImportParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PhoneNumber,
        )

    async def provision(
        self,
        *,
        label: str,
        agent_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumberProvisionResponse:
        """
        Provision a new Cartesia-managed US phone number

        Args:
          label: A human-readable name for the phone number.

          agent_id: Optionally assign an agent to answer inbound calls to this number. Omit to keep
              the number outbound-only.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/agents/phone-numbers/provision",
            body=await async_maybe_transform(
                {
                    "label": label,
                    "agent_id": agent_id,
                },
                phone_number_provision_params.PhoneNumberProvisionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PhoneNumberProvisionResponse,
        )

    async def provisioning_usage(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PhoneNumberProvisioningUsageResponse:
        """
        Returns Cartesia-managed phone number provisioning usage for the current month.
        Active numbers and numbers deleted during the current month count toward usage.
        """
        return await self._get(
            "/agents/phone-numbers/provision",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PhoneNumberProvisioningUsageResponse,
        )


class PhoneNumbersResourceWithRawResponse:
    def __init__(self, phone_numbers: PhoneNumbersResource) -> None:
        self._phone_numbers = phone_numbers

        self.retrieve = to_raw_response_wrapper(
            phone_numbers.retrieve,
        )
        self.update = to_raw_response_wrapper(
            phone_numbers.update,
        )
        self.list = to_raw_response_wrapper(
            phone_numbers.list,
        )
        self.delete = to_raw_response_wrapper(
            phone_numbers.delete,
        )
        self.import_ = to_raw_response_wrapper(
            phone_numbers.import_,
        )
        self.provision = to_raw_response_wrapper(
            phone_numbers.provision,
        )
        self.provisioning_usage = to_raw_response_wrapper(
            phone_numbers.provisioning_usage,
        )

    @cached_property
    def providers(self) -> ProvidersResourceWithRawResponse:
        return ProvidersResourceWithRawResponse(self._phone_numbers.providers)


class AsyncPhoneNumbersResourceWithRawResponse:
    def __init__(self, phone_numbers: AsyncPhoneNumbersResource) -> None:
        self._phone_numbers = phone_numbers

        self.retrieve = async_to_raw_response_wrapper(
            phone_numbers.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            phone_numbers.update,
        )
        self.list = async_to_raw_response_wrapper(
            phone_numbers.list,
        )
        self.delete = async_to_raw_response_wrapper(
            phone_numbers.delete,
        )
        self.import_ = async_to_raw_response_wrapper(
            phone_numbers.import_,
        )
        self.provision = async_to_raw_response_wrapper(
            phone_numbers.provision,
        )
        self.provisioning_usage = async_to_raw_response_wrapper(
            phone_numbers.provisioning_usage,
        )

    @cached_property
    def providers(self) -> AsyncProvidersResourceWithRawResponse:
        return AsyncProvidersResourceWithRawResponse(self._phone_numbers.providers)


class PhoneNumbersResourceWithStreamingResponse:
    def __init__(self, phone_numbers: PhoneNumbersResource) -> None:
        self._phone_numbers = phone_numbers

        self.retrieve = to_streamed_response_wrapper(
            phone_numbers.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            phone_numbers.update,
        )
        self.list = to_streamed_response_wrapper(
            phone_numbers.list,
        )
        self.delete = to_streamed_response_wrapper(
            phone_numbers.delete,
        )
        self.import_ = to_streamed_response_wrapper(
            phone_numbers.import_,
        )
        self.provision = to_streamed_response_wrapper(
            phone_numbers.provision,
        )
        self.provisioning_usage = to_streamed_response_wrapper(
            phone_numbers.provisioning_usage,
        )

    @cached_property
    def providers(self) -> ProvidersResourceWithStreamingResponse:
        return ProvidersResourceWithStreamingResponse(self._phone_numbers.providers)


class AsyncPhoneNumbersResourceWithStreamingResponse:
    def __init__(self, phone_numbers: AsyncPhoneNumbersResource) -> None:
        self._phone_numbers = phone_numbers

        self.retrieve = async_to_streamed_response_wrapper(
            phone_numbers.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            phone_numbers.update,
        )
        self.list = async_to_streamed_response_wrapper(
            phone_numbers.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            phone_numbers.delete,
        )
        self.import_ = async_to_streamed_response_wrapper(
            phone_numbers.import_,
        )
        self.provision = async_to_streamed_response_wrapper(
            phone_numbers.provision,
        )
        self.provisioning_usage = async_to_streamed_response_wrapper(
            phone_numbers.provisioning_usage,
        )

    @cached_property
    def providers(self) -> AsyncProvidersResourceWithStreamingResponse:
        return AsyncProvidersResourceWithStreamingResponse(self._phone_numbers.providers)
