'''
send request and return the response object

需要改进：
1. 如果你发送一个非常大的文件作为 multipart/form-data 请求，你可能希望将请求做成数据流。默认下 requests 不支持, 但有个第三方包 requests-toolbelt 是支持的。
2. 增加put，delete
3. response.json方法，如果返回的不是可以转为json格式则会报错
'''


class Request(object):
    def __init__(self, session, url='', method='get', **kwargs ):
        self.url = url
        self.session = session
        self.method = method
        self.kwargs = kwargs
        self.response = None

    def send_request(self):
        if self.method.upper() == 'POST':
            self.response = self.session.post(self.url, **self.kwargs)

        elif self.method.upper() == 'GET':
            self.response = self.session.get(self.url)

        return self.response

        ''' add other http function put, delete'''


if __name__ == '__main__':
    from data.loader import *
    data = yaml_load(r"../data/casedata/login_case_data.yml") #yml文件的路径，../表示当前项目路径
    req_kwargs = data[0]['test']['request']

    try:
        url = req_kwargs.pop('url')
        method = req_kwargs.pop('method')
    except KeyError as e:
        raise e.ParamsError("Params Error")

    from requests import Session
    req = Request(Session(),url=url, method=method, **req_kwargs)
    response = req.send_request()

    print(response)

