import os
import django
import datetime
from dateutil.parser import parse as dateparse
import datetime as pydatetime
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "save_your_ingredient.settings")
django.setup()

from recipe.models import Recipe
from stock.models import Stock


# list to json
def list_to_json(list):
    lst = []
    for pn in list:
        d = {}
        d["id"] = pn
        lst.append(d)
    return json.dumps(lst)


# 사용자 재고 리스트 가져오기
def get_stock_list():
    all_stock = Stock.objects.all() # filter 넣어야함: .objects.filter(author=request.user)
    stock_list = []
    for stock in all_stock:
        stock_list.append(stock.ingredient_id.id)
    return stock_list


# 재료 기반 레시피 추천
def recommend_ingredient():
    all_recipes = Recipe.objects.all()
    recommend_recipe_id_list = []
    stock_list = get_stock_list()
    # print(stock_list)
    for recipe in all_recipes:
        if not(recipe.ingredient_ids):
            continue
        ss = recipe.ingredient_ids.split(',')
        re_list = []
        for s in ss:
            re_list.append(int(s))
        if len(re_list) != 0 and len(set(stock_list) - set(re_list)) == 0:# and len(set(re_list) - set(stock_list)) < 10:
            recommend_recipe_id_list.append(recipe.reci_id)
    if len(recommend_recipe_id_list) < 10:
        for recipe in all_recipes:
            if not (recipe.ingredient_ids):
                continue
            ss = recipe.ingredient_ids.split(',')
            re_list = []
            for s in ss:
                re_list.append(int(s))
            if len(re_list) != 0 and 0 < len(set(stock_list) - set(re_list)) < 2:  # and len(set(re_list) - set(stock_list)) < 10:
                if len(recommend_recipe_id_list) < 20:
                    recommend_recipe_id_list.append(recipe.reci_id)
    if len(recommend_recipe_id_list) < 8:
        for recipe in all_recipes:
            if not (recipe.ingredient_ids):
                continue
            ss = recipe.ingredient_ids.split(',')
            re_list = []
            for s in ss:
                re_list.append(int(s))
            if len(re_list) != 0 and 1 < len(set(stock_list) - set(re_list)) < 3:
                if len(recommend_recipe_id_list) < 20:
                    recommend_recipe_id_list.append(recipe.reci_id)
    result = {}
    result['ids'] = recommend_recipe_id_list
    return result


def parse_korean_type_date(d, assert_min_year=1900):
    """
    날짜문자열(년도가 앞, 일자가 뒤 형태)을 입력받아 datetime 인스턴스를 반환
    파싱이 불가능한 경우 또는 assert_min_year년도 이전인 경우 None 반환
    """
    try:
        d_parsed = dateparse(d, yearfirst=True, dayfirst=False)
        if d_parsed.year < assert_min_year: # 보장해야하는 최소 년도보다 작은 경우 None 반환
            return None
        else:
            return d_parsed
    except: # 파싱이 불가능한 경우 None 반환
        return None


def get_time_diff(start_date, end_date, unit='second'):
    """
    datetime 인스턴스의 시작과 종료일자를 받아 시간차이를 반환
    unit이 day인 경우 일수 차이 반환
    unit이 second 등일 경우 초 차이 반환
    """
    assert isinstance(start_date, pydatetime.datetime), 'start_date required datetime instance'
    assert isinstance(end_date,   pydatetime.datetime), 'end_date   required datetime instance'
    _timedelta = end_date - start_date
    if unit=='day':
        return abs(_timedelta.days)
    return abs((_timedelta.days * (_timedelta.max.seconds + 1)) + _timedelta.seconds)


# 유통기한 기반 레시피 추천
def recommend_expiration_date():
    now = datetime.datetime.now()
    nowDates = now.strftime('%Y-%m-%d')
    nowDate = nowDates.replace('-', '')
    all_stocks = Stock.objects.all()
    expiration_list = []
    for stock in all_stocks:
        stock_time = str(stock.expiration_date).replace('-', '')
        ex_day = get_time_diff(parse_korean_type_date(nowDate), parse_korean_type_date(stock_time), unit='day')
        if ex_day < 5:
            expiration_list.append(stock.ingredient_id.id)
    # print(expiration_list)

    recommend_recipe_list = []
    all_recipes = Recipe.objects.all()
    for recipe in all_recipes:
        if not(recipe.ingredient_ids):
            continue
        ss = recipe.ingredient_ids.split(',')
        re_list = []
        for s in ss:
            re_list.append(int(s))
        if len(re_list) != 0 and len(set(expiration_list) - set(re_list)) == 0:
            if len(recommend_recipe_list) < 20:
                recommend_recipe_list.append(recipe.reci_id)
        if recommend_recipe_list:
            a = Recipe.objects.filter(reci_id=recommend_recipe_list[0])
    print(len(recommend_recipe_list))
    result = dict()
    result['ids'] = recommend_recipe_list

    return result
#
#
# # 만개사이트 인기 레시피 파싱후 레시피 추천
# recommend_expiration_date()
recommend_ingredient()
# a = Recipes.objects.filter(reci_id=new[0])
# for n in new[1:]:
#     b = Recipes.objects.filter(reci_id=n)
#     print(a,b)
#     result = a.union(b, all=True)
# print(result)
# for reci in recies:
#     if str(reci)