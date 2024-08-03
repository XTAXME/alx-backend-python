#!/usr/bin/env python3
""" define test_utils """
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
import requests


class TestAccessNestedMap(unittest.TestCase):
    """ define class TestAccessNestedMap """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, exp):
        """ imp test method """
        self.assertEqual(access_nested_map(nested_map, path), exp)

    @parameterized.expand([
        ({}, ("a",), "KeyError: 'a'"),
        ({"a": 1}, ("a", "b"), "KeyError: 'b'")
    ])
    def test_access_nested_map_exception(self, nested_map, path, exp):
        """ testing method that raises keyError Excp """
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        # self.assertEqual(exp, e)


class TestGetJson(unittest.TestCase):
    """ define TestGetJson class """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """ tests utils.get_json """

        attr = {'json.return_value': test_payload}
        with patch('requests.get', return_value=Mock(**attr)) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """ class TestMoize """

    def test_memoize(self):
        """ test_memoize definition """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            mock.assert_called_once()
