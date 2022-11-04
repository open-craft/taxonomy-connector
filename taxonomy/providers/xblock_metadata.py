# -*- coding: utf-8 -*-
"""
Abstract base class for xblock metadata providers.

All host platform must implement this provider in order for taxonomy to work.
"""
from abc import abstractmethod


class XBlockMetadataProvider:
    """
    Abstract base class for xblock metadata providers.

    All abstract methods must be implemented for taxonomy's normal functionality.
    """

    @abstractmethod
    def get_xblocks(self, xblock_ids):
        """
        Get a list of xblocks matching the xblock ids provided in the argument.
        Include content of all children xblocks in content

        Arguments:
          xblock_ids(list<str>): A list of UUIDs in the form of a string.

        Returns:
          list<dict>: A list of xblocks in the form of dictionary.
            Dictionary object must have the following keys
            1. key: xblock usage key
            2. content_type: xblock content type
            3. content: xblock text content
        """

    @abstractmethod
    def get_all_xblocks(self):
        """
        Get iterator for all the xblocks.

        Returns:
          iterator<dict>: An iterator of xblocks in the form of dictionary.
            Dictionary object must have the following keys
            1. key: xblock usage key
            2. content_type: xblock content type
            3. content: xblock text content
        """
