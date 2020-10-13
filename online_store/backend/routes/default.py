"""Module for providing a default route for the site."""
import os
import re
import subprocess

from flask import Blueprint, render_template_string

default_router = Blueprint(__name__, "default", url_prefix="")  # pylint: disable=C0103


@default_router.route('/')
def get_default_route():
    """Return a list of routes."""
    routes = subprocess.getoutput(f'python manage.py routes 2>{os.devnull}') \
                       .split('\n')
    routes = [re.sub('[ \t]+', '\t', route).split('\t') for route in routes]
    return render_template_string(
        """
        <link rel="stylesheet"
              href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
              integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
              crossorigin="anonymous">
        <h1>Flask app is active!</h1>

        <h2>Routes</h2>
        <div>
        <p>
            The REST API can be experimented with using the Swagger-UI page,
            found <a href='/apidocs'>here</a>
        </p>
        <p>
            The routes available are:
        </p>

        <table class="table table-hover">
            </thead>
                <tr>
                    <th>Rule</td>
                    <th>Methods</td>
                    <th>Endpoint</td>
                </tr>
            </thead>
        {% for i in range(2, len) %}
            <tr>
                {% for j in range(3)|reverse %}
                <td>{{ routes[i][j] }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
        </table>

        </div>

        """, routes=routes, len=len(routes)
    )
