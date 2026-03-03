

"""
Health checker: makes HTTP request to service URI and returns response data.
"""

import requests
import time


def check_service(service: dict) -> dict:
    """
    Perform a health check on the given service.
    Args:
        service (dict): Service definition with keys: name, uri, expected_version, interval_check
    Returns:
        dict: Result containing status, latency, version, and metadata
    """
    uri = service["uri"]
    expected_version = service.get("expected_version")
    start = time.time()

    try:
        resp = requests.get(uri, timeout=5)
        latency = int((time.time() - start) * 1000)
        status = "UP" if resp.status_code == 200 else "DOWN"

        # Try to parse JSON response
        try:
            data = resp.json()
        except ValueError:
            data = {}

        version = data.get("version")
    except Exception as e:
        status, latency, version, data = "DOWN", None, None, {"error": str(e)}

    return {
        "name": service["name"],
        "uri": uri,
        "status": status,
        "latency_ms": latency,
        "version": version,
        "expected_version": expected_version,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "raw_response": data
    }
