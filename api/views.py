from django.shortcuts import render
from django.core.cache import cache
from django.views import View
from django import http
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


# Cache this for one day
@method_decorator(cache_page(24 * 60 * 60), name='dispatch')
class GithubContribs(View):
    """Fetches, format and return github contrib history by week."""
    def get(self, request):

        # Instaciate a graphql client
        graph_client = Client(
            transport=RequestsHTTPTransport(
                url='https://api.github.com/graphql',
                headers={'Authorization': 'bearer {token}'.format(token=settings.GITHUB_TOKEN)},
                verify=False,
                retries=3,
            ),
            fetch_schema_from_transport=True,
        )

        # Builds the query for get the raw contribution data
        query = gql('''
            query { 
                user(login: "elpapi42") {
                    contributionsCollection {
                        contributionCalendar {
                            totalContributions
                            weeks {
                                contributionDays {
                                    contributionCount
                                    date
                                }
                            }
                        }
                    }
                }
            }
        ''')

        response = graph_client.execute(query)
        data = response.get('user').get('contributionsCollection').get('contributionCalendar')

        # Extracts and transforms relevant information from the returned data
        total = data.get('totalContributions')
        start = data.get('weeks')[0].get('contributionDays')[0].get('date')
        end = data.get('weeks')[-1].get('contributionDays')[-1].get('date')

        # Extract the total contribs per week
        contribs = []
        for week in data.get('weeks'):
            week_total = 0
            for day in week.get('contributionDays'):
                week_total += day.get('contributionCount')
            contribs.append(week_total)

        return http.JsonResponse(
            {
                'total': total,
                'start': start,
                'end': end,
                'contribs': contribs,
            }
        )
