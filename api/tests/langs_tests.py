import json
import requests

from django.urls import reverse


class MockResponse():
    def json(self):
        return {
            'data': {
                'viewer': {
                    'repositories': {
                        'nodes': [
                            {
                                'languages': {
                                    'nodes': [
                                        {
                                        'name': 'Python'
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        } 


def mock_post(*args, **kwargs):
        return MockResponse()


def test_langs(client, monkeypatch):
    # Monckeypatch grapjql query
    monkeypatch.setattr(requests, 'post', mock_post)

    response = client.get(reverse('api-langs'))

    assert response.status_code == 200
    assert json.loads(response.content) == {
        'langs': ['Python'],
        'ocurrences': [1]
    }
