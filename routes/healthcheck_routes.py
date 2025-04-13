from fastapi import APIRouter

class HealthCheckRoutes:
    application = app = {}
    sl_controller = {}

    def __init__(self):
        self.app = APIRouter()
        self.application = self.app
        self.__add_routes()

    def __add_routes(self):
        self.app.add_api_route(
            path='/healthCheck'
            , endpoint=self.health_check
            , methods=['GET']
        )

    def health_check(self):
        try:
            return '202'
        except Exception as e2:
            return str(e2)
