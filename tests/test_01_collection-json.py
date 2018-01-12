import unittest
# import requests
import requests_mock

import ab.http
import ab.tests.data as data

class Test_Collection_JSON (unittest.TestCase):
    """
    """

    def setUp (self):
        self.global_value = 13

    @requests_mock.Mocker()
    def test (self, mock):
        url = 'https://api.example.net'

        mock.get (url,
            status_code = 200,
            headers     = { 'Content-Type' : 'application/vnd.collection+json' },
            json        = data.collection,
        )

        request = ab.http.Request()
        res = request.get (url = url)

        self.assertSequenceEqual (
            sorted ('href items links template version'.split()),
            sorted (list (res.keys())),
        )


if __name__ == '__main__':
    unittest.main()
