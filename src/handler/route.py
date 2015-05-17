from src.handler import wechat
wechat_handlers = [
    (r'/wechat', wechat.WechatHandler),
]

handlers = (
    wechat_handlers
)
