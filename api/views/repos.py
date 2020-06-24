import requests

from django.conf import settings
from django.views import View
from django import http
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# Cache this for one day
@method_decorator(cache_page(24 * 60 * 60), name='dispatch')
class GithubRepos(View):
    """Fetches, format and and return pinned repos."""
    def get(self, request):
        # Builds the query for get the raw pinned repos data
        query = '''
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
        '''

        response = requests.post(
            url='https://api.github.com/graphql',
            headers={'Authorization': 'bearer {token}'.format(token=settings.GITHUB_TOKEN)},
            json={'query': query},
        ).json()

        data = response.get('data').get('user').get('pinnedItems').get('nodes')

        return http.JsonResponse(
            {
                'repos': data
            }
        )

