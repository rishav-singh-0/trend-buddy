import unittest

from trend_buddy_shared.contracts.health import HealthResponse


class HealthResponseTest(unittest.TestCase):
    def test_health_contract_shape(self) -> None:
        response = HealthResponse(
            service="backtesting",
            status="ok",
        )

        self.assertEqual(response.service, "backtesting")
        self.assertEqual(response.status, "ok")
        self.assertEqual(response.checks, {})
