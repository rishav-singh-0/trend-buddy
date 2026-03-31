import unittest

from trend_buddy_shared.contracts.health import HealthResponse


class HealthResponseTest(unittest.TestCase):
    def test_health_contract_shape(self) -> None:
        response = HealthResponse(
            service="portfolio-analytics",
            status="ok",
            details={"runtime": "python"},
        )

        self.assertEqual(response.service, "portfolio-analytics")
        self.assertEqual(response.status, "ok")
        self.assertIn("runtime", response.details)
        self.assertEqual(response.details["runtime"], "python")
