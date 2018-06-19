---
title: oslo 源码分析之 context
date: 2018-06-03 15:28:40
tags: [openstack]
---

在介绍源码之前，我们先谈谈什么是 context. 一开始不太理解什么是 context，其实它是一个统称，在不同的地方有不同的含义，所以不是很直白。context 翻译成中文是“上下文”的意思，说白了和文章的上下文是一个意思，通俗一点讲就是环境。例如用户信息，token 之类的。如果还是不明白，看看下面的例子。

<!-- more -->

openstack 的 context 主要是用来保存 http request 相关信息。 context 模块主要定义了一个 RequestContext 类，里面保存了跟 request 请求相关的信息：

```python
class RequestContext(object):

    """Helper class to represent useful information about a request context.

    Stores information about the security context under which the user
    accesses the system, as well as additional request information.
    """

    user_idt_format = u'{user} {tenant} {domain} {user_domain} {p_domain}'
    # Can be overridden in subclasses to specify extra keys that should be
    # read when constructing a context using from_dict.
    FROM_DICT_EXTRA_KEYS = []

    @_renamed_kwarg('user', 'user_id')
    @_renamed_kwarg('tenant', 'project_id')
    @_renamed_kwarg('domain', 'domain_id')
    @_renamed_kwarg('user_domain', 'user_domain_id')
    @_renamed_kwarg('project_domain', 'project_domain_id')
    def __init__(self,
                 auth_token=None,
                 user_id=None,
                 project_id=None,
                 domain_id=None,
                 user_domain_id=None,
                 project_domain_id=None,
                 is_admin=False,
                 read_only=False,
                 show_deleted=False,
                 request_id=None,
                 resource_uuid=None,
                 overwrite=True,
                 roles=None,
                 user_name=None,
                 project_name=None,
                 domain_name=None,
                 user_domain_name=None,
                 project_domain_name=None,
                 is_admin_project=True,
                 service_token=None,
                 service_user_id=None,
                 service_user_name=None,
                 service_user_domain_id=None,
                 service_user_domain_name=None,
                 service_project_id=None,
                 service_project_name=None,
                 service_project_domain_id=None,
                 service_project_domain_name=None,
                 service_roles=None,
                 global_request_id=None,
                 system_scope=None):
        """Initialize the RequestContext

        :param overwrite: Set to False to ensure that the greenthread local
                          copy of the index is not overwritten.
        :param is_admin_project: Whether the specified project is specified in
                                 the token as the admin project. Defaults to
                                 True for backwards compatibility.
        :type is_admin_project: bool
        :param system_scope: The system scope of a token. The value ``all``
                             represents the entire deployment system. A service
                             ID represents a specific service within the
                             deployment system.
        :type system_scope: string
        """
        # setting to private variables to avoid triggering subclass properties
        self._user_id = user_id
        self._project_id = project_id
        self._domain_id = domain_id
        self._user_domain_id = user_domain_id
        self._project_domain_id = project_domain_id

        self.auth_token = auth_token
        self.user_name = user_name
        self.project_name = project_name
        self.domain_name = domain_name
        self.system_scope = system_scope
        self.user_domain_name = user_domain_name
        self.project_domain_name = project_domain_name
        self.is_admin = is_admin
        self.is_admin_project = is_admin_project
        self.read_only = read_only
        self.show_deleted = show_deleted
        self.resource_uuid = resource_uuid
        self.roles = roles or []

        self.service_token = service_token
        self.service_user_id = service_user_id
        self.service_user_name = service_user_name
        self.service_user_domain_id = service_user_domain_id
        self.service_user_domain_name = service_user_domain_name
        self.service_project_id = service_project_id
        self.service_project_name = service_project_name
        self.service_project_domain_id = service_project_domain_id
        self.service_project_domain_name = service_project_domain_name
        self.service_roles = service_roles or []

        if not request_id:
            request_id = generate_request_id()
        self.request_id = request_id
        self.global_request_id = global_request_id
        if overwrite or not get_current():
            self.update_store()
```

先看官方文档给的一个例子：

```python
from oslo_config import cfg
from oslo_context import context
from oslo_log import log as logging

CONF = cfg.CONF
DOMAIN = "demo"

logging.register_options(CONF)
logging.setup(CONF, DOMAIN)

LOG = logging.getLogger(__name__)

LOG.info("Message without context")
context.RequestContext()
LOG.info("Message with context")
```

上面的代码打印结果如下：

```bash
2016-01-20 21:56:29.283 8428 INFO __main__ [-] Message without context
2016-01-20 21:56:29.284 8428 INFO __main__ [req-929d23e9-f50e-46ae-a8a7-02bc8c3fd2c8 - - - - -] Message with context
```

看到上面的打印，有些人可能会有疑问，代码中只创建了 context.RequestContext 对象，并未赋值给 LOG, LOG 是怎么获取 request_id 的，实际上，RequestContext 对象创建之后会保存在 threading.local() 中，所以当前线程的其它代码都可以读取到 RequestContext 的值。