from django.views import View
from django import http
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from gql import gql
'''
from api.graphql import client as graph_client


# Cache this for one day
@method_decorator(cache_page(24 * 60 * 60), name='dispatch')
class GithubContribs(View):
    """Fetches, format and return github contrib history by month."""
    def get(self, request):
        # Builds the query for get the raw contribution data
        query = gql(
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
                            months {
                                name
                            }
                        }
                    }
                }
            }
        )

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

                # If the day is part of the same month, add to it,
                # else, create a new entry for the new month
                if (self.get_month(day.get('date')) == last_month):
                    contribs[-1] += day_contribs
                else:
                    contribs.append(day_contribs)
                    last_month = self.get_month(day.get('date'))

        # Extract the name of the months in order
        months = []
        for month in data.get('months'):
            months.append(month.get('name'))

        return http.JsonResponse(
            {
                'total': total,
                'contribs': contribs,
                'months': months,
            }
        )

    def get_month(self, date):
        """
        Extract the month from the supplied date.

        Args:
            date (str): From where to extract the month number.
        """
        return date.split('-')[1]
'''