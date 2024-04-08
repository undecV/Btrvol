"""Testcases for configuration."""

import unittest
import pickle
import logging


from .configuration import BtrvolConfiguration


logging.basicConfig(format="%(message)s")
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


class BtrvolConfigurationTest(unittest.TestCase):
    def test_btrvol_configuration(self) -> None:
        configuration_1 = BtrvolConfiguration()
        print(vars(configuration_1))

    def test_btrvol_configuration_dump(self) -> None:
        configuration: BtrvolConfiguration = BtrvolConfiguration()
        dumped: bytes = pickle.dumps(configuration)
        loaded: bytes = pickle.loads(dumped)
        log.debug("configuration: %r", vars(configuration))
        log.debug("loaded: %r", vars(loaded))
        self.assertEqual(vars(configuration), vars(loaded))


if __name__ == "__main__":
    unittest.main()
