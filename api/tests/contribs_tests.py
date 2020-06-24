import json
import requests

from django.urls import reverse


class MockResponse():
    def json(self):
        return {
            'data': {
                'user': {
                    'contributionsCollection': {
                        'contributionCalendar': {
                            'totalContributions': 1538,
                            'weeks': [
                                {
                                    'contributionDays': [
                                        {
                                            'contributionCount': 29,
                                            'date': '2020-06-14T00:00:00.000+00:00'
                                        },
                                        {
                                            'contributionCount': 3,
                                            'date': '2020-06-15T00:00:00.000+00:00'
                                        }
                                    ]
                                }
                            ],
                            'months': [
                                {
                                'name': 'Jun'
                                },
                            ],
                        }
                    }
                }
            }
        }


def mock_post(*args, **kwargs):
        return MockResponse()


def test_contribs(client, monkeypatch):
    # Monckeypatch grapjql query        
    monkeypatch.setattr(requests, 'post', mock_post)

    response = client.get(reverse('api-contribs'))

    assert response.status_code == 200
    assert json.loads(response.content) == {
        'total': 1538,
        'contribs': [32],
        'months': ['Jun']
    }
