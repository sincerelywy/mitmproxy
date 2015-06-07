# -*- coding: utf-8 -*-
from __future__ import absolute_import
import urwid
from . import common, searchable
from .. import utils
import urlparse
import re, urllib2

def parseurl(state, flow):

	#test_url = "http://api.meituan.com/group/v1/poi/1577016?fields=phone,markNumbers,cityId,addr,lng,hasGroup,subwayStationId,cates,frontImg,chooseSitting,wifi,avgPrice,style,featureMenus,avgScore,name,parkingInfo,lat,cateId,introduction,showType,areaId,districtId,preferent,lowestPrice,cateName,areaName,zlSourceType,campaignTag,mallName,mallId,brandId,ktv,geo,historyCouponCount,recommendation,iUrl,isQueuing,payInfo,sourceType,abstracts,groupInfo,isSuperVoucher,discount,isWaimai,collectionDeals,tour&__vhost=api.mobile.meituan.com&utm_source=undefined&utm_medium=android&utm_term=260&version_name=5.6&utm_content=000000000000000&utm_campaign=AgroupBgroupC0E0Fab_a550poi_xxyl__b__leftflow___ab_a550poi_lr__d__leftflow___ab_a_group_5_6_searchkuang__a__a___ab_a_group_5_5_onsite__b__b___ab_a550poi_shfw__b__leftflow___ab_a_trip_zhoubiandeallist__b__leftflow___ab_a_group_5_4_poidetaildeallist__a__a___ab_a502poi__b__f___ab_a550poi_ktv__d__jGhomepage_category6_195__a0&ci=1&uuid=2C2C0ECD557F366849954BEF88D0017AA215FA24A8ECAA81361AAA1DEFA7320D&msid=0000000000000001433660501995&__skck=09474a920b2f4c8092f3aaed9cf3d218&__skts=1433665625596&__skua=b1cda2b94d7f29f3e15fb16fa0e83bd7&__skno=e5854518-08fd-409c-a233-13975ad41c21&__skcy=E0ZiIzsd%2BZ%2BY0%2Bn1iy9gd6wMnk4%3D"
	text = []
	parts = []
	# Raw URL
	url_raw = flow.request.url
	text.append(urwid.Text([("head", "Raw URL:")]))
	parts = [
		["Method", flow.request.method],
		["URL", url_raw],
	]
	text.extend(
		common.format_keyvals(parts, key="key", val="text", indent=4)
	)
	
	# Parse the URL
	url_parse = urlparse.urlparse(url_raw)
	text.append(urwid.Text([("head", "Parse:")]))
	parts = [
		["Scheme", url_parse.scheme],
		["Netlocation", url_parse.netloc],
		["Path", url_parse.path],
		["Params", url_parse.params],
		["QueryString", url_parse.query],
		["Fragment", url_parse.fragment]
	]
	text.extend(common.format_keyvals(parts, key="key", val="text", indent=4))

	# parse the query string
	text.append(urwid.Text([("head", "QueryString:")]))
	parts = []
	query_raw = urlparse.parse_qs(url_parse.query)
	for k, v in query_raw.iteritems():
		parts.append([k.upper(), v])
	text.extend(common.format_keyvals(parts, key="key", val="text", indent=4))

	# Parse the utm_campaign
	text.append(urwid.Text([("head", "utm_campaign:".upper())]))
	parts = []
	utm_params = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
	utm_campaign = ''.join(query_raw['utm_campaign']) # list to string
	for param in utm_params:
		m = re.match(r'.*' + param + '([^A-Z]+)', utm_campaign)
		if m:
			parts.append([param, m.group(1)])
	text.extend(common.format_keyvals(parts, key="key", val="text", indent=4))

	# parse stid and ctpoi
	config_parse_url = 'http://config.mobile.meituan.com/api/v1/strategy/detail/'
	m = re.match(r'.*' + 'C([^A-Z]+)', utm_campaign)
	if m and cmp(m.group(1), '0') != 0:
		text.append(urwid.Text([("head", "STID:")]))
		stid = re.match(r'(\d+)', m.group(1))
		response = urllib2.urlopen(config_parse_url + stid.group(1))
		parts = [
			#[stid.group(1) ,''.join(utils.pretty_json(response.read())).decode('unicode_escape')]
			# 本来想使用函数格式化Json，但是格式化后还厚很多行，而且要输出中文还得转化成字符串，所以直接输出字符串
			[stid.group(1) ,response.read()]
		]
		text.extend(common.format_keyvals(parts, key="key", val="text", indent=4))

	m = re.match(r'.*' + 'E([^A-Z]+)', utm_campaign)
	if m and cmp(m.group(1), '0') != 0:
		text.append(urwid.Text([("head", "CT_POI:")]))
		ct_poi = re.match(r'(\d+)', m.group(1))
		response = urllib2.urlopen(config_parse_url + ct_poi.group(1))
		parts = [
			#[ct_poi.group(1) ,utils.pretty_json(response.read()).decode('unicode_escape')]
			[ct_poi.group(1) ,response.read()]
		]
		text.extend(common.format_keyvals(parts, key="key", val="text", indent=4))


	return searchable.Searchable(state, text)