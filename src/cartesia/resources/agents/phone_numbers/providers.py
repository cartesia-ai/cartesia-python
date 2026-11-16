# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, cast
from typing_extensions import Literal, overload

import httpx

from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ...._utils import path_template, required_args, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.agents.phone_numbers import provider_list_params, provider_create_params, provider_update_params
from ....types.agents.phone_numbers.provider_list_response import ProviderListResponse
from ....types.agents.phone_numbers.provider_create_response import ProviderCreateResponse
from ....types.agents.phone_numbers.provider_update_response import ProviderUpdateResponse
from ....types.agents.phone_numbers.provider_retrieve_response import ProviderRetrieveResponse

__all__ = ["ProvidersResource", "AsyncProvidersResource"]


class ProvidersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProvidersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return ProvidersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProvidersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return ProvidersResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        account_sid: str,
        api_key_secret: str,
        api_key_sid: str,
        type: Literal["twilio"],
        label: str | Omit = omit,
        region: Literal["us1", "ie1", "au1"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderCreateResponse:
        """Link a telephony provider account.

        For Twilio, credentials are validated before
        the provider is created. Each account SID + region combination can only be
        linked once. For SIP trunks, configure a trunk with an inbound and/or outbound
        configuration.

        Args:
          account_sid: Your Twilio account SID.

          api_key_secret: The corresponding API key secret.

          api_key_sid: A Twilio API key SID.

          type: Must be `"twilio"`.

          label: An optional human-readable label for the provider.

          region: The Twilio region the phone number and API key are configured for. `us1` (US),
              `ie1` (Ireland), `au1` (Australia). Default is `us1`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderCreateResponse:
        """Link a telephony provider account.

        For Twilio, credentials are validated before
        the provider is created. Each account SID + region combination can only be
        linked once. For SIP trunks, configure a trunk with an inbound and/or outbound
        configuration.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["account_sid", "api_key_secret", "api_key_sid", "type"], ["body"])
    def create(
        self,
        *,
        account_sid: str | Omit = omit,
        api_key_secret: str | Omit = omit,
        api_key_sid: str | Omit = omit,
        type: Literal["twilio"] | Omit = omit,
        label: str | Omit = omit,
        region: Literal["us1", "ie1", "au1"] | Omit = omit,
        body: object | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderCreateResponse:
        return cast(
            ProviderCreateResponse,
            self._post(
                "/agents/phone-numbers/providers",
                body=maybe_transform(
                    {
                        "account_sid": account_sid,
                        "api_key_secret": api_key_secret,
                        "api_key_sid": api_key_sid,
                        "type": type,
                        "label": label,
                        "region": region,
                        "body": body,
                    },
                    provider_create_params.ProviderCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ProviderCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

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
    ) -> ProviderRetrieveResponse:
        """
        Returns the details of a specific provider account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            ProviderRetrieveResponse,
            self._get(
                path_template("/agents/phone-numbers/providers/{id}", id=id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ProviderRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    def update(
        self,
        id: str,
        *,
        api_key_secret: str,
        api_key_sid: str,
        type: Literal["twilio"],
        region: Literal["us1", "ie1", "au1"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderUpdateResponse:
        """Update a provider.

        To ensure assigned numbers are reachable, Twilio credentials
        are validated before saving. If the new credentials are invalid, the request
        fails and returns a list of unreachable numbers currently assigned to agents.
        For SIP trunks, omitted fields remain unchanged. Set `credentials` or
        `destination_country` to `null` to clear that field. Send `[]` to clear an
        inbound allowlist.

        Args:
          api_key_secret: New API key secret.

          api_key_sid: New Twilio API key SID.

          type: Must be `"twilio"`.

          region: The Twilio region the phone number and API key are configured for. `us1` (US),
              `ie1` (Ireland), `au1` (Australia). Default is `us1`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def update(
        self,
        id: str,
        *,
        type: Literal["sip_trunk"],
        inbound: provider_update_params.UpdateSipTrunkProviderBodyInbound | Omit = omit,
        label: str | Omit = omit,
        outbound: provider_update_params.UpdateSipTrunkProviderBodyOutbound | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderUpdateResponse:
        """Update a provider.

        To ensure assigned numbers are reachable, Twilio credentials
        are validated before saving. If the new credentials are invalid, the request
        fails and returns a list of unreachable numbers currently assigned to agents.
        For SIP trunks, omitted fields remain unchanged. Set `credentials` or
        `destination_country` to `null` to clear that field. Send `[]` to clear an
        inbound allowlist.

        Args:
          type: Must be `"sip_trunk"`.

          inbound: Inbound SIP configuration for updating a trunk. Omitted fields remain unchanged.
              Send `[]` to clear an allowlist.

          label: A new human-readable label for the provider. Omit to leave unchanged.

          outbound: Outbound SIP configuration for updating a trunk. `address` and `transport` are
              immutable on an existing outbound trunk, but required when adding outbound to an
              inbound-only provider.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["api_key_secret", "api_key_sid", "type"], ["type"])
    def update(
        self,
        id: str,
        *,
        api_key_secret: str | Omit = omit,
        api_key_sid: str | Omit = omit,
        type: Literal["twilio"] | Literal["sip_trunk"],
        region: Literal["us1", "ie1", "au1"] | Omit = omit,
        inbound: provider_update_params.UpdateSipTrunkProviderBodyInbound | Omit = omit,
        label: str | Omit = omit,
        outbound: provider_update_params.UpdateSipTrunkProviderBodyOutbound | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderUpdateResponse:
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            ProviderUpdateResponse,
            self._patch(
                path_template("/agents/phone-numbers/providers/{id}", id=id),
                body=maybe_transform(
                    {
                        "api_key_secret": api_key_secret,
                        "api_key_sid": api_key_sid,
                        "type": type,
                        "region": region,
                        "inbound": inbound,
                        "label": label,
                        "outbound": outbound,
                    },
                    provider_update_params.ProviderUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ProviderUpdateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        account_sid: str | Omit = omit,
        type: Literal["twilio", "sip_trunk"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderListResponse:
        """List telephony provider accounts linked to your account.

        Supports Twilio and SIP
        Trunk providers.

        Args:
          account_sid: Filter by account SID (Twilio providers only).

          type: Filter by provider type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/agents/phone-numbers/providers",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_sid": account_sid,
                        "type": type,
                    },
                    provider_list_params.ProviderListParams,
                ),
            ),
            cast_to=ProviderListResponse,
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
        Delete a provider account

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
            path_template("/agents/phone-numbers/providers/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncProvidersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProvidersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncProvidersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProvidersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncProvidersResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        account_sid: str,
        api_key_secret: str,
        api_key_sid: str,
        type: Literal["twilio"],
        label: str | Omit = omit,
        region: Literal["us1", "ie1", "au1"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderCreateResponse:
        """Link a telephony provider account.

        For Twilio, credentials are validated before
        the provider is created. Each account SID + region combination can only be
        linked once. For SIP trunks, configure a trunk with an inbound and/or outbound
        configuration.

        Args:
          account_sid: Your Twilio account SID.

          api_key_secret: The corresponding API key secret.

          api_key_sid: A Twilio API key SID.

          type: Must be `"twilio"`.

          label: An optional human-readable label for the provider.

          region: The Twilio region the phone number and API key are configured for. `us1` (US),
              `ie1` (Ireland), `au1` (Australia). Default is `us1`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderCreateResponse:
        """Link a telephony provider account.

        For Twilio, credentials are validated before
        the provider is created. Each account SID + region combination can only be
        linked once. For SIP trunks, configure a trunk with an inbound and/or outbound
        configuration.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["account_sid", "api_key_secret", "api_key_sid", "type"], ["body"])
    async def create(
        self,
        *,
        account_sid: str | Omit = omit,
        api_key_secret: str | Omit = omit,
        api_key_sid: str | Omit = omit,
        type: Literal["twilio"] | Omit = omit,
        label: str | Omit = omit,
        region: Literal["us1", "ie1", "au1"] | Omit = omit,
        body: object | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderCreateResponse:
        return cast(
            ProviderCreateResponse,
            await self._post(
                "/agents/phone-numbers/providers",
                body=await async_maybe_transform(
                    {
                        "account_sid": account_sid,
                        "api_key_secret": api_key_secret,
                        "api_key_sid": api_key_sid,
                        "type": type,
                        "label": label,
                        "region": region,
                        "body": body,
                    },
                    provider_create_params.ProviderCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ProviderCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

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
    ) -> ProviderRetrieveResponse:
        """
        Returns the details of a specific provider account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            ProviderRetrieveResponse,
            await self._get(
                path_template("/agents/phone-numbers/providers/{id}", id=id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ProviderRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    async def update(
        self,
        id: str,
        *,
        api_key_secret: str,
        api_key_sid: str,
        type: Literal["twilio"],
        region: Literal["us1", "ie1", "au1"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderUpdateResponse:
        """Update a provider.

        To ensure assigned numbers are reachable, Twilio credentials
        are validated before saving. If the new credentials are invalid, the request
        fails and returns a list of unreachable numbers currently assigned to agents.
        For SIP trunks, omitted fields remain unchanged. Set `credentials` or
        `destination_country` to `null` to clear that field. Send `[]` to clear an
        inbound allowlist.

        Args:
          api_key_secret: New API key secret.

          api_key_sid: New Twilio API key SID.

          type: Must be `"twilio"`.

          region: The Twilio region the phone number and API key are configured for. `us1` (US),
              `ie1` (Ireland), `au1` (Australia). Default is `us1`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def update(
        self,
        id: str,
        *,
        type: Literal["sip_trunk"],
        inbound: provider_update_params.UpdateSipTrunkProviderBodyInbound | Omit = omit,
        label: str | Omit = omit,
        outbound: provider_update_params.UpdateSipTrunkProviderBodyOutbound | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderUpdateResponse:
        """Update a provider.

        To ensure assigned numbers are reachable, Twilio credentials
        are validated before saving. If the new credentials are invalid, the request
        fails and returns a list of unreachable numbers currently assigned to agents.
        For SIP trunks, omitted fields remain unchanged. Set `credentials` or
        `destination_country` to `null` to clear that field. Send `[]` to clear an
        inbound allowlist.

        Args:
          type: Must be `"sip_trunk"`.

          inbound: Inbound SIP configuration for updating a trunk. Omitted fields remain unchanged.
              Send `[]` to clear an allowlist.

          label: A new human-readable label for the provider. Omit to leave unchanged.

          outbound: Outbound SIP configuration for updating a trunk. `address` and `transport` are
              immutable on an existing outbound trunk, but required when adding outbound to an
              inbound-only provider.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["api_key_secret", "api_key_sid", "type"], ["type"])
    async def update(
        self,
        id: str,
        *,
        api_key_secret: str | Omit = omit,
        api_key_sid: str | Omit = omit,
        type: Literal["twilio"] | Literal["sip_trunk"],
        region: Literal["us1", "ie1", "au1"] | Omit = omit,
        inbound: provider_update_params.UpdateSipTrunkProviderBodyInbound | Omit = omit,
        label: str | Omit = omit,
        outbound: provider_update_params.UpdateSipTrunkProviderBodyOutbound | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderUpdateResponse:
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            ProviderUpdateResponse,
            await self._patch(
                path_template("/agents/phone-numbers/providers/{id}", id=id),
                body=await async_maybe_transform(
                    {
                        "api_key_secret": api_key_secret,
                        "api_key_sid": api_key_sid,
                        "type": type,
                        "region": region,
                        "inbound": inbound,
                        "label": label,
                        "outbound": outbound,
                    },
                    provider_update_params.ProviderUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ProviderUpdateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def list(
        self,
        *,
        account_sid: str | Omit = omit,
        type: Literal["twilio", "sip_trunk"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProviderListResponse:
        """List telephony provider accounts linked to your account.

        Supports Twilio and SIP
        Trunk providers.

        Args:
          account_sid: Filter by account SID (Twilio providers only).

          type: Filter by provider type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/agents/phone-numbers/providers",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "account_sid": account_sid,
                        "type": type,
                    },
                    provider_list_params.ProviderListParams,
                ),
            ),
            cast_to=ProviderListResponse,
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
        Delete a provider account

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
            path_template("/agents/phone-numbers/providers/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ProvidersResourceWithRawResponse:
    def __init__(self, providers: ProvidersResource) -> None:
        self._providers = providers

        self.create = to_raw_response_wrapper(
            providers.create,
        )
        self.retrieve = to_raw_response_wrapper(
            providers.retrieve,
        )
        self.update = to_raw_response_wrapper(
            providers.update,
        )
        self.list = to_raw_response_wrapper(
            providers.list,
        )
        self.delete = to_raw_response_wrapper(
            providers.delete,
        )


class AsyncProvidersResourceWithRawResponse:
    def __init__(self, providers: AsyncProvidersResource) -> None:
        self._providers = providers

        self.create = async_to_raw_response_wrapper(
            providers.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            providers.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            providers.update,
        )
        self.list = async_to_raw_response_wrapper(
            providers.list,
        )
        self.delete = async_to_raw_response_wrapper(
            providers.delete,
        )


class ProvidersResourceWithStreamingResponse:
    def __init__(self, providers: ProvidersResource) -> None:
        self._providers = providers

        self.create = to_streamed_response_wrapper(
            providers.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            providers.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            providers.update,
        )
        self.list = to_streamed_response_wrapper(
            providers.list,
        )
        self.delete = to_streamed_response_wrapper(
            providers.delete,
        )


class AsyncProvidersResourceWithStreamingResponse:
    def __init__(self, providers: AsyncProvidersResource) -> None:
        self._providers = providers

        self.create = async_to_streamed_response_wrapper(
            providers.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            providers.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            providers.update,
        )
        self.list = async_to_streamed_response_wrapper(
            providers.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            providers.delete,
        )
