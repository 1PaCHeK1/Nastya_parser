import sentry_sdk
from sentry_sdk.integrations import Integration
from config import get_config, SentrySettings


def init(integrations: list[Integration] | None = None):
    integrations = integrations or []

    config = get_config(SentrySettings)

    sentry_sdk.init(
        dsn=config.dsn,
        traces_sample_rate=config.traces_sample_rate,
        integrations=integrations,
    )
