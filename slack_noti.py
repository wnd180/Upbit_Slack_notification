import pyupbit
import requests
import time
import schedule

access = "" # upbit access key
secret = "" # upbit secret key
myToken = "" # slack bot token

def restart():

    global init_balance

    today_bal = get_wallet_balance

    earn = today_bal-init_balance
    earn_percent = earn/init_balance*100

    noti_message = "---------------------------------\n\n"+"어제 잔고 : "+ str(init_balance)+"\n\n" + "오늘 잔고 : " + str(today_bal)+"\n\n"+"수익률 : " + str(earn_percent)+"\n\n"+"수익 금액 : " + str(earn)
    post_message(myToken,"upbit-noti",noti_message)

    init_balance = today_bal

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_wallet_balance():
    wallet_list = upbit.get_balances()
    total_money = 0
    total_money += float(upbit.get_balance("KRW"))
    # get_amount("ALL")
    for i in wallet_list:
        cur_name = i['currency']
        cur_unit = i['unit_currency']
        bal = i['balance']
        ticker_name = cur_name+"-"+cur_unit
        if cur_name != "KRW":
            cur_price = pyupbit.get_current_price(ticker_name)
            total_money += bal*cur_price
            time.sleep(0.3)
        else:
            continue

    return total_money

try:
    upbit = pyupbit.Upbit(access, secret)
    print("login complete")

    # myKRW_balance = int(upbit.get_balance("KRW")) # 보유 현금 조회
    # myCOIN_balance = int(upbit.get_amount("ALL")) # 보유중인 코인 현금 환산 조회
    init_balance = get_wallet_balance

    # 매일 10시 알림
    schedule.every().day.at("10:00").do(restart)

    while True:
        schedule.run_pending()
        time.sleep(1)

except:
    print("login failed")
    print("please restart after check your key or token again")



