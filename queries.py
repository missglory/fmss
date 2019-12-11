import psycopg2
# conn = psycopg2.connect(dbname='testdb', user='postgres',
                        # password='1234', host='localhost')
# cursor = conn.cursor()
 
 
### 1 Запрос
def get_providers_by_good(cursor, good_id: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    '''
       1. Получить список поставщиков по товару
       Inputs:
           good_id: номер товара
           time_s: начало периода
           time_e: конец периода
   '''
 
    cursor.execute("""
           select p.* from providers p
           inner join deliveries d
           on d.provider = p.id
           where good = %s
           and date_trunc('day', d.ts) between %s and %s
       
       """, (str(good_id), time_s, time_e))
    return cursor.fetchall()
 
 
def get_providers_by_count(cursor, count: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    '''
       1.Получить список поставщиков по количеству товара
       Inputs:
           count: количество товара
           time_s: начало периода
           time_e: конец периода
   '''
 
    cursor.execute("""
           select p.* from providers p
           inner join deliveries d
           on d.provider = p.id
           where d.count >= %s
           and date_trunc('day', d.ts) between %s and %s
 
       """, (str(count), time_s, time_e))       
    return cursor.fetchall()
### конец 1го запроса
 
 
###2ой запрос
def get_customers_by_good(cursor, good_id: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       2.Получить покупателей купивших некоторый вид товара
       Inputs:
           good_id: номер товара
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
           select c.* from customers c
           inner join sales s
           on s.customer = c.id
           where date_trunc('day', s.ts) between %s and %s
           and s.good = %s
 
       """, (time_s, time_e, str(good_id)))
    return cursor.fetchall()
 
def get_customers_by_value(cursor, count: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       2.Получить покупателей купивших определенное количество товара
       Inputs:
           count: необходимое количество товара
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
           select c.* from customers c
           inner join sales s
           on s.customer = c.id
           where date_trunc('day', s.ts) between %s and %s
           and s.count >= %s
 
       """, (time_s, time_e, str(count)))
    return cursor.fetchall()
### конец второго запроса
 
### 3ий запрос
def get_goods(cursor, store_id: int):
    """
       3.Получить товары для определенного магазина
       Inputs:
           store_id: необходимое количество товара
   """
 
    cursor.execute("""
           select g.name, w.count, w.price, w.store as store_id from stores s
           inner join warehouse w
           on w.store = s.id
           inner join goods g
           on w.good = g.id
           where s.id = %s
 
       """, (str(store_id), ))
    return cursor.fetchall()
### конец 3го запроса
 
# 4ый запрос
def get_good_info(cursor, good_id: int):
    """
       4.Получить инфо по товару во всех точках
       Inputs:
           good_id: id товара
   """
 
    cursor.execute("""
           select w.*, g.name from warehouse w
           inner join goods g
           on g.id = w.good
           where
           w.id = %s
 
       """, (str(good_id), ))
    return cursor.fetchall()

def get_good_info_by_store_type(cursor, good_id: int, store_type: int):
    """
       4.Получить инфо по товару в точках определенного типа
       Inputs:
           good_id: необходимое количество товара
           store_type: тип точки
   """
 
    cursor.execute("""
       select w.*, g.name from warehouse w
       inner join goods g
       on g.id = w.good
       inner join stores s
       on w.store = s.id
       where g.id = %s
       and s.type = %s
 
       """, (str(good_id), str(store_type)))
    return cursor.fetchall()

 
def get_good_info_by_store_id(cursor, good_id: int, store_id: int):
    """
       4.Получить инфо по товару конкретной точке
       Inputs:
           good_id: необходимое количество товара
           store_id: id точки
   """
 
    cursor.execute("""
       select w.*, g.name from warehouse w
       inner join goods g
       on g.id = w.good
       inner join stores s
       on w.store = s.id
       where g.id = %s
       and s.id = %s
 
       """, (str(good_id), str(store_id)))
    return cursor.fetchall()

 
### конец 4го запроса
 
### начало 5го запроса
 
def get_seller_info(cursor, seller_id: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       5.Получить инфо по продавцу по всем точкам
       Inputs:
           seller_id: необходимое количество товара
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
       select * from sales s
       where s.seller = %s
       and date_trunc('day', s.ts) between %s and %s
 
       """, (str(seller_id), time_s, time_e))
    return cursor.fetchall()
 
def get_seller_info_by_store_type(cursor, seller_id: int, store_type: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       5.Получить инфо по продавцу по точкам определенного типа
       Inputs:
           seller_id: необходимое количество товара
           store_type: тип точки
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
       select * from sales s
       inner join stores st
       on st.id = s.store
       where s.seller = %s
       and st.type = %s
       and date_trunc('day', s.ts) between %s and %s
       """, (str(seller_id), str(store_type), time_s, time_e))
    return cursor.fetchall()
 
###конец 5го запроса
 
###начало 6го запроса
 
def get_seller_info_by_store_id(cursor, seller_id: int, store_id: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       6.Получить инфо по продавцу по точкам определенного типа
       Inputs:
           seller_id: необходимое количество товара
           store_type: тип точки
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
       select * from sales s
       where s.seller = %s
       and s.store = %s
       and date_trunc('day', s.ts) between %s and %s
       """, (str(seller_id), str(store_id), time_s, time_e))
    return cursor.fetchall()
 
### конец 6го запроса
 
### начало 7го запроса
def get_good_count(cursor, good_id: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       7.Получить инфо по товару во всех точках
       Inputs:
           seller_id: необходимое количество товара
           time_s: начало периода
           time_e: конец периода
    """
 
    cursor.execute("""
           select s.count, st.id, s.customer, s.seller, s.store from sales s
           inner join stores st
           on st.id = s.store
           where s.good = %s
           and date_trunc('day', s.ts) between %s and %s
       """, (str(good_id),  time_s, time_e))
    return cursor.fetchall()
 

def get_good_count_by_store_type(cursor, good_id: int, store_type:int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       7.Получить инфо по товару по типу точки
       Inputs:
           seller_id: необходимое количество товара
           store_type: тип торговой точки
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
               select s.count, st.id, s.customer, s.seller, s.store from sales s
               inner join stores st
               on st.id = s.store
               where s.good = %s
               and st.type = %s
               and date_trunc('day', s.ts) between %s and %s
       """, (str(good_id), str(store_type), time_s, time_e))
    return cursor.fetchall()
 
def get_good_count_by_store(cursor, good_id: int, store_id:int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       7.Получить инфо по товару в точке
       Inputs:
           seller_id: необходимое количество товара
           store_id: номер торговой точки
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
               select s.count, st.id, s.customer, s.seller, s.store from sales s
               inner join stores st
               on st.id = s.store
               where s.good = %s
               and st.id = %s
               and date_trunc('day', s.ts) between %s and %s
       """, (str(good_id), str(store_id), time_s, time_e))
    return cursor.fetchall()
 
### конец 7го запроса
 
### начало 8го запроса
def get_sellers_salaries(cursor, ):
    """
       8.Получить инфо по зарплатам
       Inputs:
           None
   """
 
    cursor.execute("""
           select s.name, s.salary, st.store from sellers s
           inner join staff st
           on st.seller = s.id
       """, ())
    return cursor.fetchall()
 
def get_sellers_salaries_by_store_type(store_type: int):
    """
       8.Получить инфо по товару по типу точки
       Inputs:
           store_type: тип точки
    """
    cursor.execute(cursor, """
           select s.name, s.salary, st.store from sellers s
           inner join staff st
           on st.seller = s.id
           inner join stores str
           on str.id = st.store
           where str.type = %s
       """, (str(store_type), ))
    return cursor.fetchall()
 
def get_sellers_salaries_by_store_id(cursor,store_id: int):
    """
       8.Получить инфо по товару в точке
       Inputs:
           store_id: точка
    """
    cursor.execute("""
           select s.name, s.salary, st.store from sellers s
           inner join staff st
           on st.seller = s.id
           where st.store = %s
       """, (str(store_id), ))
    return cursor.fetchall()
### конец 8го запроса
 
### начало 9го запроса
def get_deliveries(cursor,good_id: int, provider_id: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       9.Получить инфо по зарплатам
       Inputs:
           provider_id: номер поставщика
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
           select * from deliveries d
           where d.good = %s
           and d.provider = %s
           and date_trunc('day', d.ts) between %s and %s
       """, (str(good_id), str(provider_id), time_s, time_e))
    return cursor.fetchall()
 
### конец 9го запроса
 
### начало 10го запроса
def get_ratio_square(cursor, id: int):
    '''
       10.Получить отношение проданных товаров к площади точки
 
       Input:
           id: номер тороговой точки
       Output:
           Таблица с полями: seller, store, ratio (то самое отношение)
   '''
    cursor.execute("""
           select s.seller, s.store, s.count::float / st.total_square as ratio from sales s
           inner join stores st
           on st.id = s.store
           where s.store = %s
       """, (str(id), ))
    return cursor.fetchall()
 
def get_ratio_halls(cursor, id: int):
    '''
       10.Получить отношение проданных товаров к числу залов
 
       Input:
           id: номер тороговой точки
       Output:
           Таблица с полями: seller, store, ratio (то самое отношение)
   '''
    cursor.execute("""
           select s.seller, s.store, s.count / st.halls_number as ratio from sales s
           inner join stores st
           on st.id = s.store
           where s.store = %s
       """, (str(id), ))
    return cursor.fetchall()
 
def get_ratio_prilavok(cursor, id: int, prilavok_type: int):
    '''
       10.Получить отношение проданных товаров к числу прилавков определенного типа
 
       Input:
           id: номер тороговой точки
           prilavok_type: тип прилавка
       Output:
           Таблица с полями: seller, store, ratio (то самое отношение)
   '''
    cursor.execute("""
           select s.seller, s.store, s.count::float / ps.count as ratio from sales s
           inner join stores st
           on st.id = s.store
           inner join prilavok_stores ps
           on ps.store = s.store
           inner join prilavok_type pt
           on pt.id = ps.prilavok
           where s.store = %s
            and  pt.id = %s
       """, (str(id), str(prilavok_type)))
    return cursor.fetchall()
 
### конец 10го запроса
 
### начало 11го запроса
def get_profit(cursor, id: int, p_start: str = '2019-01-01', p_end: str = '2019-12-31'):
    '''
       11.Отношение прибыли к затратам по конкретной точке за определенный период
 
       Input:
           id: номер точки
           p_start: начало периода отчета
           p_end: конец периода отчета
       Output:
           число - отношение прибыли к убыли
   '''
 
    cursor.execute("""
               with incomes as (select s.store, sum(s.count * w.price)
                                    from sales s
                                    inner join warehouse w
                                    on w.store = s.store
                                    where s.store = %s
                                    and s.ts between %s and %s
                                    group by s.store
                                    ),
               outcomes as (select s.store, sum(ss.salary)
                                from staff s
                                inner join sellers ss
                                on ss.id = s.seller
                                where s.store = %s
                                group by s.store
                                ),
               taxes as (select ex.store, sum(ex.amount)
                             from expenses ex
                             where ex.store = %s
                             and ex.ts between %s and %s
                             group by ex.store)
               select i.sum::float / (o.sum + t.sum) as ratio from incomes i
               inner join outcomes o
               on o.store = i.store
               inner join taxes t
               on t.store = i.store
       """, (str(id), p_start, p_end, str(id), str(id), p_start, p_end))
    return cursor.fetchall()
 
### конец 11го запроса
 
### начало 12го запроса
def get_deliveries(cursor,id: int):
    """
       12.Получить инфо по доставке
       Inputs:
           id: точка
    """
    cursor.execute("""
               select * from deliveries d
               where d.id = %s
       """, (str(id), ))
    return cursor.fetchall()
 
### конец 12го запроса
 
### начало 13го запроса
def get_customers_info(cursor,good_id: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       13.Получить инфо по товару во всех точках
       Inputs:
           good_id: номер товара
           time_s: начало периода
           time_e: конец периода
    """
 
    cursor.execute("""
           select * from sales s
           where s.good = %s
           and date_trunc('day', s.ts) between %s and %s
       """, (str(good_id), time_s, time_e))
    return cursor.fetchall()
 
def get_customers_info_by_store(cursor,good_id: int, store_id: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       13.Получить инфо по товару в конкретной точке
       Inputs:
           good_id: номер товара
           store_id: номер магазина
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
               select * from sales s
               where s.good = %s
               and s.store = %s
               and date_trunc('day', s.ts) between %s and %s
       """, (str(good_id), str(store_id), time_s, time_e))
    return cursor.fetchall()
 
def get_customers_info_by_store_type(cursor, good_id: int, store_type: int, time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       13.Получить инфо по товару по типу точки
       Inputs:
           good_id: номер товара
           store_id: номере магазина
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
               select s.* from sales s
               inner join stores st
               on st.id = s.store
               where s.good = %s
               and st.type = %s
               and date_trunc('day', s.ts) between %s and %s
       """, (str(good_id), str(store_type), time_s, time_e))
    return cursor.fetchall()
### конец 13го запроса
 
### начало 14го запроса
def get_active_customers(cursor):
    """
       14.Самые активные покупатели по всем точкам
       Inputs:
    """
    cursor.execute("""
               select s.customer, count(s.customer) from sales s
               group by s.customer
               order by count desc
               limit 5
       """, ())
    return cursor.fetchall()
 
def get_active_customers_by_store(cursor, store_id: int):
    """
       14.Самые активные покупатели по конкретной точке
       Inputs:
           store_id: номер магазина
    """
    cursor.execute("""
               select s.customer, count(s.customer) from sales s
               where s.store = %s
               group by s.customer
               order by count desc
               limit 5
       """, (str(store_id)))
    return cursor.fetchall()
 
def get_active_customers_by_store_type(cursor, store_type: int):
    """
       14.Самые активные покупатели по типу точки
       Inputs:
           store_type: тип магазина
    """
 
    cursor.execute("""
               select s.customer, count(s.customer)
               from sales s
               inner join stores st
               on st.id = s.store
               where st.type = %s
               group by s.customer
               order by count desc
               limit 5
       """, (str(store_type)))
    return cursor.fetchall()
 
###конец 14го запроса
 
### начало 15го запроса
def get_sales_info(cursor, store_id:int,  time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       15.Инфо о продажах в конкретном магазине
       Inputs:
           store_id: номере магазина
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
               select * from sales s
               where s.store = %s
               and date_trunc('day', s.ts) between %s and %s
       """, (str(store_id), time_s, time_e))
    return cursor.fetchall()
 
def get_sales_info_by_store_type(cursor, store_type: int,  time_s: str = '2019-01-01', time_e: str = '2019-12-31'):
    """
       15.Инфо о продажах во всех магазинах типа
       Inputs:
           store_type: номере магазина
           time_s: начало периода
           time_e: конец периода
   """
 
    cursor.execute("""
               select * from sales s
               inner join stores st
               on st.id = s.store
               where st.type = %s
               and date_trunc('day', s.ts) between %s and %s
       """, (str(store_type), time_s, time_e))
    return cursor.fetchall()

def select_table(cursor, tablename: str):
    cursor.execute(f"select * from {tablename}", ())
    return cursor.fetchall()
