from collections.abc import Mapping

import requests

BASE_URL = 'https://demo.slashdb.com/'


def retrieve_data(relative_url):
    """Take a relative url and return the JSON Object at that address."""

    url = BASE_URL + relative_url
    response = requests.get(url)
    
    # Raise a 404 status before we go further.
    response.raise_for_status()
    
    return response.json()


def isScalar(value):
    return isinstance(value, (int, str, float))

class APIResponse(Mapping):

    @classmethod
    def fromJSONResponse(cls, response, **kwargs):
        """Create an APIResponse object from exsisting data."""
        return cls(response=response, **kwargs)
    
    @classmethod
    def fromURL(cls, url, **kwargs):
        """Creat an APIResponse object from a relative URL."""
        return cls(url=url, **kwargs)

    @classmethod
    def fromKeys(cls, database, table, resource_id, **kwargs):
        """Create an APIResponse object from a database, table, and id"""
        return cls(database=database, table=table, resource_id=resource_id, **kwargs)

    def __init__(self, **kwargs):

        if kwargs.get('response') is not None:
            self.json_response = kwargs.get('response')

        elif kwargs.get('url') is not None:
            self.__href = kwargs.get('url')
            self.json_response = retrieve_data(self.__href)

        else:
            database = kwargs.get('database')
            table = kwargs.get('table')
            resource_id = kwargs.get('resource_id')

            self.__href = f'/db/{database}/{table}/{table}Id/{resource_id}.json'
            self.json_response = retrieve_data(self.__href)

        if 'loads' not in kwargs:
            kwargs['loads'] = 0

        if kwargs.get('loads') < 2:
            self.load(**kwargs)
        else:
            self.__loaded = False

            
    def load(self, **kwargs):
        kwargs['loads'] = kwargs.get('loads', 0) + 1
        if 'url' in kwargs:
            del kwargs['url']

        if isinstance(self.json_response, dict):
            for key, val in self.json_response.items():
                
                if not (isScalar(val) or isinstance(val, APIResponse)):
                    if '__href' in val:
                        val = APIResponse.fromURL(url=val['__href'], **kwargs)
                        self.json_response[key] = val
        else:
            for i in range(len(self.json_response)):
                val = self.json_response[i]
                
                if not (isScalar(val) or isinstance(val, APIResponse)):
                    if '__href' in val:
                        val = APIResponse.fromURL(url=val['__href'], **kwargs)
                        self.json_response[i] = val

        self.__loaded = True

    def __len__(self):
        return len(self.json_response)

    def __contains__(self, key):
        return key in self.json_response

    def __iter__(self):
        # TODO: Override this to handle the API's Pagination
        return iter(self.json_response)

    def __getitem__(self, key):

        if not self.__loaded:
            self.load()

        return self.json_response[key]

    def __repr__(self):
        if self.json_response is None:
            return f'<unfetched APIResponse object>'
        else:
            return '<APIResponse ' + repr(self.json_response) + '>'