import unittest

import core


class TestCore(unittest.TestCase):
    def setUp(self):
        self.state = core.new_game()
        core.new_batch(self.state, "B1")

    def test_01_no_duplicate_ingredient(self):
        self.assertTrue(core.add_ingredient(self.state, "B1", "麦芽", 10))
        self.assertFalse(core.add_ingredient(self.state, "B1", "麦芽", 10))

    def test_02_no_ferment_when_paused(self):
        self.state["batches"]["B1"]["paused"] = True
        core.ferment(self.state, "B1", 30)
        self.assertEqual(self.state["batches"]["B1"]["stage"], 0)

    def test_03_over_temp_boundary(self):
        self.state["batches"]["B1"]["temp"] = 35
        self.assertEqual(core.check_temp(self.state, "B1"), "over")

    def test_04_no_add_to_locked_batch(self):
        self.state["batches"]["B1"]["locked"] = True
        result = core.add_ingredient(self.state, "B1", "麦芽", 10)
        self.assertFalse(result)

    def test_05_inspect_failure_refunds(self):
        self.state["batches"]["B1"]["defect"] = True
        self.state["batches"]["B1"]["amount"] = 20
        before = self.state["stock"]
        result = core.inspect(self.state, "B1")
        self.assertFalse(result)
        self.assertEqual(self.state["stock"], before + 20)

    def test_06_cancel_order_releases_tank(self):
        core.assign_tank(self.state, "B1", "K1")
        core.cancel_order(self.state, "B1")
        self.assertIsNone(self.state["tanks"]["K1"])

    def test_07_holiday_event_applied_once(self):
        core.holiday_event(self.state, "B1")
        self.assertEqual(self.state["batches"]["B1"]["stage"], 10)

    def test_08_load_preserves_stage(self):
        self.state["batches"]["B1"]["stage"] = 3
        loaded = core.load_state(core.save_state(self.state))
        self.assertEqual(loaded["batches"]["B1"]["stage"], 3)


if __name__ == "__main__":
    unittest.main()
