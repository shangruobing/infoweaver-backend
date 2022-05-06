import time

from rest_framework.throttling import BaseThrottle, SimpleRateThrottle

RECORD = {
    '用户IP': []
}


class MyThrottle(BaseThrottle):
    ctime = time.time
    # 60s 10次
    time_request = 60  # 访问时间
    num_request = 30  # 访问次数

    def get_ident(self, request):
        """
        根据用户IP和代理IP，当做请求者的唯一IP
        Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
        if present and number of proxies is > 0. If not use all of
        HTTP_X_FORWARDED_FOR if it is available, if not use REMOTE_ADDR.
        """
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = request.META.get('REMOTE_ADDR')

        return ''.join(xff.split()) if xff else remote_addr

    def allow_request(self, request, view):
        """
        是否仍然在允许范围内
        具体执行频率控制的方法
        Return `True` if the request should be allowed, `False` otherwise.
        :param request:
        :param view:
        :return: True，表示可以通过；False表示已超过限制，不允许访问
        """
        # 获取用户唯一标识（如：IP）

        # 允许60s访问3次
        # num_request = 3  # 访问次数
        # time_request = 60  # 访问时间

        now = self.ctime()
        ident = self.get_ident(request)
        self.ident = ident
        if ident not in RECORD:
            RECORD[ident] = [now, ]
            return True
        history = RECORD[ident]
        # while history and history[-1] <= now - time_request:
        while history and history[-1] <= now - self.time_request:
            history.pop()
        if len(history) < self.num_request:
            # if len(history) < num_request:
            history.insert(0, now)
            return True

    def wait(self):
        """
        当拒绝访问后 多少秒后可以允许继续访问
        """
        last_time = RECORD[self.ident][0]
        now = self.ctime()
        # return int(10 + last_time - now)
        return int(self.time_request + last_time - now)


class MySimpleThrottle(SimpleRateThrottle):
    # scope就是一个key，用于在配置文件指明
    scope = 'mySimpleThrottle'

    def get_cache_key(self, request, view):
        """
        Should return a unique cache-key which can be used for throttling.
        Must be overridden.

        May return `None` if the request should not be throttled.
        """
        if not request.user:
            ident = self.get_ident(request)
        else:
            ident = request.user

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
