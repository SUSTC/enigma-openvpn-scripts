# -*- coding: UTF-8 -*-

import os
import json
import urllib, httplib
import urllib2

__VERSION__ = '0.1'
__TIMEOUT__ = 10
__MAX_TRIES__ = 3

def read_config():
	configPath = os.path.dirname(os.path.abspath(__file__)) + "/config.conf"
	if (not os.path.isfile(configPath)):
		print "File config.conf not found"
		os._exit(-1)

	f = open(configPath)
	configContent = f.read()
	config = {}

	try:
		config = json.loads(configContent)
	except Exception:
		print "config parse failed"
		os._exit(-1)

	f.close()

	if not (config['key'] and config['api']):
		print "config error"
		os._exit(-1)

	return config

config = read_config()

def print_err(err):
	if err:
		if (type(err) == urllib2.HTTPError):
			print 'HTTPError = ' + str(err.code)
		elif (type(err) == urllib2.URLError):
			print 'URLError = ' + str(err.reason)
		elif (type(err) == urllib2.URLError):
			print 'HTTPException'
		else:
			import traceback
			print 'Generic Exception: ' + traceback.format_exc()

def urlopen_try(reqURL, data = None):
	content = None
	err = None
	postdata = None
	if data:
		postdata = urllib.urlencode(data)

	i_tries = __MAX_TRIES__
	while (i_tries > 0):
		try:
			if (postdata):
				f = urllib2.urlopen(reqURL, postdata, timeout = __TIMEOUT__)
			else:
				f = urllib2.urlopen(reqURL, timeout = __TIMEOUT__)
			content = f.read()
			err = None
			break
		except urllib2.HTTPError, e:
			err = e
		except urllib2.URLError, e:
			err = e
		except httplib.HTTPException, e:
			err = e
		except Exception, e:
			err = e

		i_tries -= 1

	if err:
		print_err(err)

	return content

def enigma_request(method, data):
	reqURL = config['api'] + method

	data['key'] = config['key']
	content = urlopen_try(reqURL, data)

	if not content:
		return False

	try:
		d = json.loads(content)
	except Exception:
		return False

	return d

def enigma_exit(r):
	if not r:
		os._exit(-1)
	elif type(r['err']) == int:
		if r['err'] != 0:
			if r['message']:
				print r['message']
			os._exit(r['err'])
		else:
			os._exit(0)
	else:
		os._exit(-1)

def enigma_getenv(method):
	env_reads = [ 'username' ]
	allowed_methods = [ 'auth', 'connect', 'disconnect' ]
	if method not in allowed_methods:
		print 'Not an allowed method'
		return False

	if method == 'auth':
		env_reads.append('password')
	else:
		env_reads += [ 'ifconfig_pool_local_ip', 'ifconfig_pool_remote_ip' ]
		if method == 'disconnect':
			env_reads += [ 'bytes_received', 'bytes_sent' ]

	data = {}
	for env in env_reads:
		data[env] = os.environ.get(env)

	return data

def enigma_call(method):
	data = enigma_getenv(method)

	if not data:
		os._exit(-1)
		return

	r = enigma_request(method, data)
	enigma_exit(r)
