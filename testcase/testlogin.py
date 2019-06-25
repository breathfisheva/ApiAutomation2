import unittest, xmlrunner
from testcase.testcasebase import ApiServerUnittest
from utils.Request import *
from data.get_parameters import Parameters
from utils.Validator import *


'''同一个testcase类下面共用一个Session， 所以Session初始化放在testcasebase里'''
class TestLogin(ApiServerUnittest):

    def test_info(self):
        #login firstly then Session will have be save on self.api_client
        para = Parameters(r"../data/casedata/login_case_data.yml")
        req_kwargs = para.request
        url = para.url
        method = para.method
        response_expected = para.response

        response = Request(self.api_client, url=url, method=method, **req_kwargs).send_request()

        #visit info url
        para = Parameters(r"../data/casedata/info_case_data.yml")
        req_kwargs = para.request
        url = para.url
        method = para.method
        response_expected = para.response

        response = Request(self.api_client, url=url, method=method, **req_kwargs).send_request()

        result = response_validator(response, response_expected)
        print(result)


    def test_login(self):

        para = Parameters(r"../data/casedata/login_case_data.yml")
        req_kwargs = para.request
        url = para.url
        method = para.method
        response_expected = para.response

        response = Request(self.api_client, url=url, method=method, **req_kwargs).send_request()

        result = response_validator(response, response_expected)
        print(result)


if __name__=='__main__':
    suite = unittest.TestSuite()
    # suite.addTest(TestLogin('test_login'))
    suite.addTest(TestLogin('test_info'))
    runner = xmlrunner.XMLTestRunner(output='report')#指定报告放的目录
    runner.run(suite)