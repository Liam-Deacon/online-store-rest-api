"""Module for returning a simple terms of use webpage."""
from flask import Blueprint

terms_of_user_router = Blueprint("terms-of-use", __name__, url_prefix='/api')  # pylint: disable=invalid-name


@terms_of_user_router.route("/terms")
def terms():
    """Create a simple terms of use page for user."""
    return """<h1>Terms of Use</h1>
    Please be considerate when performing API requests.
    <br><br>
    Users who abuse the system will have their access removed and, in the
    case of criminal activity, potentially have legal action against them.
    """
