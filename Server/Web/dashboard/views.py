import json
import os
from pyvis import network as net
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse

from elasticsearch import Elasticsearch

es = Elasticsearch('http://192.168.65.128:9200/')

def index(request):
    # response_score = es.get(index='scorecheck_df', id=2)
    # wallet_score_df = pd.DataFrame.from_dict([response_score['_source']])

    print('[!]', request.path)

    # if(requset.path == '/dashboard/danger/')

    wallet_score_df = pd.read_csv("static/wallet/scorecheck_df.csv" ,encoding= 'utf-8')

    # response_cycle = es.get(index='all_cycle_df', id=2)
    # cycle_df = pd.DataFrame([response_cycle['_source']])

    cycle_df = pd.read_csv("static/cycle/all_cycle_df.csv" ,encoding= 'utf-8')


    # token_list = ['animal_society','ape_harbour_yachts','dogex','metavillains','the_evolving_forest']
    # for token_name in token_list:
    #     es_response = es.get(index=token_name, id=2)
    #     df = pd.DataFrame(es_response['_source'])
    #
    #     token_df = token_df.append(df)

    token_df = pd.DataFrame()
    cnt = 0
    path ="static/token/"
    file_list = os.listdir(path)
    for name in file_list:
        if(cnt == 0):
            token_df = pd.read_csv(path+name)
            cnt += 1
            continue

        token_df_tmp = pd.read_csv(path + name)
        token_df = pd.concat([token_df,token_df_tmp])


    token_df.reset_index(drop=True,inplace=True)
    transaction_num = len(token_df)
    wallet_num = len(wallet_score_df)

    # # 블랙홀 제거
    # idx = token_df[token_df['From'].str.slice(start=0, stop=10) == "Black Hole"].index
    # token_df.drop(idx, inplace=True)
    #
    # # 전송 제거
    # idx = token_df[token_df['Value'] == 0].index
    # token_df.drop(idx, inplace=True)

    trade_num = len(token_df)
    avg_trade_value = round(token_df['Value'].agg('mean'),2)
    fraud_trade = len(wallet_score_df[wallet_score_df['type']=="위험"])

    render_context = {'wallet_num': format(wallet_num,','), 'trade_num': format(trade_num,','), 'avg_trade_value': avg_trade_value,
                      'fraud_wallet': fraud_trade}


    # 막대 그래프 주간 거래횟수, 거래금액, 일간 거래횟수, 거래금액, 시간별 거래횟수, 거래금액 --- 평균을 계산해서 넣기
    week_trade_avg = wallet_score_df['week trade count'].agg('mean')
    week_value_avg = wallet_score_df['week value sum'].agg('mean')
    day_trade_avg = wallet_score_df['day trade count'].agg('mean')
    day_value_avg = wallet_score_df['day value sum'].agg('mean')
    hour_trade_avg = wallet_score_df['hour trade count'].agg('mean')
    hour_value_avg = wallet_score_df['hour value sum'].agg('mean')

    trade_avg =[round(week_trade_avg,2),round(week_value_avg,2),round(day_trade_avg,2),round(day_value_avg,2),
                round(hour_trade_avg,2),round(hour_value_avg,2)]
    render_2 = {'trade_avg':trade_avg}
    render_context.update(render_2)

    # 거래 비율  트랜잭션 총 개수, 순환 트랜잭션, 고액거래 트랜잭션 갯수, 자전거래 트랜잭션 갯수

    single_cycle_num = len(cycle_df[cycle_df['Cycle Length'] == 1])
    multi_cycle_num = len(cycle_df) - single_cycle_num
    high_value_num = len(token_df[token_df['Value'] >= 10])
    fraud_trade_num = single_cycle_num + multi_cycle_num + high_value_num

    fraud_trade_percent = (fraud_trade_num / trade_num) * 100
    single_cycle_percent = (single_cycle_num / fraud_trade_num) * 100
    multi_cycle_percent = (multi_cycle_num / fraud_trade_num) * 100
    high_value_percent = (high_value_num / fraud_trade_num) *100

    render_3 = {'single_cycle_num':round(single_cycle_percent,2),'multi_cycle_num':round(multi_cycle_percent,2),
                'high_value_num':round(high_value_percent,2),'normal_trade_num':round(fraud_trade_percent,2),'normal_trade':trade_num,
                'fraud_trade':fraud_trade_num,'high_value':high_value_num,'single_cycle':single_cycle_num,'multi_cycle':multi_cycle_num}
    render_context.update(render_3)

    # 지갑 비율
    multi_single_wallet = len(wallet_score_df[(wallet_score_df['multi cycle number']> 0) &
                                              (wallet_score_df['single cycle number']>0)])
    multi_wallet = len(wallet_score_df[(wallet_score_df['multi cycle number'] > 0) &
                                              (wallet_score_df['single cycle number'] == 0)])
    single_wallet = len(wallet_score_df[(wallet_score_df['multi cycle number'] == 0) &
                                              (wallet_score_df['single cycle number'] > 0)])
    # normal_wallet = len(wallet_score_df) - (multi_single_wallet + multi_wallet + single_wallet)

    cycle_sum = multi_wallet+single_wallet+multi_single_wallet
    multi_single_percent = round((multi_single_wallet/cycle_sum)*100)
    single_wallet_percent = round((single_wallet/cycle_sum)*100)
    multi_wallet_percent = round((multi_wallet/cycle_sum)*100)

    render_4 = {'multi_single_percent':multi_single_percent,'single_wallet_percent':single_wallet_percent,'multi_wallet_percent':multi_wallet_percent}
    render_context.update(render_4)


    # 지갑 점수

    danger_wallet_num = len(wallet_score_df[wallet_score_df['type']=="위험"])
    caution_wallet_num = len(wallet_score_df[wallet_score_df['type']=="관심"])
    normal_wallet_num = len(wallet_score_df[wallet_score_df['type']=="일반"])
    sum = danger_wallet_num + caution_wallet_num + normal_wallet_num

    danger_wallet_avg = round((danger_wallet_num /sum) * 100)
    caution_wallet_avg = round((caution_wallet_num / sum) * 100)
    normal_wallet_avg = round((normal_wallet_num / sum) * 100)

    render_5 = {'danger_wallet_avg':danger_wallet_avg,'caution_wallet_avg':caution_wallet_avg,'normal_wallet_avg':normal_wallet_avg}
    render_context.update(render_5)
    wallet_score_df = wallet_score_df.rename(columns={'value average':'value avg'})
    wallet_score_df = wallet_score_df[['type','score','wallet','cycle wallets']]
    wallet_score_df['wallet'] = wallet_score_df['wallet'].apply(lambda x: f'<a href="/table/wallet?wallet={x}">{x}</a>')
    wallet_score_table = wallet_score_df.to_html(index=False,table_id='datatablesSimple',render_links=True,escape=False)

    render_table = {'wallet_score_table':wallet_score_table}
    render_context.update(render_table)

    if(request.path == '/dashboard/danger/'):
        wallet_score_table = wallet_score_df[wallet_score_df['type']=="위험"].to_html(index=False,table_id='datatablesSimple',render_links=True,escape=False)

        return render(request, 'dashboard/danger.html', context={'wallet_score_table':wallet_score_table})
    

    return render(request, 'dashboard/index.html',context=render_context)
