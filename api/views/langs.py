import requests

from django.conf import settings
from django.views import View
from django import http
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# Cache this for one day
#@method_decorator(cache_page(24 * 60 * 60), name='dispatch')
class TopLangs(View):
    """Fetches, format and and return top user languages."""
    def get(self, request):
        # Builds the query for get the raw data
        query = '''
            query { 
                viewer { 
                    repositories(first:40, orderBy:{field:STARGAZERS, direction:DESC}) {
                        nodes {
                            languages(first:6) {
                                nodes {
                                    name
                                }
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

        data = response.get('data').get('viewer').get('repositories').get('nodes')

        # Counter that stack the number of times each language is used
        user_langs = {}

        for repo in data:
            repo_langs = repo.get('languages').get('nodes')
            for lang in repo_langs:
                name = lang.get('name')
                if (user_langs.get(name)):
                    user_langs[name] += 1
                else:
                    user_langs[name] = 1

        return http.JsonResponse(
            {
                'langs': user_langs
            }
        )