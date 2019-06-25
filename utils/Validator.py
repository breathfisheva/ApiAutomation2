'''
function to analyse the response with expected result
'''
from utils.Request import *
import logging

def response_validator(resp_obj, expec_obj):

    diff_content = diff_response(resp_obj, expec_obj)
    success = False if diff_content else True
    return success, diff_content

def parse_response_object(resp_obj):
    try:
        resp_body = resp_obj.json()
    except ValueError:
        resp_body = resp_obj.text

    return {
        'status_code': resp_obj.status_code,
        'headers': resp_obj.headers,
        'body': resp_body
    }


def diff_response(resp_obj, expected_resp_json):
    diff_content = {}
    resp_info = parse_response_object(resp_obj)
    for key, expected_value in expected_resp_json.items():
        value = resp_info.get(key, None)
        if str(value)!= str(expected_value):
            diff_content[key] = {
                'value': value,
                'expected': expected_value
            }
    if diff_content != {}:
        logging.error('%s' %(diff_content))
        assert diff_content == {}
    # return diff_content


# if __name__ == '__main__':
#     from data.loader import *
#     data = yaml_load(r"../data/casedata/login_case_data.yml") #yml文件的路径，../表示当前项目路径
#     req_kwargs = data[0]['test']['request']
#     response_expected = data[0]['test']['response']
#
#     try:
#         url = req_kwargs.pop('url')
#         method = req_kwargs.pop('method')
#     except KeyError as e:
#         raise e.ParamsError("Params Error")
#
#     req = Request(url=url, method=method, **req_kwargs)
#     response = req.send_request()


    # result = response_validator(response, response_expected)
    # print(result)


