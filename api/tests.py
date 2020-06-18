import json

import pytest
from gql import Client
from django.urls import reverse


def test_contribs(client, monkeypatch):
    # Monckeypatch grapjql query
    def mock_execute(query, extra):
        return {
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
                        ]
                    }
                }
            }
        }
    monkeypatch.setattr(Client, 'execute', mock_execute)

    response = client.get(reverse('api-contribs'))

    assert response.status_code == 200
    assert json.loads(response.content) == {
        'total': 1538,
        'start': '2020-06-14T00:00:00.000+00:00',
        'end': '2020-06-15T00:00:00.000+00:00',
        'contribs': [32]
    }

def test_contribs_bad_response(client, monkeypatch):
    # Monckeypatch grapjql query
    def mock_execute(query, extra):
        return {
            'message': 'github generic error'
        }
    monkeypatch.setattr(Client, 'execute', mock_execute)

    response = client.get(reverse('api-contribs'))

    assert response.status_code == 500
