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
        collection = dict (
            collection = dict (
                version = '1.0',
                href    = url,
                items   = [
                    dict (
                        href = '%s/%s'.format (url, item),
                        data = [
                            dict (
                                name = 'caption',
                                value = 'this is item %s'.format (item),
                            ),
                            dict (
                                name = 'value',
                                value = item,
                            ),
                        ],
                    )
                    for item in 'one two three'.split()
                ]
            )
        )

        mock.get (url,
            status_code = 200,
            headers     = { 'Content-Type' : 'application/vnd.collection+json' },
            json        = data.collection,
        )

        request = ab.http.Request()
        res = request.get (url = url)

        self.assertSequenceEqual (
            sorted ('href thing links template version'.split()),
            sorted (list (res.keys())),
        )


if __name__ == '__main__':
    unittest.main()
