'''
load yaml file , replace variable and function (from config.py), return a dict data
'''

import re, io, yaml
import importlib


#动态导入库，所有yaml文件会用到的函数和变量都放到utils.py文件里，之后在yaml_load里，return函数方法和变量值的时候记得加上"module."
def load_all_variables_functions():
    module =importlib.import_module('data.config')
    return module
module = load_all_variables_functions()

#yaml_load 方法把yaml文件里的函数调用返回结果，参数返回结果，变成最后的测试用例，实现了参数和测试用例的隔离.之后的send request就从这里获取数据
def yaml_load(yaml_file):
    """
    异步读取yaml文件，并转义其中的特殊值
    :param file:
    :return:
    """

    #1.load yaml文件内容
    with io.open(yaml_file, 'r', encoding='utf-8') as stream:
        yaml_content = yaml.load(stream)

    data = yaml_content


    #2.定义filter出function和variable的正则
    pattern_function = re.compile(r"^\$\{(\w+)\(([\$\w =,]*)\)\}$")
    pattern_variable = re.compile(r"\$(\w+)") #$var


    #3.根据正则判断是function还是variable
    def is_functon(content):
        matched = pattern_function.match(content)
        return True if matched else False

    def is_variable(content):
        matched = pattern_variable.match(content)
        return True if matched else False


    #4.循环遍历整个yaml文件内容， 如果是list，tuple， dict则继续迭代，如果是string或者bytes，说明已经到了最里面的部分了，这时候有可能是function，varaible，也可能就是最后的值。
    def my_iter(data):
        """
        递归测试用例，根据不同数据类型做相应处理，将模板语法转化为正常值
        :param data:
        :return:
        """
        if isinstance(data, (list, tuple)):
            for index, _data in enumerate(data):
                data[index] = my_iter(_data) or _data

        elif isinstance(data, dict):
            for k, v in data.items():
                data[k] = my_iter(v) or v

        elif isinstance(data, (str, bytes)):
            #4.1 如果是function 有可能是这几个情况
            # ${gen_uid($vara, $varb)} ； 把函数名，和变量拆开，然后判断变量是参数还是直接的结果，如果是参数则通过eval返回参数值，如果不是参数则直接返回
            # ${gen_uid(3, b=2)}
            # 这里用func_str来拼接函数表达值，最后调用eval(func_str)来调用函数返回执行结果

            if is_functon(data):
                m = pattern_function.match(data)
                func_str = ""
                if m:
                    fun = m.group(1)
                    args = m.group(2).split(',')

                    func_str += "module."+ fun + "("

                    for index, arg in enumerate(args):
                        if is_variable(arg.strip()):
                            variable_name = "module." + pattern_variable.match(arg.strip()).group(1)
                            # args[index] = str(eval(pattern_variable.match(arg.strip()).group(1)))
                            args[index] = str(eval(variable_name))
                        else:
                            args[index] = arg
                        func_str += args[index] + ","

                    func_str = func_str[:-1]  #remove the last , letter
                    func_str += ")"
                    return eval(func_str) #execute the method


            elif is_variable(data):
                m = pattern_variable.match(data)
                if m:
                    variable_name = "module." + m.group(1)
                    return eval(variable_name)
            else:
                return data

    my_iter(data)
    return data

if __name__ == '__main__':
    print(yaml_load(r"casedata/login_case_data.yml"))