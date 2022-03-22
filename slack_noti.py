import pyupbit
import requests
import time
import schedule

access = "" # upbit access key
secret = "" # upbit secret key
myToken = "" # slack bot token

try:
    upbit = pyupbit.Upbit(access, secret)
    print("login complete")
except:
    print("login failed")
    print("restart please after check your key or token again ")

myKRW_balance = int(upbit.get_balance("KRW")) # 보유 현금 조회
myCOIN_balance = int(upbit.get_amount("ALL")) # 보유중인 코인 현금 환산 조회
init_balance = myKRW_balance + myCOIN_balance

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def restart():

    global init_balance

    KRW_hold = int(upbit.get_balance("KRW"))
    total_buy = int(upbit.get_amount('ALL'))
    today_bal = KRW_hold+total_buy


    earn = today_bal-init_balance
    earn_percent = earn/init_balance*100

    noti_message = "---------------------------------\n\n"+"어제 잔고 : "+ str(init_balance)+"\n\n" + "오늘 잔고 : " + str(today_bal)+"\n\n"+"수익률 : " + str(earn_percent)+"\n\n"+"수익 금액 : " + str(earn)
    post_message(myToken,"upbit-noti",noti_message)

    init_balance = today_bal

# 매일 10시 알림
schedule.every().day.at("10:00").do(restart)

while True:
    schedule.run_pending()
    time.sleep(1)


