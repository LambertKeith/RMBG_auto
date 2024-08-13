
import requests
import json

def notify_to_the_group():
    
    
    # Webhook URL
    webhook_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/b64636ca-ac31-4a33-ba78-9ff1ac4dd348'

    # 消息内容
    data = {
        "msg_type": "text",
        "content": {
             "text": "本次抠图任务即将完成，请在一分钟后查看结果"
            #"text": "这是测试，不用理会。"
        }
    }

    # 将消息发送到Webhook
    response = requests.post(
        webhook_url, 
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    # 检查响应状态码
    if response.status_code == 200:
        print('消息发送成功')
    else:
        print(f'消息发送失败，状态码: {response.status_code}')
