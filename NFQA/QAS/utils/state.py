def is_have_history(request) -> (bool, object):
    """
    判断请求是否有历史信息
    1:代表具有历史信息
    other:代表没有
    """
    state = int(request.data.get('state', 0))
    if state == 1:
        history = request.data.get('history', None)
        return True, history
    return False, None
