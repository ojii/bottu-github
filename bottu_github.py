# -*- coding: utf-8 -*-
import json
import re
from twisted.python import log
from twisted.web.client import getPage

ISSUES_URL_TPL = 'https://api.github.com/repos/%s/issues/%s'

def get_issue_status(env, issue_id):
    def callback(data):
        try:
            issue = json.loads(data)
        except ValueError:
            log.msg("Could not load JSON data: %r" % data)
            log.err()
            env.msg("Error looking up issue #%s" % issue_id)
            return
        env.msg("Issue #%(number)s: %(title)s (%(state)s): %(html_url)s" % issue)

    def errback(failure):
        try:
            failure.raiseException()
        except Exception:
            log.err()
        env.msg("Error looking up issue #%s" % issue_id)
    deferred = getPage(ISSUES_URL_TPL % (env.plugin.reponame, issue_id))
    deferred.addCallback(callback).addErrback(errback)

def message(env, message):
    if env.user.name.lower() in env.plugin.ignore_names:
        return
    numbers = []
    for regex in env.plugin.regexes:
        for number in regex.findall(message):
            if number not in numbers:
                numbers.append(number) # duplicate prevention
                get_issue_status(env, number)

def compile_re(regex):
    return re.compile(regex, re.I)

def register(app, conf):
    plugin = app.add_plugin('GitHub')
    plugin.regexes = map(compile_re, conf.get('issues-regex', []))
    plugin.reponame = conf.get('reponame', None)
    plugin.ignore_names = [name.lower() for name in conf.get('ignore', [])]
    if plugin.reponame and plugin.regexes:
        plugin.bind_event('message', message)
    else:
        log.msg("No reponame and/or no issues-regex specified")
