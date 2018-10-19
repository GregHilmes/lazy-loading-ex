import unittest

from lazy import APIResponse


# Data samples taken from /DB demo database.
SAMPLE_RESPONSE_LIST = [
    {
        "Album": {
            "__href": "/db/Chinook/Artist/ArtistId/1/Album.json"
        },
        "ArtistId": 1,
        "Name": "AC/DC",
        "__href": "/db/Chinook/Artist/ArtistId/1.json"
    }
]
SAMPLE_RESPONSE_DICT = {
    "__href": "/db/Chinook/Album/AlbumId/1.json",
    "Title": "For Those About To Rock We Salute You",
    "Track": {
        "__href": "/db/Chinook/Album/AlbumId/1/Track.json"
    },
    "Artist": {
        "__href": "/db/Chinook/Album/AlbumId/1/Artist.json"
    },
    "AlbumId": 1,
    "ArtistId": 1
}

class TestAPIResponse(unittest.TestCase):

    def testCreationFromDictResponse(self):
        """Check that a JSON object behaves when passed."""
        resp = APIResponse.fromJSONResponse(SAMPLE_RESPONSE_DICT)
        self.assertIsInstance(resp.json_response, dict)    

    def testCreationFromListResponse(self):
        """Check that JSON array behaves when passed."""
        resp = APIResponse.fromJSONResponse(SAMPLE_RESPONSE_LIST)
        self.assertIsInstance(resp.json_response, list)

    def testCreationFromRelURL(self):
        """Check that the API is not called when a URL is passed."""
        resp = APIResponse.fromURL(SAMPLE_RESPONSE_DICT['__href'])
        self.assertIsNone(resp.json_response)

    def testCreationFromKeys(self):
        """Check that the API is not called when database keys are passed."""
        resp = APIResponse.fromKeys('Chinook', 'Album', 1)
        self.assertIsNone(resp.json_response)

    def testScalarAttrAccess(self):
        """Check that scalar attributes behave."""
        resp = APIResponse.fromJSONResponse(SAMPLE_RESPONSE_DICT)
        self.assertEqual(resp['AlbumId'], 1)

    def testRelationshipAttrCreation(self):
        """Check that an APIResponse is returned for relationship access."""
        resp = APIResponse.fromJSONResponse(SAMPLE_RESPONSE_DICT)
        # data should be a dict until acessed through resp[attr]
        self.assertIsInstance(resp.json_response['Track'], dict)
        self.assertIsInstance(resp['Track'], APIResponse)

    def testInvalidAttributeAccess(self):
        """Check that KeyError is raised when a nonexsistant value is requested."""
        resp = APIResponse.fromJSONResponse(SAMPLE_RESPONSE_DICT)
        with self.assertRaises(KeyError):
            resp['NONEXSISTANT_ATTRIBUTE']


if __name__ == '__main__':
    unittest.main()    
