import unittest
import delivery_metrics

class TestDeliveryMetrics(unittest.TestCase):

    def test_metrics_definition(self):
        """Verify that Prometheus metrics are properly defined."""
        self.assertIsNotNone(delivery_metrics.total_deliveries)
        self.assertIsNotNone(delivery_metrics.pending_deliveries)
        self.assertIsNotNone(delivery_metrics.on_the_way_deliveries)
        self.assertIsNotNone(delivery_metrics.average_delivery_time)

    def test_simulate_delivery_logic(self):
        """Verify that simulate_delivery generates valid metrics."""
        result = delivery_metrics.simulate_delivery()
        
        # Verify returned dictionary keys
        self.assertIn("total", result)
        self.assertIn("pending", result)
        self.assertIn("on_the_way", result)
        self.assertIn("avg_time", result)

        # Logical bounds verification
        self.assertGreater(result["total"], 0, "Total deliveries should be positive")
        self.assertGreaterEqual(result["pending"], 10, "Pending deliveries must be >= 10")
        self.assertGreaterEqual(result["on_the_way"], 5, "On-the-way deliveries must be >= 5")
        self.assertGreater(result["avg_time"], 0, "Average delivery time must be positive")

        # Verify values assigned to Prometheus Gauges
        self.assertEqual(delivery_metrics.total_deliveries._value.get(), result["total"])
        self.assertEqual(delivery_metrics.pending_deliveries._value.get(), result["pending"])
        self.assertEqual(delivery_metrics.on_the_way_deliveries._value.get(), result["on_the_way"])

    # --------------------------------------------------------------------------
    # FOR STEP 5 (CONTROLLED TEST FAILURE DEMONSTRATION):
    # Uncomment the test below (or change an assert) to fail the build intentionally:
    # --------------------------------------------------------------------------
    def test_controlled_failure_for_demo(self):
        """Intentional test failure to prove Jenkins marks the build as failed."""
        self.assertEqual(1, 2, "Controlled test failure to demonstrate Jenkins failure detection!")

if __name__ == "__main__":
    unittest.main()
