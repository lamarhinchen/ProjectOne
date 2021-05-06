from controllers import tuition_controller, home_controller


def route(app):
    # Call all other controllers
    tuition_controller.route(app)
    home_controller.route(app)
