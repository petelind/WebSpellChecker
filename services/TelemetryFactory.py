
import os

from applicationinsights import TelemetryClient

def create():
    try:
        instrumentation_key = os.environ.get('AIKEY')
        if instrumentation_key is None:
            return None

        tc = TelemetryClient(instrumentation_key)
        return tc
    except Exception as e:
        raise ConnectionError("[ ERROR ] Cannot connect to the telemetry service, check if the instrumentation is "
                              "present in env. variables: " + e)

