# -*- coding: utf-8 -*-
#
# This file is part of hepcrawl.
# Copyright (C) 2015, 2016, 2017 CERN.
#
# hepcrawl is a free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Parsers for various metadata formats"""

from __future__ import absolute_import, division, print_function

from inspire_schemas.api import LiteratureBuilder

from ..utils import get_node


class JatsParser(object):
    """Parser for the JATS format.

    It can be used directly by invoking the :ref:`parse_record` method, or be
    subclassed to customize its behavior.
    """

    @classmethod
    def parse_record(cls, jats_record, source=None):
        """Parse a JATS record into an Inspire HEP record.

        Args:
            jats_record (str): the record in JATS format to parse.
            source (Optional[str]): if provided, sets the ``source`` everywhere
                in the record. Otherwise, the source is parsed from the JATS
                metadata.

        Returns:
            object: the same record in the Inspire Literature schema.
        """
        article = cls.get_article_node(jats_record)

        abstract = cls.parse_abstract(article)
        collaborations = cls.parse_collaborations(article)
        publication_info = {
            'journal_title': cls.parse_journal_title(article)
        }
        if not source:
            source = cls.parse_publisher(article)

        lit_builder = LiteratureBuilder(source)
        lit_builder.add_abstract(abstract)
        lit_builder.add_publication_info(**publication_info)
        for collab in collaborations:
            lit_builder.add_collaboration(collab)

        return lit_builder.record

    @staticmethod
    def get_article_node(jats_record):
        """Get a selector on the root article node of the record.

        This can be overridden in case some preprocessing needs to be done on
        the XML.

        Args:
            jats_record(str): the record in JATS format.

        Returns:
            scrapy.selector.Selector: a selector on the root node.
        """
        node = get_node(jats_record)
        node.remove_namespaces()

        return node

    @staticmethod
    def parse_abstract(root_node):
        """Parse the abstract"""
        abstract = root_node.xpath('//front//abstract[1]/*').extract_first()

        return abstract

    @staticmethod
    def parse_collaborations(root_node):
        """Parse the collaborations"""
        collaborations = root_node.xpath(
            '//front//collab|'
            '//front//contrib[@contrib-type="collaboration"]'
        ).extract()

        return collaborations

    @staticmethod
    def parse_journal_title(root_node):
        """Parse the journal title"""
        journal_title = root_node.xpath(
            './front/journal-meta//abbrev-journal-title/text()|'
            './front/journal-meta//journal-title/text()'
        ).extract_first()

        return journal_title

    @staticmethod
    def parse_journal_issue(root_node):
        """Parse the journal issue"""
        journal_issue = root_node.xpath('./front/article-meta/issue/text()').extract_first()

        return journal_issue

    @staticmethod
    def parse_journal_volume(root_node):
        """Parse the journal volume"""
        journal_volume = root_node.xpath('./front/article-meta/volume/text()').extract_first()

        return journal_volume

    @staticmethod
    def parse_issue(root_node):
        """Parse the journal issue"""
        journal_issue = root_node.xpath('//front//issue/text()').extract_first()

        return journal_issue

    @staticmethod
    def parse_publisher(root_node):
        """Parse the publisher name"""
        publisher_name = root_node.xpath('//front//publisher-name/text()'
                                         ).extract_first()

        return publisher_name

