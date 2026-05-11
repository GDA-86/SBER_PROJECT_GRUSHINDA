import pandas as pd


# Ктергория 1 - готовы совершить целевое действие 
# Финальные конверсии и подтвержденные контакты
hot_conversions = [
    "sub_submit_success",          # Успешная отправка заявки на подписку
    "sub_car_request_submit_click", # Клик по кнопке отправки запроса на авто
    "form_request_call_sent",      # Форма заказа звонка успешно отправлена
    "request_success",             # Успешный запрос
    "sub_car_claim_submit_click",  # Клик по подтверждению претензии/заявки
    "sber_id_auth_success",        # Успешная авторизация через Сбер ID
    "phone_auth_success",          # Успешный вход по номеру телефона
    "code_sms_entered_success",    # Правильный ввод SMS-кода
    "success_ad_creation",         # Успешное создание объявления
    "user gave contacts during chat", # Пользователь оставил контакты в чате
    "callback requested"           # Заказан обратный звонок
]

# Финансовые и кредитные действия 
financial_actions = [
    "setelem_credit_form_button",  # Клик по кнопке кредитной формы Сетелем
    "click_setelem_credit",        # В кредит у Сетелем
    "click_on_credit_btn",         # Клик по кнопке "В кредит"
    "click_pos_credit",            # Клик по POS кредитованию (экспресс кредит )
    "click_credit",                # го в кредиттный раздел 
    "greenday_sub_submit_success"  # Заявка по акции Green Day согласована
]



# Заполнение формы 
warm_intent = [
    "click_free_car_selection",    # Запрос на бесплатный подбор авто
    "click_on_help_in_finding",    # Клик "Помочь с поиском"
    "quiz_start",                  # Старт подбора
    "start_auth",                  # Начало процесса авторизации
    "phone_entered",               # Введен номер телефона 
    "name_entered",                # Введено имя
    "sub_car_claim_click",         # Клик по оформлению заявки
    "click_on_subscription",       # Клик по кнопке "Подписаться"
    "calculate",                   # Нажата кнопка "Рассчитать"
    "client initiate chat"         # Пользователь первым написал в чат
]

# Ктергория 2 - почти готовы  
# Просмотр конкретных объектов
view_actions = [
    "go_to_car_card",              # Переход в карточку автомобиля
    "view_new_card",               # Просмотр карточки нового авто
    "view_used_card",              # Просмотр карточки б/у авто
    "view_card",                   # Общий просмотр карточки
    "sub_car_page"                 # Просмотр страницы подписки
]


# Фильтры и поиск 
search_filters = [
    "search_form_mark_select",     # Выбор марки
    "search_form_model_select",    # Выбор модели
    "search_form_cost_from",       # Цена ОТ
    "search_form_cost_to",         # Цена ДО
    "search_form_year_from",       # Год выпуска ОТ
    "search_body_type",            # Выбор типа кузова
    "search_engine",               # Выбор типа двигателя
    "search_kpp",                  # Выбор коробки передач
    "search_drive",                # Выбор привода
    "sub_view_cars_click"          # Клик по кнопке "Посмотреть все авто"
]


# Ктергория 3 -  не готовы 
# Поиск информации 
awareness_actions = [
    "potential_banner_click",      # Клик по акционному баннеру
    "sub_banner_click",            # Клик по баннеру подписки
    "click_on_menu",               # Клик по меню навигации
    "sub_view_faq_click",          # Просмотр часто задаваемых вопросов
    "scrolling_to_advantages",     # Скролл до блока преимуществ
    "click_on_logo",               # Клик по логотипу
    "go_to_special_offers"         # Переход в спецпредложения
    "tinkoff_credit_form_button",  # Тинькофф - ????
    "sravni_credit_form_button"    # Сравни.ру - ????
]



def gda_set_moda(data, col, mode=1):
    if mode == 1:
        data[col].fillna(data[col].mode()[0], inplace=True)
        
        print(f'{col}: {data[col].mode()[0]}')

    if mode == 2:
#       Моды на которых учили 
        mode_s = {
       'utm_source': 'ZpYIoDJMcFzVoPFsHGJL',
       'utm_medium': 'banner',
       'utm_campaign': 'LTuZkdKfxRGVceoWkVyg',
       'utm_adcontent': 'JNHcPlZPxEMWDnRiyoBf',
       'device_brand': 'Apple'
                }

        data[col].fillna(mode_s[col] , inplace=True)
    return data 


def gda_drop_col(data, col): 
    data.drop([col], axis = 1, inplace=True)
    return data



def gda_set_date_feature(data, col_date, col_time): 
    
    data['visit_datetime'] = pd.to_datetime(data[col_date] + ' ' + data[col_time])

    date_time = data['visit_datetime'].dt

    # Временные отрезки
    data['visit_hour']   = date_time.hour           
    data['visit_minute'] = date_time.minute       
    data['visit_second'] = date_time.second      


    # Календарные признаки
    data['visit_day_of_week'] = date_time.dayofweek  
    data['visit_month']       = date_time.month          
    data['visit_is_year_end'] = date_time.is_year_end.astype(int)  
    
        # Периоды суток (Custom feature)
    def get_part_of_day(h):
        if 6 <= h < 12: return 'morning'
        elif 12 <= h < 18: return 'afternon'
        elif 18 <= h < 24: return 'evening'
        else: return 'night'

    data['visit_part_of_day'] = data['visit_hour'].apply(get_part_of_day) 

    data.drop([col_date], axis = 1, inplace=True)
    data.drop([col_time], axis = 1, inplace=True)
    data.drop(['visit_datetime'], axis = 1, inplace=True)

    return data



def gda_set_mult(data, col): 
    data['screen_area'] = data[col].str.split('x').apply(lambda x: float(x[0]) * float(x[1]) if isinstance(x, list) and len(x) == 2 else 0.0)

    data.drop([col], axis = 1, inplace=True)
    return data


def gda_leave_only_top_val(data, col, n, mode=1):
    cat_uniq_data = pd.DataFrame()
    
    if mode == 1:
        # Находим 20 самых топовых значений  
        top_n = data[col].value_counts().nlargest(n).index

    if mode == 2:
        if not cat_uniq_data:  # type: ignore
            cat_uniq_data = pd.read_csv('data/cat_uniq_data.csv')
        top_n = cat_uniq_data[col].value_counts().nlargest(n).index

    top_n = top_n.drop(['(none)', '(not set)', 'other'], errors='ignore') # type: ignore
    # их оставим, остальное заменяем на 'other'
    data[col] = data[col].where(data[col].isin(top_n), 'other')
    return data



def gda_calc_conversion(session, hits, groupby_col, key_cols, cols_pref):
    col_count_name = f'{cols_pref}_count'
    col_is_name    = f'{cols_pref}_is'
    # кол-во целевых action за сессию 
    conv_counts = hits[hits[groupby_col].isin(hot_conversions)].groupby(key_cols).size()

    # добавляем столбец 
    session[col_count_name] = session[key_cols].map(conv_counts).fillna(0).astype(int)

    # добавляем бинар-признак - было или нет 
    session[col_is_name] = (session[col_count_name] > 0).astype(int)

    session.drop([col_count_name], axis = 1, inplace=True)
    return session


def gda_main_proc(go_session, go_hits):

    go_session = gda_drop_col(go_session, 'client_id')
    go_session = gda_drop_col(go_session, 'utm_keyword')
    go_session = gda_drop_col(go_session, 'device_os' )
    go_session = gda_drop_col(go_session,  'device_model')


    go_session = gda_set_moda(go_session, 'utm_source',mode=1)
    go_session = gda_set_moda(go_session, 'utm_medium',mode=1)
    go_session = gda_set_moda(go_session, 'utm_campaign',mode=1)
    go_session = gda_set_moda(go_session, 'utm_adcontent',mode=1)
    go_session = gda_set_moda(go_session, 'device_brand',mode=1)

    go_session = gda_set_date_feature(go_session, 'visit_date', 'visit_time')


    go_session = gda_set_mult(go_session, 'device_screen_resolution')

    go_session = gda_leave_only_top_val(go_session, 'geo_city', 20 , mode=1 )
    go_session = gda_leave_only_top_val(go_session, 'geo_country', 10 , mode=1  )
    go_session = gda_leave_only_top_val(go_session, 'device_browser', 10 , mode=1 )
    go_session = gda_leave_only_top_val(go_session, 'device_brand', 10 , mode=1 )
    go_session = gda_leave_only_top_val(go_session, 'utm_source', 10 , mode=1 )
    go_session = gda_leave_only_top_val(go_session, 'utm_medium', 10 , mode=1 )
    go_session = gda_leave_only_top_val(go_session, 'utm_campaign', 15 , mode=1 )
    go_session = gda_leave_only_top_val(go_session, 'utm_adcontent', 10 , mode=1 )

    go_session = gda_calc_conversion(go_session, go_hits, 'event_action', 'session_id', 'target')

    go_session = gda_drop_col(go_session, 'session_id')

    return go_session