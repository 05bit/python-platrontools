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

Documentation
=============

Please, read documentation in **docs** dir.

It's brief enough, feedback and questions are welcome.