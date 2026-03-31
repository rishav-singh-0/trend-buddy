import unittest

from trend_buddy_shared.contracts.health import HealthResponse


class HealthResponseTest(unittest.TestCase):
    def test_health_contract_shape(self) -> None:
        response = HealthResponse(
            service="strategy-engine",
            status="ok",
            details={"runtime": "python"},
        )

        self.assertEqual(response.service, "strategy-engine")
        self.assertEqual(response.status, "ok")
        self.assertEqual(response.details.get("runtime"), "python")
