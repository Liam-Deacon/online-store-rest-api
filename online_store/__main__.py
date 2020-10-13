"""Convenience entry point for invoking flask server e.g. for Docker/Heroku"""
from __future__ import absolute_import
import os
from online_store.app import create_app

create_app().run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # noqa
