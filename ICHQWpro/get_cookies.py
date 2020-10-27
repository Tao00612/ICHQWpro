import random


def cookies_list():
	cookies_lists = [
		# 'Hqew_SessionId=ldm2lpex3q1h3pspubahpugz',
		'Hqew_SessionId=4oj4ferkdpbgj0jv1wjtryvc'
	]

	return cookies_lists


def get_cookies_dict():
	cookie = cookies_list()
	cookie = random.choice(cookie)
	cookie_dict = {
		c.split('=')[0].strip(): c.split('=')[-1].strip()
		for c in cookie.split(';')
	}
	return cookie_dict
