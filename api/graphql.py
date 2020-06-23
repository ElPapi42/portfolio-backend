from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from django.conf import settings

# Instaciate a graphql client
client = Client(
    transport=RequestsHTTPTransport(
        url='https://api.github.com/graphql',
        headers={'Authorization': 'bearer {token}'.format(token=settings.GITHUB_TOKEN)},
        verify=False,
        retries=3,
    ),
    fetch_schema_from_transport=True,
)