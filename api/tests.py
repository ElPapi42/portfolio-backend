import json

import pytest
import gql
from django.urls import reverse
from django.test import override_settings
from django.core.cache import cache


def test_contribs(client, monkeypatch):
    # Monckeypatch grapjql query
    class monkey_client():
        def __init__(self, transport, fetch_schema_from_transport):
            pass

        def execute(self, query):
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
    monkeypatch.setattr(gql, 'Client', monkey_client)

    response = client.get(reverse('api-contribs'))

    assert response.status_code == 200
    assert json.loads(response.content) == {
        'total': 1538,
        'start': '2020-06-14T00:00:00.000+00:00',
        'end': '2020-06-15T00:00:00.000+00:00',
        'contribs': [32]
    }



