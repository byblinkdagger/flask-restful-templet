
### [day-01]
#### 1.蓝图注册 
``Blueprint(__name__,url_prefix)``

#### 2.红图注册 
自定义的一个类，主要避免频繁创建蓝图（蓝图是用于区分模块的，而我们自定义的红图可以用来在同一个模块内区分不同业务类型的api）,
主要实现思路就是封装了蓝图的构造函数，构造器等，将部分需要的信息通过bp.add_url_rule()传入当前模块的蓝图对象

#### 3.尽量使用枚举来限制入参值

#### 4.wtform 
验证表单数据的插件库，Validator类提供了一些数据的限制验证，同时也可以自己通过validate_keyform的方式来验证参数的正确性。

application/json方式传递：
```
data = request.json
form = ClientForm(data=data)
```

form-data方式传递
```
data = request.form
form = ClientForm(formdata=data)
```

#### 5.自定义异常
400 : 参数错误  401 :未授权 403：禁止访问 404：not found 500:服务器未知错误 301， 302:重定向。

在wtform类中不满足验证的情况下手动抛出 raise ApiException()
捕获全局异常（隐藏问题了） --> AOP 全局拦截思想



### [day-02]

#### 1.token相关
存储时效性&&用户id
生成token的方法--generate_auth_token
生成密码的方法--generate_password_hash(raw)
验证密码的方法--check_password_hash

#### 2.namedtuple
命名元祖，可以再初始化的时候指定‘类名’与‘字段名’，将其当成一个对象来使用

```
import collections

MyTupleClass = collections.namedtuple('MyTupleClass',['name', 'age', 'job'])
obj = MyTupleClass("Tomsom",12,'Cooker')
print(obj.name)
print(obj.age)
print(obj.job)
```


#### 3.authtoken验证
* 1.通过header传递token,然后通过verify_auth_token验证改token的有效性（自定义一个login_check装饰器）

* 2.通过HTTPBasicAuthon自带协议，传递和验证token（将token放如accout中，通过@auth.login_required内置装饰器自行验证）


#### 4.jsonify()序列化对象
序列化对象(jsonify只可以将dict对象转换成Json格式的数据)
* 1.类变量不会存放至__dict__字典中，只有实例变量才会存至__dict__字典中

* 2.可通过dict(obj)的方式获取所有属性，需要重写keys() -- 返回dict的key值，即obj的每个成员变量名

* 3.需要重写__getitem__(self,item) --返回dict的value值



### [day-03]

#### 1.数据库软删除
仅把某个状态字段状态修改为0，表示不存在

#### 2.接口
访问时如果同时请求了一个接口，通过flask.g暂存某些数据，会造成数据紊乱吗  --  不会，g变量是线程隔离的

#### 3.数据库测试数据生成
可以通过with app.app_context()上下文，通过代码动态创建一系列账号

#### 4.管理员权限
user表中新增auth字段，修改管理员账号的字段值

#### 5.globals() 
类似于java的反射，可以将当前类的所有信息以K、V的形式存储至dict中，然后通过变量名可以直接实例化、直接使用。

#### 6.sqlAlchemy查询条件

```
Student.query(Student).filter(and_(Student.Sdept == 'SFS' , Student.Sage < 22)).all()
Student.query(Student).filter(or_(Student.Name.like('%luck%') , Student.addr.like('%luck%'))).all()
```

#### 7.序列化对象时隐藏某些字段
将模型对象的def keys()方法返回字段前，调用自定义的hide()方法，从中去除某些字段,记得 return self

#### 8.relationship反向引用


### [day-03]

#### 文件上传
利用``from werkzeug.wsgi import SharedDataMiddleware``