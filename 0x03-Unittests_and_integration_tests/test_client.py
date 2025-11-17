#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient."""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""

        # mock return value
        expected = {"payload": True}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        # ensure get_json was called once with correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        # ensure returned value is what the mock returned
        self.assertEqual(result, expected)
    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns expected URL."""

        mock_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch("client.GithubOrgClient.org", new_callable=property, return_value=mock_payload):
            client = GithubOrgClient("google")
            result = client._public_repos_url

            # assert returned URL is correct
            self.assertEqual(result, mock_payload["repos_url"])
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected list of repos."""

        # Fake JSON payload returned by get_json()
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = mock_payload

        # Mock URL returned by _public_repos_url
        mock_url = "https://api.github.com/orgs/testorg/repos"

        with patch("client.GithubOrgClient._public_repos_url", return_value=mock_url):
            client = GithubOrgClient("testorg")
            result = client.public_repos()

        # Expected list of repo names
        expected = ["repo1", "repo2"]

        self.assertEqual(result, expected)

        # Assertions: both mocks called once
        mock_get_json.assert_called_once_with(mock_url)
        client.GithubOrgClient._public_repos_url  # ensure the attribute is accessed
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean."""
        client = GithubOrgClient("testorg")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)
from parameterized import parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
import requests
from unittest.mock import patch, Mock
from client import GithubOrgClient
import unittest


@parameterized_class([{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "apache2_repos": apache2_repos,
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and configure side_effect."""
        cls.get_patcher = patch("requests.get")

        # Start the patcher and get the mock
        mock_get = cls.get_patcher.start()

        # Define function to return different payloads depending on URL
        def side_effect(url):
            mock_response = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_response.json.return_value = cls.repos_payload
            else:
                raise ValueError(f"Unexpected URL {url}")
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
    def test_public_repos(self):
        """Test that public_repos returns the expected repos."""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering public_repos by license = 'apache-2.0'."""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)



