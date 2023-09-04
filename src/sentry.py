import sentry_sdk
from sentry_sdk.integrations import Integration

from settings import SentrySettings, get_settings


def init(integrations: list[Integration] | None = None):
    integrations = integrations or []

    config = get_settings(SentrySettings)

    sentry_sdk.init(
        dsn=config.dsn,
        traces_sample_rate=config.traces_sample_rate,
        integrations=integrations,
    )
