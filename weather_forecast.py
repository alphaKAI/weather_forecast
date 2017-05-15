#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import lxml.html
import re
import sys


#TODO: 無駄に取得しないようにする(更新時間を過ぎていたら取得。そうでなければ前回の結果を利用。)
# 更新頻度 :> 0,2,4,6,8,10,12,14,16,18,20,22時頃に更新。

CHACHE = True  # 一時ファイルを生成するので注意
DEBUG  = False
ESC_COL_OFF = '\033[0m'

# 任意の地点のtenki.jpの「３時間天気」のページのURLを設定する
URL = 'http://www.tenki.jp/forecast/3/11/4020/8220.html'  # つくば市


dom = lxml.html.parse(URL)
announce_datetime = dom.xpath(r'//*[@id="point_announce_datetime"]')[0].text
point_info = dom.xpath(r'//*[@id="pinpoint_weather_name"]')[0].text
point_name = re.match(ur'(.+)のピンポイント天気', point_info).group(1)


def print_weather_col(weatherstr, past=False):
    def hexcol_to_esc(hexcolstr):
        colint = int(hexcolstr, 16)
        b = colint % 256
        colint/=256
        g = colint % 256
        colint/=256
        r = colint

        if past:
            r *= 0.475
            g *= 0.475
            b *= 0.475

        return '\033[1;38;2;' + '%d;%d;%d' % (r, g, b) + 'm'

    ESC_COL_UNKNOWN = '\033[1;7;31m'

    # WEATHER_TO_ESC_COLOR = {
    #   u'晴れ':'\033[31m',
    #   u'曇り':'\033[37m',
    #   u'小雨':'\033[36m',
    #   u'弱雨':'\033[34m',
    #   u'雨':'\033[1;34m',
    #   'PAST':'\033[2m',
    # }

    ## 24bitカラー対応端末のみ
    WEATHER_TO_ESC_COLOR = {
      u'晴れ' : hexcol_to_esc('ffc235'),
      u'曇り' : hexcol_to_esc('bbbbbb'),
      u'小雨' : hexcol_to_esc('80c7e6'),
      u'弱雨' : hexcol_to_esc('77abea'),
      u'雨'   : hexcol_to_esc('437ce6'),
    }

    sys.stdout.write(WEATHER_TO_ESC_COLOR.get(weatherstr, ESC_COL_UNKNOWN)
     + weatherstr.rjust(2, u'　') + ESC_COL_OFF + ' ')


if DEBUG:
    print '====DEBUG================'
    a = [u'晴れ', u'曇り', u'小雨', u'弱雨', u'雨']
    for k in a:
        print_weather_col(k, False)
    print ''
    for k in a:
        print_weather_col(k, True)
    print ''
    print_weather_col(u'HOGE')
    print ''
    print '========================='


print '----------------------------------------------------------------------------'
print point_name + u'の天気 (' + announce_datetime + ')'
print u'                    03時 06時 09時 12時 15時 18時 21時 24時'

for k in range(2):  # 今日、明日の天気を表示

    date = dom.xpath(r'//*[@id="bd-main"]/div[1]/table[%d]/thead/tr/td/div/p' % (k + 1))[0].text
    tds  = dom.xpath(r'//*[@id="bd-main"]/div[1]/table[%d]/tbody/tr[3]/td' % (k + 1))
    print date + ' : ',

    for td in tds:
        weather = td[1].text

        if re.match('.*past.*', td[0].attrib['src']):
            print_weather_col(weather, True)
        else:
            print_weather_col(weather, False)

    print ''  # \n

print "----------------------------------------------------------------------------"
