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

        # Extract the total contribs per month
        contribs = []
        last_month = None
        for week in data.get('weeks'):
            week_total = 0
            for day in week.get('contributionDays'):
                day_contribs = day.get('contributionCount')

                if (self.get_month(day.get('date')) == last_month):
                    contribs[-1] += day_contribs
                else:
                    contribs.append(day_contribs)
                    last_month = self.get_month(day.get('date'))

        return http.JsonResponse(
            {
                'total': total,
                'contribs': contribs,
            }
        )

    def get_month(self, date):
        """
        Extract the month from the supplied date.

        Args:
            date (str): From where to extract the month number.
        """
        return date.split('-')[1]