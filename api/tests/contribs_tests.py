import json

import gql
from django.urls import reverse
"""
from api.graphql import client as graph_client


def test_contribs(client, monkeypatch):
    # Monckeypatch grapjql query
    def mock_execute(query):
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
    monkeypatch.setattr(graph_client, 'execute', mock_execute)

    response = client.get(reverse('api-contribs'))

    assert response.status_code == 200
    assert json.loads(response.content) == {
        'total': 1538,
        'contribs': [32],
        'months': ['Jun']
    }
"""