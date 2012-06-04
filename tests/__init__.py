import sys
import unittest
from platrontools import utils
from platrontools import client
from . import config

XML_RESULT = """<?xml version="1.0" encoding="utf-8"?>
<request>
<pg_salt>fedcf333</pg_salt>
<pg_order_id>37</pg_order_id>
<pg_payment_id>3120286</pg_payment_id>
<pg_payment_system>TEST</pg_payment_system>
<pg_amount>400.0000</pg_amount>
<pg_net_amount>400</pg_net_amount>
<pg_currency>RUR</pg_currency>
<pg_ps_currency>RUR</pg_ps_currency>
<pg_ps_amount>400</pg_ps_amount>
<pg_ps_full_amount>400.00</pg_ps_full_amount>
<pg_result>1</pg_result>
<pg_can_reject>0</pg_can_reject>
<pg_payment_date>2012-05-29 11:52:31</pg_payment_date>
<pg_user_phone>79688676293</pg_user_phone>
<pg_description></pg_description>
<pg_sig>2558cc22c124ef0dd0f0c1a939e26d4b</pg_sig>
</request>
"""

class TestRequest(unittest.TestCase):
    def setUp(self):
        self.client = client.Client(secret=config.SECRET,
                                    merchant_id=config.MERCHANT_ID)

    @unittest.skipIf(not config.MERCHANT_ID,
                     "config.MERCHANT_ID is not defined")
    def test_init_payment(self):
        r = self.client.init_payment(1.0, 'Test', '127.0.0.1')
        print r
        self.assertTrue(not r is None)

    def test_parse_response(self):
        r = self.client.parse_response(XML_RESULT, url='')
        # print r
        self.assertTrue(not r is None)

if __name__ == '__main__':
    unittest.main()