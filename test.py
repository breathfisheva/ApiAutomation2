import re
import os
import sys

from requests import Session

template ="""
args:
  - {method}
  - {api}
kwargs:
  -
    caseName: {caseName}
    {data_or_params}:
        {data}
validator:
  -
    json:
      successed: True
"""
paras_list = ['Content-Type', 'POST', 'GET', 'PUT', 'DELETE', 'HTTP/1.1']
data_dict = {}
data_list = []

#如果没有定义编码格式，则会使用系统默认的编码，如果有不支持的则会出错，所以制定encoding='utf8'
f = open('fiddler2.txt', 'r', encoding='utf8')
data = f.readlines()

for index, line in enumerate(data):
    if line.split(' ')[0].upper() in paras_list:
        # data_dict['url'] = line.split(' ')[1]
        # data_dict['method'] = line.split(' ')[0]
        data_dict[line.split(' ')[0]] = line.split(' ')[1]

    if line.split(':')[0] in paras_list:
        data_dict[line.split(':')[0]] = line.split(':')[1]

    if "{" in line:
        data_dict['response'] = line

    # need improve , how to get request data
    if "username" in line:
        data_dict['data'] = line

    #different req
    if '------------------------------------------------------------------\n' in line:
        data_list.append(data_dict)
        data_dict = {}


print(data_list)
f.close()


# def auto_gen_cases(filepath):


        # with open(file_, 'w', encoding='utf-8') as fw:
        #     fw.write(template.format(
        #         method=method,
        #         api=api,
        #         caseName=caseName,
        #         data_or_params=data_or_params,
        #         data=data_s
        #     ))
        #
        # os.chdir(project_)



