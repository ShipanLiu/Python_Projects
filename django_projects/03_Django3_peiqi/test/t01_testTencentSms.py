""" 这个是 为了测试和 弄清楚  到底是如何发送短信的 """
# 加入import 不出来的话， 就关闭vscode
from tencentcloud.common import credential
from tencentcloud.sms.v20210111 import sms_client, models

# secret_id and secret_key
cred = credential.Credential("AKIDa0B7nhOq3zf5G819TmzNVO0MRHrAE3Yn", "4rPincBUYMuCEzUjsdIiuqWv3vYu0qPh")

client = sms_client.SmsClient(cred, "ap_guangzhou")

req = models.SendSmsRequest()

req.SmsSdkAppId = "1400455481"
req.SignName = "Python之路"
req.TemplateId = "548762"
req.PhoneNumberSet = ["+8617720139627"]

resp = client.SendSms(req)

print(resp.to_json_string(indent = 2))
