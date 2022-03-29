from peewee import *
from sys import argv
import datetime
import random
import os.path
import pytest


db_name = 'database.db'
db = SqliteDatabase(db_name)

class BaseModel(Model):
    class Meta:
        database = db


class Clients (BaseModel):
    name = CharField()
    city = CharField()
    address = CharField()


class Orders (BaseModel):
    clients = ForeignKeyField(Clients, backref='client')
    date = DateTimeField()
    amount = IntegerField()
    description = CharField()


def init_db():
    # ---Create or delete database---

    if os.path.exists(db_name) == True:
        os.remove(db_name)
        print('--- DataBase delete ---')
    db.create_tables([Clients, Orders], safe=True)
    print('--- DataBase create ---')

    # ---Over---


def fill_db():
    # ---Create table---
    people_number = 11
    print('--- Filling out database ---')
    clients_list = []
    name_arr = ["Hicks", "Clark", "Casey", "Miller", "Fisher", "Boyd", "Castillo", "Pittman", "Vega", "Ramirez", "Erickson", "Weaver",
                "Scott", "Massey", "Boone", "Francis", "Wolfe", "Gutierrez", "Chambers", "Hammond", "Alvarez", "Hill", "Tran", "Morrison", "Rogers"]
    city_arr = ["Frohchester", "Shueburgh", "Srohham", "Chuoport", "Nuland", "Zago", "Iyard", "Cladena", "Alerora",
                "Ammouth", "Tatol", "Woburgh", "Efruburgh", "Troxlens", "Phelvine", "Awam", "Qrison", "Pirie", "Akachester", "Ekastin"]
    address_arr = ["'4 Kellawe Place, Newton Aycliffe',DL5 5QZ", "'25 Winsford Crescent, Stafford',ST17 0PH", "'102 Glengarnock Avenue, London',E14 3BP", "'Belle-Vue, Chapel Town, Summercourt',TR8 5AH", "'Tamarisk, 3 Green Lane, Upton Upon Severn',WR8 0PR", "'17 Rosewarne Close, Liverpool',L17 5BX", "'8 St Walstans Close, Taverham',NR8 6PD", "'7 Moor Lane, Manchester',M23 0LT", "'Awel Y Frenni, Newchapel',SA37 0EH", "'Flat 11, Monkton Court, 35 Branksome Wood Road, Bournemouth',BH4 9JS", "'24 Ashurst Drive, Shepperton',TW17 0JL", "'28 Ravenhurst Road, Harborne',B17 9SE", "'16 Central Avenue, Worthing',BN14 0DS", "'18 River View, Braintree',CM7 1HX", "'6 Lime Tree Close, Bookham',KT23 3PJ", "'Glen View Cottage, Gelligaer',CF82 8EF", "'13 - 14 Welbeck Street, London',W1G 9XU", "'1 Crespigny Road, Aldeburgh',IP15 5HB", "'2 Cwm Coedre Cottages, Leighton',SY21 8HR", "'183 Hull Road, Anlaby',HU10 6ST", "'51 Kavanaghs Road, Brentwood',CM14 4NE", "'46 Church Lane, Henley',IP6 0RN", "'160 Pickhurst Lane, Bromley',BR2 7JB", "'1 Clayton Close, Bury',BL8 2TE", "'5 Martin Avenue, Warrington',WA2 0EU", "'19 Farmstead Close, Sheffield',S14 1LR", "'Lower Grimshaw Farm, Johnson Road, Eccleshill',BB3 3PE", "'26 Cwrt Isaf, Birchgrove',SA7 9PP", "'17 Strathmore Drive, Charvil',RG10 9QT", "'3 Crescent Road, North Baddesley',SO52 9HU", "'Croeso, Broomfield Lane, Farnsfield',NG22 8LQ", "'106 Chantry Gardens, Southwick',BA14 9QR", "'Forge Farm, Eskdale',CA19 1TT", "'5 Hows Close, Uxbridge',UB8 2AS", "'117 Victoria Road, Bradford',BD2 2BT", "'Flat 5, Westbourne Court, Lichfield Road, Walsall',WS4 2DD", "'31 Minster Road, London',NW2 3SH", "'2 Woodlands Park Grove, Pudsey',LS28 8LY", "'8 Kings Avenue, Whitefield',M45 7DJ", "'4 Sydney Place, London',SW7 3NN", "'95 Privett Road, Gosport',PO12 3SR", "'122 Yapham Road, Pocklington',YO42 2DY", "'68 Russell Drive, Nottingham',NG8 2BH", "'3 Medway Close, Skelton In Cleveland',TS12 2JZ", "'The Homestead, Foolow',S32 5QB", "'9 Upper Street, Wolverhampton',WV6 8QF", "'11 Waterfield Close, London',SE28 8DD", "'232 Oystermouth Road, Swansea',SA1 3UH", "'210 Tatwin Crescent, Southampton',SO19 6JD", "'40 Rodney Road, Backwell',BS48 3HW", "'Cheshire Gas, Peel Street, Stalybridge',SK15 1PT",
                   "'5 Beech Court, Beech Street, Elland',HX5 0EW", "'108 Priory Street, Newport Pagnell',MK16 9BL", "'4 Sheendale Road, Richmond',TW9 2JJ", "'9 Madden Close, Swanscombe',DA10 0DH", "'13 Beechcroft Close, Chandler's Ford',SO53 2HU", "'77 Belmont Street, Oldham',OL1 2AP", "'Flat 545, Ben Jonson House, Barbican, London',EC2Y 8NH", "'119 Palace Meadow, Chudleigh',TQ13 0PH", "'16 Boxhill Way, Strood Green',RH3 7HY", "'17 Brynteg, Bettws Cedewain',SY16 3DU", "'108 High Street, Great Abington',CB21 6AE", "'20 Wynyards Gap, North Baddesley',SO52 9JW", "'The Mews, Wormley West End, Broxbourne',EN10 7QN", "'3 Manchester Square, London',W1U 3PB", "'Barnaby, Roughmoor Lane, Westbury Sub Mendip',BA5 1HQ", "'The Limes, Barrowby Road, Grantham',NG31 8NT", "'20 Bordesley Green East, Bordesley Green',B9 5SA", "'8 Northlands Park, Trimdon Grange',TS29 6HX", "'12 Rainton Close, Gateshead',NE10 8RW", "'Flat 1, 2A Lambert Way, London',N12 9EP", "'Bridge House, Wrexham Road, Whitchurch',SY13 3AA", "'12 Church Close, Sharlston Common',WF4 1BJ", "'1 Terminus House, Terminus Street, Harlow',CM20 1XA", "'Flat 3, 21 Rathbone Street, London',W1T 1NF", "'18 Palleg Road, Lower Cwmtwrch',SA9 2QE", "'87 - 89 St Sepulchre Gate, Doncaster',DN1 1RU", "'40 Stray Park Road, Camborne',TR14 7TE", "'3 Denton Terrace, Gosforth',CA20 1AR", "'3 Bro Dawel, Rhosgoch',LL66 0AB", "'11 Claxton Street, Heanor',DE75 7QS", "'Apartment 13, Royal Albert Court, New Road, Saltash',PL12 6JH", "'65 Pinecroft Road, Ipswich',IP1 6BN", "'9 Wakefield Road, Norwich',NR5 8JE", "'Flat 1, Hazel Bank, South Norwood Hill, London',SE25 6BB", "'7 Somerset Court, Blackpool',FY1 5QQ", "'10 Heol Y Parc, Porthmadog',LL49 9AR", "'2 Farm View, Regents Park Road, London',N3 3JE", "'7 Bartlett Mews, London',E14 3GS", "'4 Shepherds Hill Cottages, Shepherds Hill, Colemans Hatch',TN7 4HN", "'6 Gower Close, Ulceby',DN39 6AD", "'7 Parsons Grove, Denby Village',DE5 8PY", "'Flat 3, 3 St Helens Parade, Southsea',PO4 0RW", "'15 Hall Lane, Partington',M31 4PY", "'10 Oakwood Grove, Basildon',SS13 3HT", "'18 Dew Way, Calne',SN11 8HD", "'19 Eddleston Way, Tilehurst',RG30 4GY", "'19 Dallam Chase, Milnthorpe',LA7 7DW", "'20 Wheelers Walk, Blackfield',SO45 1WX"]

    for i in range(people_number):
        clients_list.append({'name': name_arr[random.randint(0, len(name_arr)-1)], 'city': city_arr[random.randint(
            0, len(city_arr)-1)], 'address': address_arr[random.randint(0, len(address_arr)-1)]})

    orders_list = []
    orders_list_dis = ['metal', 'gold', 'silver',
                       'bronze', 'diamond', 'redstone']

    for i in range(len(clients_list)):
        orders_list.append({'clients': i+1, 'date': str(random.randint(2000, 2020))+'-'+str(random.randint(1, 12))+'-'+str(
            random.randint(1, 28)), 'amount': random.randint(1, 100), 'description': orders_list_dis[random.randint(0, len(orders_list_dis)-1)]})

    Clients.insert_many(clients_list).execute()
    Orders.insert_many(orders_list).execute()
    print('--- Database is full ---')
    # ---Over---


def show_db(names):
    if names == 'Clients':
        print('\nNAME\tSITY\tADDRESS')
        query = Clients.select().order_by(Clients.id)
        for row in query:
            print(row.name, row.city, row.address, sep='\t', end='\n')
    elif names == 'Orders':
        print('\nID CLIENTS\t\tDATE\t\t\tAMOUNT\t\tDESCRIPTION')
        query = Orders.select().order_by(Orders.id)
        for row in query:
            print(row.clients.name, row.date, row.amount,
                  row.description, sep='\t\t', end='\n')
    elif names == 'all':
        print('\n-----------TABLE CLIENTS-----------\n')
        print('\nNAME\tSITY\tADDRESS')
        query = Clients.select().order_by(Clients.id)
        for row in query:
            print(row.name, row.city, row.address, sep='\t', end='\n')
        print('\n-----------TABLE ORDERS-----------\n')
        print('\nID CLIENTS\t\tDATE\t\t\tAMOUNT\t\tDESCRIPTION')
        query = Orders.select().order_by(Orders.id)
        for row in query:
            print(row.clients.name, row.date, row.amount,
                  row.description, sep='\t\t', end='\n')


if __name__ == "__main__":
    if len(argv) <= 1:
        print(
            "for create db:\tinit\nfor fill:\tfill\nfor select db:\tshow\nfor start:\tstart")
    else:
        if argv[1] == 'init':
            init_db()
        if argv[1] == 'fill':
            fill_db()
        if argv[1] == 'show':
            if len(argv) <= 2:
                print("tables:\tClients, Orders")
            else:
                show_db(argv[2])
        if argv[1] == "start":
            init_db()
            fill_db()
            show_db("Clients")
            show_db("Orders")
