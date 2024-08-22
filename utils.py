
class ResponseParam:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    def get_response(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }


