============
platrontools
============

Platron http://www.platron.ru/ is a Russian electronic payment system. This package provides basic tools for interaction with API.


Usage example
=============

::

	import platrontools
	platron = platrontools.Client(merchant_id=111, secret='qwertyasdf')
	r = platron.init_payment(1.0, 'Test payment', '127.0.0.1')
	print r['pg_status']
	print r['pg_redirect_url']

Client class
============

.. class:: Client(method='POST', secret=None, merchant_id=None)

	Platron API handler class.

	.. method:: init_payment(amount, description, user_ip, **optional)

		Sends request to Platron to initialize new payment.

	.. method:: create_response(data, url)

		Creates XML response by data, with signature.

	.. method:: parse_response(xml, url)

		Parses XML response from Platron.

	.. method:: check_signature(data, url)

		Checks data signature, which is send/received by script
		located at specified ``url``.
