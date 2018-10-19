from collections.abc import Mapping

import requests

BASE_URL = 'https://demo.slashdb.com/'


def retrieve_data(rel_url):
    url = BASE_URL + rel_url
    response = requests.get(url)

    # Throw an exception on HTTP errors (404, 500, etc).
    response.raise_for_status()

    # Parse the response as JSON and return a Python dict.
    return response.json()


def isScalar(value):
    return isinstance(value, (int, str, float, bool))


class APIResponse(Mapping):

    @classmethod
    def fromJSONResponse(cls, response):
        """Create an APIResponse object from existing data."""
        return cls(response=response)
    
    @classmethod
    def fromURL(cls, url):
        """Create an APIResponse object from a relative URL."""
        return cls(url=url)

    @classmethod
    def fromKeys(cls, database, table, resource_id):
        """Create an APIResponse object from a database, table, and id."""
        return cls(database=database, table=table, resource_id=resource_id)

    def __init__(self, **kwargs):

        if kwargs.get('response') is not None:
            self.json_response = kwargs.get('response')

        elif kwargs.get('url') is not None:
            self.__href = kwargs.get('url')
            self.json_response = None

        else:
            database = kwargs.get('database')
            table = kwargs.get('table')
            resource_id = kwargs.get('resource_id')

            self.__href = f'/db/{database}/{table}/{table}Id/{resource_id}.json'
            self.json_response = None

    def __getitem__(self, key):

        self.__load()

        val = self.json_response[key]

        if not (isScalar(val) or isinstance(val, APIResponse)):
            # Check if the attribute is a relationship with other API data
            # If val is a dictionary with only 1 key ('__href'),
            #     then more data is available for download
            if '__href' in val:
                val = APIResponse(url=val['__href'])
                self.json_response[key] = val

        return val

    def __load(self):
        if self.json_response is None:
            self.json_response = retrieve_data(self.__href)
        return None

    def __len__(self):
        self.__load()
        return len(self.json_response)

    def __iter__(self):
        self.__load()
        return iter(self.json_response)

    def __contains__(self, key):
        self.__load()
        return key in self.json_response

    def __repr__(self):
        if self.json_response is None:
            return f'<unfetched APIResponse object>'
        else:
            return '<APIResponse ' + repr(self.json_response) + '>'
