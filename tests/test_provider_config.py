import json

from utils.config import AccountConfig, AppConfig, ProviderConfig, load_accounts_config


def test_builtin_provider_profile_persistence_defaults(monkeypatch):
	monkeypatch.delenv('PROVIDERS', raising=False)

	config = AppConfig.load_from_env()

	assert config.providers['anyrouter'].persist_profile is True
	assert config.providers['agentrouter'].persist_profile is False


def test_provider_profile_persistence_can_override_builtin(monkeypatch):
	monkeypatch.setenv(
		'PROVIDERS',
		json.dumps(
			{
				'anyrouter': {'domain': 'https://anyrouter.top', 'persist_profile': False},
				'agentrouter': {'domain': 'https://agentrouter.org', 'persist_profile': True},
			}
		),
	)

	config = AppConfig.load_from_env()

	assert config.providers['anyrouter'].persist_profile is False
	assert config.providers['agentrouter'].persist_profile is True


def test_agentrouter_login_url_is_fixed_even_when_provider_overrides_domain(monkeypatch):
	monkeypatch.setenv(
		'PROVIDERS',
		json.dumps({'agentrouter': {'domain': 'https://example.invalid', 'login_path': '/wrong-login'}}),
	)

	config = AppConfig.load_from_env()

	assert config.providers['agentrouter'].login_url() == 'https://agentrouter.org/login'


def test_custom_provider_profile_persistence_defaults_to_false(monkeypatch):
	monkeypatch.setenv('PROVIDERS', json.dumps({'custom': {'domain': 'https://custom.example.com'}}))

	config = AppConfig.load_from_env()

	assert config.providers['custom'].persist_profile is False


def test_provider_from_dict_inherits_profile_persistence_from_defaults():
	defaults = ProviderConfig(name='custom', domain='https://old.example.com', persist_profile=True)

	provider = ProviderConfig.from_dict(
		'custom',
		{'domain': 'https://new.example.com'},
		defaults=defaults,
	)

	assert provider.persist_profile is True


def test_account_defaults_to_agentrouter():
	account = AccountConfig.from_dict({'github_username': 'octocat', 'github_password': 'secret'}, 0)

	assert account.provider == 'agentrouter'
	assert account.has_github_credentials() is True


def test_github_credentials_can_omit_api_user(monkeypatch):
	monkeypatch.setenv(
		'ANYROUTER_ACCOUNTS',
		json.dumps([{'name': 'AgentRouter', 'github_username': 'octocat', 'github_password': 'secret'}]),
	)

	accounts = load_accounts_config()

	assert accounts is not None
	assert accounts[0].provider == 'agentrouter'
	assert accounts[0].has_github_credentials() is True
