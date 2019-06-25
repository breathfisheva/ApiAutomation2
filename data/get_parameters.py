'''
现在是用data[0]来选出第一个case，需要改进的更灵活，而不是数字0
1.@property 使类的方法可以作为属性访问
'''

from data.loader import *

class Parameters(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = yaml_load(self.filepath)

    @property
    def request(self):
        req_kwargs = self.data[0]['test']['request']
        return req_kwargs

    @property
    def response(self):
        response = self.data[0]['test']['response']
        return response

    @property
    def url(self):
        try:
            url =  self.data[0]['test']['request'].pop('url') #这里使用pop，如果用self.data[0]['test']['request']['url']则可能或报错TypeError: type object got multiple values for keyword argument 'method'
            return url
        except KeyError as e:
            raise e.ParamsError("Params Error")

    @property
    def method(self):
        try:
            method = self.data[0]['test']['request'].pop('method')
            return method
        except KeyError as e:
            raise e.ParamsError("Params Error")


if __name__ == '__main__':
    para = Parameters(r"../data/casedata/login_case_data.yml")
    req_kwargs = para.get_request()
    print(para.get_url())
    print(req_kwargs)
