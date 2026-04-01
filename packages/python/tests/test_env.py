import unittest
from unittest.mock import patch

from trend_buddy_shared.config.env import service_url


class ServiceURLTest(unittest.TestCase):
    def test_service_url_uses_default_compose_address(self) -> None:
        with patch.dict("os.environ", {}, clear=False):
            self.assertEqual(
                service_url("DATABASE_SERVICE_URL", "database-service", 8083),
                "http://database-service:8083",
            )
