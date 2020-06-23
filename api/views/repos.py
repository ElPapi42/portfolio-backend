from django.views import View
from django import http
from gql import gql

from api.graphql import client as graph_client


class GithubRepos(View):
    """Fetches, format and and return pinned repos."""
    def get(self, request):
        # Builds the query for get the raw pinned repos data
        query = gql('''
            query {
                user(login:"elpapi42") {
                    pinnedItems(first: 6, types: REPOSITORY) {
                        nodes {
                            ... on Repository {
                                name
                                url
                                description
                            }
                        }
                    }
                }
            }
        ''')

        response = graph_client.execute(query)
        data = response.get('user').get('pinnedItems').get('nodes')

        return http.JsonResponse(
            {
                'repos': data 
            }
        )

