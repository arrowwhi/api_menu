from fastapi import FastAPI, Depends, Body
from fastapi.responses import JSONResponse
from db_requests import create_session, select_menus, select_submenus_count, select_dishes_count_on_menu, insert_menu, update_menu, delete_menu_r
from db_requests import select_submenus, select_dishes_count, insert_submenu, update_submenu, delete_submenu_r
from db_requests import select_dishes, insert_dish, update_dish, delete_dish_r


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

