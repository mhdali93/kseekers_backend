class Result:
    def __init__(self):
        self.result_code = 0
        self.result_obj = {}
        self.result_row_count = 0
        self.message = ""


    def get(self):
        return {'code': self.result_code, 'object': self.result_obj,'row_count':self.result_row_count ,'message': self.message}

    def set(self, result_code, result_obj,result_row_count=0,message=""):
        self.result_code = result_code
        self.result_obj = result_obj
        self.result_row_count = result_row_count
        self.message = message

