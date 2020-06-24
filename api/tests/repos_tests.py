import json
import requests

from django.urls import reverse


class MockResponse():
    def json(self):
        return {
            'data': {
                'user': {
                    'pinnedItems': {
                        'nodes': [
                            {
                                'name': 'deep-deblurring',
                                'url': 'https://github.com/ElPapi42/deep-deblurring',
                                'description': 'Image Deblurring/Restoration Web Application Powered by Deep Learning'
                            }
                        ]
                    }
                }
            }
        } 


def mock_post(*args, **kwargs):
        return MockResponse()


def test_repos(client, monkeypatch):
    # Monckeypatch grapjql query
    monkeypatch.setattr(requests, 'post', mock_post)

    response = client.get(reverse('api-repos'))

    assert response.status_code == 200
    assert json.loads(response.content) == {
        'repos': [
            {
                'name': 'deep-deblurring',
                'url': 'https://github.com/ElPapi42/deep-deblurring',
                'description': 'Image Deblurring/Restoration Web Application Powered by Deep Learning'
            }
        ]
    }
