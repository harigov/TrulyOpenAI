from abc import ABC, abstractmethod
import json


class SecretManager(ABC):
    @abstractmethod
    def get_secret(self, secret_name):
        raise NotImplementedError()

    @abstractmethod
    def set_secret(self, secret_name, secret):
        raise NotImplementedError()
    

class JsonSecretManager(SecretManager):
    def __init__(self, secrets_file):
        self.secrets_file = secrets_file
        self.secrets = {}
        self._load_secrets()

    def _load_secrets(self):
        with open(self.secrets_file, 'r') as f:
            self.secrets = json.load(f)

    def _save_secrets(self):
        with open(self.secrets_file, 'w') as f:
            json.dump(self.secrets, f)

    def get_secret(self, secret_name):
        return self.secrets.get(secret_name, None)

    def set_secret(self, secret_name, secret):
        self.secrets[secret_name] = secret
        self._save_secrets()
