"""
Demo Provider - Ephemeral Resource Definitions

Contains:
- DemoSessionToken: Temporary access token for a demo server
"""

import secrets
import time
from datetime import datetime, timedelta, timezone
from typing import ClassVar

import attrs

from pyvider.ephemerals import BaseEphemeralResource, EphemeralResourceContext, register_ephemeral_resource
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_num, a_str, s_resource

from .resources import DemoServer


@attrs.define(frozen=True)
class SessionTokenConfig:
    """Token configuration (from Terraform)."""

    server_id: str
    ttl_seconds: int = 3600


@attrs.define(frozen=True)
class SessionTokenResult:
    """Token data returned to Terraform callers."""

    token: str       # sensitive in schema
    token_id: str
    server_id: str
    expires_at: str


@attrs.define(frozen=True)
class SessionTokenPrivateState(PrivateState):
    """Stored privately so the token can be renewed and revoked."""

    token: str
    token_id: str
    server_id: str
    ttl_seconds: int


@register_ephemeral_resource("session_token")
class DemoSessionToken(BaseEphemeralResource):
    """
    Manages a temporary access token for a demo server.

    Demonstrates:
    - Ephemeral open / renew / close lifecycle
    - Sensitive data in private state
    - Token rotation on renewal
    """

    config_class = SessionTokenConfig
    result_class = SessionTokenResult
    private_state_class = SessionTokenPrivateState

    # In-memory token store — stands in for a real auth API
    _tokens: ClassVar[dict[str, dict]] = {}

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            # Inputs
            "server_id":   a_str(required=True, description="Server to grant access to"),
            "ttl_seconds": a_num(optional=True,  description="Token lifetime in seconds (default 3600)"),
            # Outputs
            "token":       a_str(computed=True, sensitive=True, description="Access token"),
            "token_id":    a_str(computed=True, description="Token identifier"),
            "expires_at":  a_str(computed=True, description="ISO-8601 expiry timestamp"),
        })

    async def validate(self, config: SessionTokenConfig) -> list[str]:
        errors = []
        if config.server_id not in DemoServer._servers:
            errors.append(f"server {config.server_id!r} does not exist")
        if config.ttl_seconds < 60:
            errors.append("ttl_seconds must be at least 60")
        return errors

    async def open(
        self, ctx: EphemeralResourceContext[SessionTokenConfig, None]
    ) -> tuple[SessionTokenResult, SessionTokenPrivateState, datetime]:
        token_id = f"tok-{secrets.token_hex(6)}"
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=ctx.config.ttl_seconds)

        DemoSessionToken._tokens[token_id] = {
            "token": token,
            "server_id": ctx.config.server_id,
            "expires_at": expires_at.isoformat(),
        }

        result = SessionTokenResult(
            token=token,
            token_id=token_id,
            server_id=ctx.config.server_id,
            expires_at=expires_at.isoformat(),
        )
        private = SessionTokenPrivateState(
            token=token,
            token_id=token_id,
            server_id=ctx.config.server_id,
            ttl_seconds=ctx.config.ttl_seconds,
        )
        return result, private, expires_at

    async def renew(
        self, ctx: EphemeralResourceContext[None, SessionTokenPrivateState]
    ) -> tuple[SessionTokenPrivateState, datetime]:
        ps = ctx.private_state
        new_token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=ps.ttl_seconds)

        if ps.token_id in DemoSessionToken._tokens:
            DemoSessionToken._tokens[ps.token_id]["token"] = new_token
            DemoSessionToken._tokens[ps.token_id]["expires_at"] = expires_at.isoformat()

        new_private = SessionTokenPrivateState(
            token=new_token,
            token_id=ps.token_id,
            server_id=ps.server_id,
            ttl_seconds=ps.ttl_seconds,
        )
        return new_private, expires_at

    async def close(
        self, ctx: EphemeralResourceContext[None, SessionTokenPrivateState]
    ) -> None:
        DemoSessionToken._tokens.pop(ctx.private_state.token_id, None)
