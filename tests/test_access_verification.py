from utils.browser import _format_access_verification_error, _looks_like_access_verification


def test_access_verification_detection_matches_agentrouter_slide_page():
	text = (
		'Access Verification For better experience, please slide to complete the verification process '
		'before accessing the web page. Please slide to verify TIME: 2026-07-08 03:32:05'
	)

	assert _looks_like_access_verification(text, 'Verification') is True


def test_access_verification_detection_ignores_normal_login_shell():
	text = 'Sign in with GitHub Email or Username Password'

	assert _looks_like_access_verification(text, 'AgentRouter') is False


def test_access_verification_error_points_to_proxy_configuration():
	message = _format_access_verification_error(
		{'url': 'https://agentrouter.org/login', 'title': 'Verification', 'bodySnippet': 'Access Verification'},
		provider='agentrouter',
	)

	assert 'Access verification page detected for agentrouter' in message
	assert 'CHECKIN_PROXY_URL' in message
	assert 'PROXY_SUBSCRIPTION_URL' in message
