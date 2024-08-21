#!/usr/bin/env python
# *-* coding: utf-8 *-*
r""":mod:`ClayCode.builder.utils` --- Utility functions for ClayCode builder
===============================================================================
This module provides utility functions for the ClayCode builder.
"""
from __future__ import annotations

import logging
from functools import singledispatch, wraps
from typing import Any, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)


def make_manual_setup_choice(select_function):
    """Decorator for manual setup options choice in :mod:`ClayCode.builder.utils`
    :param select_function: Function to decorate
    :type select_function: function
    :return: Decorated function
    :rtype: function
    """

    @wraps(select_function)
    def wrapper(instance_or_manual_setup, *args, **kwargs):
        manual_setup = get_manual_setup_option(instance_or_manual_setup)
        if manual_setup:
            result = select_function(*args, **kwargs)
        else:
            try:
                result = kwargs["result_map"][""]
            except TypeError:
                raise AttributeError("No default option specified")
            except KeyError:
                result = select_function(*args, **kwargs)
        return result

    return wrapper


@singledispatch
def get_manual_setup_option(instance_or_setup_option) -> str:
    """Get manual setup option from instance or setup option from class attribute
    :param instance_or_setup_option: Instance or setup option
    :type instance_or_setup_option: Union[TargetClayComposition, MatchClayComposition]
    :return: Manual setup option
    :rtype: str
    """
    assert instance_or_setup_option.__class__.__name__ in [
        "TargetClayComposition",
        "MatchClayComposition",
    ], f"Invalid usage of {__name__} with {instance_or_setup_option.__class__.__name__}!"
    return instance_or_setup_option.manual_setup


@get_manual_setup_option.register(bool)
def _(instance_or_setup_option) -> bool:
    """Get manual setup option from instance or setup option from boolean
    :param instance_or_setup_option: Instance or setup option
    :type instance_or_setup_option: bool
    :return: Manual setup option
    :rtype: bool
    """
    return instance_or_setup_option


@make_manual_setup_choice
def select_input_option(
    query: str,
    options: Union[List[str], Tuple[str], Set[str]],
    result: Optional[str] = None,
    result_map: Optional[Dict[str, Any]] = None,
) -> Any:
    """Process user input for a given query and options
    :param query: Query to display to user
    :type query: str
    :param options: Options to choose from
    :type options: Union[List[str], Tuple[str], Set[str]]
    :param result: Result to return if no user input is given
    :type result: Optional[str]
    :param result_map: Mapping of user input to return values
    :type result_map: Optional[Dict[str, Any]]
    :return: User input or result
    :rtype: Any
    """
    while result not in options:
        result = input(query).lower().strip(" ")
    if result_map is not None:
        result = result_map[result]
    return result
