# ApiAutomation2

## 文件结构介绍

##### 1.测试的数据放在yaml文件里 【data/casedata】
    - yaml文件里依赖的变量，方法实现放在config文件里 【data/config.py】

##### 2.导入测试数据 【data/loader.py || data/get_parameters.py】
    - 用loader.py里的方法把yaml文件转换成list，每个list里面是dict ， 并且把yaml文件里的变量替换成值，方法执行并且返回方法值
    - 用get_parameters.py里的方法，把loader.py里放回的值进行处理，用户通过实例化Parameters类，直接得到url，method等， 为了方便访问用了@property装饰器
    - 用正则表达式找到变量 $var 还有函数 ${func()}
    - 有些方法的调用需要导入库，所以用importlib.import_module 实现动态导入库
    - 用eval方法可以执行字符串并返回相应的值来实现动态调用yaml文件
    
##### 3.封装request请求【utils/Request.py】
    - 根据不同的method调用不同的发送请求的方法，比如post，get
    - 返回response对象
    - 由于考虑到session，cookie等问题，所以选用requests.Session()这个类
        - 由于不同的测试用例会需要用到同一个session，所以这里把session作为一个参数传入
        - session参数来源于testcase基类里的 setUpClass 方法 【testcase/testcasebase.py】
  > cls.api_client = requests.Session()

##### 4.写判断实际的response和期望的response的函数【utils/Validator.py】
    - 把Requst里返回的response对象通过 resp_obj.json() 方法转换成json对象，然后提取需要的值，返回一个字典，然后和expected 的response进行比较
    - 因为用的是unittest框架，所以这里用了Assert方法，如果不正确则unittest的testcase fail

##### 5.写testcase的基类【testcase/testcasebase.py】
    - 基类继承unittest.TestCase，重写 setUpClass(cls)， 主要是定义了host的地址和session实例化，因为case需要共用host和session

##### 6.写具体的testcase【testcase/testlogin.py】
    - testcase继承testcase基类ApiServerUnittest
    - 1.通过data.get_parameters 里的Parameters类获得需要的url，method，kwargs，response
    - 2.实例化Request类，传入url，method，kwargs还有session的实例化对象 self.api_client
    - 3.调用类Request的send_request方法发送请求得到response
    - 4.调用Validator的response_validator方法来判断最后的结果是否是期望的结果
    - 5.使用unittest框架的xmlrunner自动生成测试报告


## 使用

##### 1.到data/casedata里写对应的yml文件 （注意yaml文件要遵循规则）
>
    test:
        casename: login
        request:
            url: http://127.0.0.1:8880/info
            method: GET

        response:
            status_code: 200
            headers:
                Content-Type: application/json
            body:
                code: 200
                msg: success
                data: info



##### 2.yaml文件用到的变量值可以到data/config.py文件里定义

##### 3.到testcase下面写具体的testcase

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
