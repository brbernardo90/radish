# -*- coding: utf-8 -*-

"""
    This module provides an extension to write all features, scenarios and steps to the syslog.
"""


from radish.terrain import world
from radish.feature import Feature
from radish.hookregistry import before, after

import syslog


def get_scenario_feature(scenario):
    """
        Gets the scenarios feature
    """
    if not isinstance(scenario.parent, Feature):
        return scenario.parent.parent

    return scenario.parent


def log(message):
    """
        Logs the given message to the syslog

        :param string message: the message to log
    """
    if isinstance(message, unicode):
        message = message.encode("utf8")
    syslog.syslog(syslog.LOG_INFO, message)


@before.all  # pylint: disable=no-member
def syslog_writer_before_all(features, marker):  # pylint: disable=unused-argument
    """
        Opens the syslog
    """
    syslog.openlog("radish")
    log(u"begin run {}".format(marker))


@after.all  # pylint: disable=no-member
def syslog_writer_after_all(features, marker):  # pylint: disable=unused-argument
    """
        Closes the syslog
    """
    log(u"end run {}".format(marker))
    syslog.closelog()


@before.each_feature  # pylint: disable=no-member
def syslog_writer_before_each_feature(feature):
    """
        Writes the feature to the syslog
    """
    log(u"begin feature {}:{} {}".format(world.config.marker, feature.id, feature.sentence))


@after.each_feature  # pylint: disable=no-member
def syslog_writer_after_each_feature(feature):
    """
        Writes the feature to the syslog
    """
    log(u"end feature {}:{} {}".format(world.config.marker, feature.id, feature.sentence))


@before.each_scenario  # pylint: disable=no-member
def syslog_writer_before_each_scenario(scenario):
    """
        Writes the scenario to the syslog
    """
    log(u"begin scenario {}:{}.{} {}".format(world.config.marker, get_scenario_feature(scenario).id, scenario.id, scenario.sentence))


@after.each_scenario  # pylint: disable=no-member
def syslog_writer_after_each_scenario(scenario):
    """
        Writes the scenario to the syslog
    """
    log(u"end scenario {}:{}.{} {}".format(world.config.marker, get_scenario_feature(scenario).id, scenario.id, scenario.sentence))


@before.each_step  # pylint: disable=no-member
def syslog_writer_before_each_step(step):
    """
        Writes the step to the syslog
    """
    log(u"begin step {}:{}.{}.{} {}".format(world.config.marker, get_scenario_feature(step.parent).id, step.parent.id, step.id, step.sentence))


@after.each_step  # pylint: disable=no-member
def syslog_writer_after_each_step(step):
    """
        Writes the step to the syslog
    """
    log(u"{} step {}:{}.{}.{} {}".format(step.state, world.config.marker, get_scenario_feature(step.parent).id, step.parent.id, step.id, step.sentence))
