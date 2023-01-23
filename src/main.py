from fastapi import FastAPI, Depends, Body
from fastapi.responses import JSONResponse
# from db_requests import create_session, select_menus, select_submenus_count, select_dishes_count_on_menu, insert_menu, update_menu, delete_menu_r
# from db_requests import select_submenus, select_dishes_count, insert_submenu, update_submenu, delete_submenu_r
# from db_requests import select_dishes, insert_dish, update_dish, delete_dish_r

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy import create_engine
from sqlalchemy import insert, select, update, delete
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.engine.url import URL

import os
from os import getenv
from dotenv import load_dotenv

Base = declarative_base()

class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String, nullable=False)
    description = Column(String)
    children_submenu = relationship(
        "Submenu",
        back_populates="parent_menu",
        cascade="all, delete",
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id":str(self.id),
            "title":self.title,
            "description":self.description
        }

class Submenu(Base):
    __tablename__ = 'submenu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey("menu.id", ondelete="CASCADE"))
    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    parent_menu = relationship("Menu", back_populates="children_submenu")
    children_dish = relationship(
        "Dish",
        back_populates="parent_submenu",
        cascade="all, delete",
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id":str(self.id),
            "title":self.title,
            "description":self.description
        }

class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True, autoincrement=True)
    submenu_id = Column(Integer, ForeignKey("submenu.id", ondelete="CASCADE"))
    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    price = Column(String, nullable=False)
    parent_submenu = relationship("Submenu", back_populates="children_dish")

    def to_dict(self):
        return {
            "id":str(self.id),
            "title":self.title,
            "description":self.description,
            "price":self.price
        }

dotenv_path = os.path.join(os.path.dirname(__file__), 'settings.env')
print(dotenv_path)
load_dotenv(dotenv_path=dotenv_path)

DATABASE = {
    'drivername': getenv("drivername"),
    'host': getenv("host"),
    'port': getenv("port"),
    'username': getenv("username"),
    'password': getenv("password"),
    'database': getenv('database')
}

def create_session():
    engine = create_engine(URL.create(**DATABASE), pool_size=50)
    engine.connect()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session

def insert_menu(Session, title:String, desc:String):
    ins = (
       insert(Menu).
       values(title=title, description=desc)
    )
    session = Session()
    primary_key = session.execute(ins)
    session.commit()
    return primary_key

def insert_submenu(Session, menu_id:Integer, title:String, desc:String):
    ins = (
        insert(Submenu).
        values(menu_id=menu_id, title=title, description=desc)
    )
    session = Session()
    primary_key = session.execute(ins)
    session.commit()
    return primary_key

def insert_dish(Session, submenu_id:Integer, title:String, desc:String, price: String):
    ins = (
        insert(Dish)
        .values(submenu_id = submenu_id, title=title, description=desc, price = price)
    )
    session = Session()
    primary_key = session.execute(ins)
    session.commit()
    return primary_key

def select_menus(Session, menu_id:Integer = None):
    sel = (
        select(Menu)
    )
    if menu_id!=None:
        sel=sel.where(Menu.id==menu_id)

    session = Session()
    return session.execute(sel)


def select_submenus(Session, menu_id:Integer = None, submenu_id:Integer = None):
    sel = (
        select(Submenu)
    )
    if menu_id!=None:
        sel=sel.where(menu_id==menu_id)
    if submenu_id!=None:
        sel=sel.where(Submenu.id==submenu_id)
    session = Session()
    return session.execute(sel)

def select_dishes(Session, submenu_id:Integer = None, dish_id:Integer = None):
    sel = (
        select(Dish)
    )
    if submenu_id!=None:
        sel=sel.where(Dish.submenu_id==submenu_id)
    if dish_id!=None:
        sel=sel.where(Dish.id==dish_id)
    session = Session()
    return session.execute(sel)

def select_submenus_count(Session, menu_id:Integer = None):
    sel = (
        select(func.count("*")).select_from(Submenu)
    )
    if menu_id != None:
        sel = sel.where(Submenu.menu_id==menu_id)
    session = Session()
    return session.execute(sel).first()[0]

def select_dishes_count_on_menu(Session, menu_id:Integer):
    pass
    sel = (
        select(func.count("*"))
        .select_from(Submenu)
        .join(Dish, Dish.submenu_id == Submenu.id)
        .where(Submenu.menu_id == menu_id)
    )
    session = Session()
    return session.execute(sel).first()[0]

def select_dishes_count(Session, submenu_id:Integer):
    sel = (
        select(func.count("*")).select_from(Dish)
        .where(Dish.submenu_id == submenu_id)
    )
    session = Session()
    return session.execute(sel).first()[0]

def update_menu(Session, menu_id:Integer, title:String, description:String):
    upd = (
    update(Menu).
    where(Menu.id == menu_id).
    values(title=title, description = description)
    )
    session = Session()
    session.execute(upd)
    session.commit()

def update_submenu(Session, submenu_id:Integer, title:String, description:String):
    upd = (
    update(Submenu).
    where(Submenu.id == submenu_id).
    values(title=title, description = description)
    )
    session = Session()
    session.execute(upd)
    session.commit()

def update_dish(Session, dish_id:Integer, title:String, description:String, price:String):
    upd = (
    update(Dish).
    where(Dish.id == dish_id).
    values(title=title, description = description, price = price)
    )
    session = Session()
    session.execute(upd)
    session.commit()

def delete_menu_r(Session, menu_id:Integer):
    delt = (
        delete(Menu)
        .where(Menu.id == menu_id)
    )
    session = Session()
    session.execute(delt)
    session.commit()

def delete_submenu_r(Session, submenu_id:Integer):
    delt = (
        delete(Submenu)
        .where(Submenu.id == submenu_id)
    )
    session = Session()
    session.execute(delt)
    session.commit()

def delete_dish_r(Session, dish_id:Integer):
    delt = (
        delete(Dish)
        .where(Dish.id == dish_id)
    )
    session = Session()
    session.execute(delt)
    session.commit()



app = FastAPI()
Session = create_session()

@app.get("/api/v1/menus")
def get_menus():
    out = []
    for iter in select_menus(Session):
        elem = iter["Menu"].to_dict()
        elem["submenus_count"] = select_submenus_count(Session, elem["id"])
        elem["dishes_count"] = select_dishes_count_on_menu(Session, elem["id"])
        out.append(elem)
    return out

@app.get("/api/v1/menus/{api_test_menu_id}")
def get_menu(api_test_menu_id):
    elem = select_menus(Session, int(api_test_menu_id))
    for iter in elem:
        dict = iter["Menu"].to_dict()
        dict["submenus_count"] = select_submenus_count(Session, int(api_test_menu_id))
        dict["dishes_count"] = select_dishes_count_on_menu(Session, int(api_test_menu_id))
        return dict
    return JSONResponse({"detail": "menu not found"}, status_code=404)
    
@app.post("/api/v1/menus")
def add_menu(title = Body(embed=True), description = Body(embed=True)):
    key = insert_menu(Session, title, description).inserted_primary_key[0]
    val = get_menu(key)
    return JSONResponse(content=val, status_code=201)

@app.patch("/api/v1/menus/{api_test_menu_id}")
def patch_menu(api_test_menu_id, title = Body(embed=True), description = Body(embed=True)):
    update_menu(Session, api_test_menu_id, title, description)
    return get_menu(api_test_menu_id)

@app.delete("/api/v1/menus/{api_test_menu_id}")
def delete_menu(api_test_menu_id):
    delete_menu_r(Session, api_test_menu_id)
    return JSONResponse(content={ "status": True, "message": "The menu has been deleted"})

@app.get("/api/v1/menus/{api_test_menu_id}/submenus")
def get_submenus(api_test_menu_id):
    out = []
    for iter in select_submenus(Session, api_test_menu_id):
        pass
        elem = iter["Submenu"].to_dict()
        elem["dishes_count"] = select_dishes_count(Session, elem["id"])
        out.append(elem)
    return out

@app.get("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}")
def get_submenu(api_test_submenu_id):
    lst = select_submenus(Session, submenu_id=api_test_submenu_id)
    for iter in lst:
        dict = iter["Submenu"].to_dict()
        dict["dishes_count"] = select_dishes_count(Session, api_test_submenu_id)
        return dict
    return JSONResponse({"detail": "submenu not found"}, status_code=404)

@app.post("/api/v1/menus/{api_test_menu_id}/submenus")
def add_submenu(api_test_menu_id, title = Body(embed=True), description = Body(embed=True)):
    key = insert_submenu(Session, api_test_menu_id, title, description).inserted_primary_key[0]
    val = get_submenu(key)
    return JSONResponse(content=val, status_code=201)


@app.patch("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}")
def patch_submenu(api_test_submenu_id, title = Body(embed=True), description = Body(embed=True)):
    update_submenu(Session, api_test_submenu_id, title, description)
    return get_submenu(api_test_submenu_id)

@app.delete("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}")
def delete_submenu(api_test_submenu_id):
    delete_submenu_r(Session, int(api_test_submenu_id))
    return JSONResponse(content={ "status": True, "message": "The submenu has been deleted"})

@app.get("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes")
def get_dishes(api_test_submenu_id):
    out = []
    for iter in select_dishes(Session, api_test_submenu_id):
        elem = iter["Dish"].to_dict()
        out.append(elem)
    return out

@app.get("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}")
def get_dish(api_test_dish_id):
    elem = select_dishes(Session, dish_id=int(api_test_dish_id))
    for iter in elem:
        return iter["Dish"].to_dict()
    return JSONResponse({"detail": "dish not found"}, status_code=404)

@app.post("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes")
def add_dish(api_test_submenu_id, title = Body(embed=True), description = Body(embed=True), price = Body(embed=True)):
    key = insert_dish(Session, api_test_submenu_id, title, description, price).inserted_primary_key[0]
    val = get_dish(key)
    return JSONResponse(content=val, status_code=201)

@app.patch("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}")
def patch_dish(api_test_dish_id, title = Body(embed=True), description = Body(embed=True), price = Body(embed=True)):
    update_dish(Session, api_test_dish_id, title, description, price)
    return get_dish(api_test_dish_id)

@app.delete("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}")
def delete_dish(api_test_dish_id):
    delete_dish_r(Session, api_test_dish_id)
    return JSONResponse(content={ "status": True, "message": "The dish has been deleted"})

