# -*- coding: utf-8 -*-
#
# This file is part of hepcrawl.
# Copyright (C) 2015, 2016, 2017 CERN.
#
# hepcrawl is a free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
import yaml

from hepcrawl.testlib.fixtures import get_test_suite_path
from hepcrawl.parsers.jats import JatsParser as JP


@pytest.fixture
def aps_parsed():
    """A dictionary holding the parsed elements of the record."""
    path = get_test_suite_path('responses', 'aps',
                               'PhysRevX.7.021022_parsed.yml')
    with open(path) as f:
        aps_parsed = yaml.load(f)

    return aps_parsed


@pytest.fixture
def aps_jats():
    """A selector on a JATS record from APS."""
    path = get_test_suite_path('responses', 'aps', 'PhysRevX.7.021022.xml')
    with open(path) as f:
        aps_jats = f.read()

    return JP.get_article_node(aps_jats)


def test_parse_abstract(aps_jats, aps_parsed):
    result = JP.parse_abstract(aps_jats)
    expected = aps_parsed['abstract']

    assert result == expected

def test_parse_journal_issue(aps_jats, aps_parsed):
    result = JP.parse_journal_issue(aps_jats)
    expected = str(aps_parsed['issue'])

    assert result == expected


def test_parse_journal_title(aps_jats, aps_parsed):
    result = JP.parse_journal_title(aps_jats)
    expected = aps_parsed['journal_title']

    assert result == expected


def test_parse_journal_volume(aps_jats, aps_parsed):
    result = JP.parse_journal_volume(aps_jats)
    expected = str(aps_parsed['volume'])

    assert result == expected


def test_parse_publisher(aps_jats, aps_parsed):
    result = JP.parse_publisher(aps_jats)
    expected = aps_parsed['publisher']

    assert result == expected
