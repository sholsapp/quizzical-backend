#!/usr/bin/env python

from quizzical import init_webapp


workers = 2
debug=False


def on_starting(server):
  server.log.setup(server.app.cfg)


def post_fork(server, worker):
  init_webapp(debug=debug)
