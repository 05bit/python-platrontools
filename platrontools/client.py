# -*- coding: utf-8 -*-
import requests
import utils

class Client(object):

	def __init__(self, method='POST', secret=None, merchant_id=None):
		self.method = method
		self.secret = secret
		self.merchant_id = merchant_id

	def create_response(self, data, url):
		return utils.create_response(data, self.secret, url)

	def parse_response(self, xml, url):
		return utils.parse_response(xml, self.secret, url)

	def check_signature(self, data, url):
		return utils.check_signature(data, self.secret, url)

	def init_payment(self, amount, description, user_ip, **optional):
		url = 'https://www.platron.ru/init_payment.php'
		data = {
			'pg_merchant_id': self.merchant_id,
			'pg_amount': amount,
			'pg_description': description,
			'pg_user_ip': user_ip
		}
		for k, v in optional.items():
			data['pg_%s' % k] = v
		return self._send_request(data, url)

	def _send_request(self, data, url):
		request = utils.create_request(data, self.secret, url,
									   method=self.method)
		response = requests.post(url=url, data=request)
		return self.parse_response(unicode(response.text), url=url)
