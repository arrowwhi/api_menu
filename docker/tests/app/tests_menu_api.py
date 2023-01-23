import requests_class as r
import pytest
from consts import URL

mt = r.MenuTest(URL)
menu_list = []
submenu_list = []
dishes_list = []

def test_get_menu_list():
    response = mt.get_menu_list()
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_add_menu():
    body = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    response = mt.input_menu(body)
    assert response.status_code == 201
    assert response.json().get('title') == body.get('title')
    assert response.json().get('description') == body.get('description')
    assert response.json().get('submenus_count') == 0
    assert response.json().get('dishes_count') == 0
    menu_list.append(response.json())

    response = mt.get_menu_list()
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get('title') == body.get('title')
    assert response.json()[0].get('description') == body.get('description')
    assert response.json()[0].get('submenus_count') == 0
    assert response.json()[0].get('dishes_count') == 0

def test_get_menu():
    menu_id = menu_list[0].get("id")
    response = mt.get_menu(menu_id)
    assert response.status_code == 200
    assert response.json().get('id') == menu_list[0].get('id')
    assert response.json().get('title') == menu_list[0].get('title')
    assert response.json().get('description') == menu_list[0].get('description')
    assert response.json().get('submenus_count') == 0
    assert response.json().get('dishes_count') == 0

    response = mt.get_menu(menu_id+"1")
    assert response.status_code == 404
    assert response.json().get('detail') == "menu not found"
    
def test_update_menu():
    menu_id = menu_list[0].get("id")
    body = {
        "title": "My updated menu 1",
        "description": "My updated menu description 1"
    }
    response = mt.update_menu(menu_id,body)
    assert response.status_code == 200
    assert response.json().get('title') == body.get('title')
    assert response.json().get('description') == body.get('description')

    response = mt.get_menu(menu_id)
    assert response.status_code == 200
    assert response.json().get('id') == menu_id
    assert response.json().get('title') == body.get('title')
    assert response.json().get('description') == body.get('description')
    assert response.json().get('submenus_count') == 0
    assert response.json().get('dishes_count') == 0

    response = mt.update_menu(menu_id+"1", body)
    assert response.status_code == 404
    assert response.json().get('detail') == "menu not found"

def test_delete_menu():
    menu_id = menu_list[0].get("id")
    response = mt.delete_menu(menu_id)
    assert response.status_code == 200
    assert response.json().get("status") == True
    assert response.json().get("message") == "The menu has been deleted"

    response = mt.get_menu_list()
    assert response.status_code == 200
    assert len(response.json()) == 0
    menu_list.pop()

def test_get_empty_submenu_list():
    body_menu = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    response = mt.input_menu(body_menu)
    menu_list.append(response.json())
    menu_id = menu_list[0].get('id')
    response = mt.get_submenu_list(menu_id)
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_add_submenu():
    body_submenu = {
        "title": "My submenu 1",
        "description": "My submenu description 1"
    }
    response = mt.input_submenu(menu_list[0].get('id'), body_submenu)
    assert response.status_code == 201
    assert response.json().get('title') == body_submenu.get('title')
    assert response.json().get('description') == body_submenu.get('description')
    assert response.json().get('dishes_count') == 0

    response = mt.get_submenu_list(menu_list[0].get('id'))
    assert response.status_code == 200
    assert response.json()[0].get('title') == body_submenu.get('title')
    assert response.json()[0].get('description') == body_submenu.get('description')
    assert response.json()[0].get('dishes_count') == 0
    submenu_list.append(response.json()[0])

def test_get_submenu():
    menu_id = menu_list[0].get("id")
    submenu_id = submenu_list[0].get("id")
    response = mt.get_submenu(menu_id,submenu_id)
    assert response.status_code == 200
    assert response.json().get('id') == submenu_list[0].get('id')
    assert response.json().get('title') == submenu_list[0].get('title')
    assert response.json().get('description') == submenu_list[0].get('description')
    assert response.json().get('dishes_count') == 0

    response = mt.get_submenu(menu_id, submenu_id+"1")
    assert response.status_code == 404
    assert response.json().get('detail') == "submenu not found"

def test_update_submenu():
    menu_id = menu_list[0].get("id")
    submenu_id = submenu_list[0].get("id")
    body = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    }
    response = mt.update_submenu(menu_id,submenu_id,body)
    assert response.status_code == 200
    assert response.json().get('title') == body.get('title')
    assert response.json().get('description') == body.get('description')

    response = mt.get_submenu(menu_id,submenu_id)
    assert response.status_code == 200
    assert response.json().get('id') == submenu_id
    assert response.json().get('title') == body.get('title')
    assert response.json().get('description') == body.get('description')
    assert response.json().get('dishes_count') == 0

    response = mt.update_submenu(menu_id,submenu_id+"1", body)
    assert response.status_code == 404
    assert response.json().get('detail') == "submenu not found"

def test_delete_submenu():
    menu_id = menu_list[0].get("id")
    submenu_id = submenu_list[0].get("id")
    response = mt.delete_submenu(menu_id,submenu_id)
    assert response.status_code == 200
    assert response.json().get("status") == True
    assert response.json().get("message") == "The submenu has been deleted"

    response = mt.get_submenu_list(menu_id)
    assert response.status_code == 200
    assert len(response.json()) == 0
    response = mt.delete_menu(menu_id)
    menu_list.pop()
    submenu_list.pop()

def test_get_empty_dishes_list():
    body_menu = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    body_submenu = {
        "title": "My submenu 1",
        "description": "My submenu description 1"
    }
    response = mt.input_menu(body_menu)
    menu_list.append(response.json())
    menu_id = menu_list[0].get('id')
    response = mt.input_submenu(menu_id, body_submenu)
    submenu_list.append(response.json())
    submenu_id = submenu_list[0].get('id')
    response = mt.get_dishes_list(menu_id,submenu_id)
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_add_dish():
    body_dish = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }
    menu_id = menu_list[0].get('id')
    submenu_id = submenu_list[0].get('id')
    response = mt.input_dish(menu_id,submenu_id,body_dish)
    assert response.status_code == 201
    assert response.json().get('title') == body_dish.get('title')
    assert response.json().get('description') == body_dish.get('description')
    assert response.json().get('price') == body_dish.get('price')

    response = mt.get_dishes_list(menu_id, submenu_id)
    assert response.status_code == 200
    assert response.json()[0].get('title') == body_dish.get('title')
    assert response.json()[0].get('description') == body_dish.get('description')
    assert response.json()[0].get('price') == body_dish.get('price')
    dishes_list.append(response.json()[0])

def test_get_dish():
    menu_id = menu_list[0].get("id")
    submenu_id = submenu_list[0].get("id")
    dish_id = dishes_list[0].get("id")
    response = mt.get_dish(menu_id,submenu_id,dish_id)
    assert response.status_code == 200
    assert response.json().get('title') == dishes_list[0].get('title')
    assert response.json().get('description') == dishes_list[0].get('description')
    assert response.json().get('price') == dishes_list[0].get('price')

    response = mt.get_dish(menu_id, submenu_id, dish_id+"1")
    assert response.status_code == 404
    assert response.json().get('detail') == "dish not found"
    
def test_update_dish():
    body = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50"
    }
    menu_id = menu_list[0].get("id")
    submenu_id = submenu_list[0].get("id")
    dish_id = dishes_list[0].get("id")

    response = mt.update_dish(menu_id,submenu_id,dish_id, body)
    assert response.status_code == 200
    assert response.json().get('title') == body.get('title')
    assert response.json().get('description') == body.get('description')
    assert response.json().get('price') == body.get('price')

    response = mt.get_dish(menu_id,submenu_id,dish_id)
    assert response.status_code == 200
    assert response.json().get('id') == dish_id
    assert response.json().get('title') == body.get('title')
    assert response.json().get('description') == body.get('description')
    assert response.json().get('price') == body.get('price')

    response = mt.update_dish(menu_id,submenu_id, dish_id+"1", body)
    assert response.status_code == 404
    assert response.json().get('detail') == "dish not found"

def test_delete_dish():
    menu_id = menu_list[0].get("id")
    submenu_id = submenu_list[0].get("id")
    dish_id = dishes_list[0].get("id")
    response = mt.delete_dish(menu_id,submenu_id, dish_id)
    assert response.json().get("status") == True
    assert response.json().get("message") == "The dish has been deleted"

    response = mt.get_dishes_list(menu_id,submenu_id)
    assert response.status_code == 200
    assert len(response.json()) == 0
    response = mt.delete_menu(menu_id)
    menu_list.pop()
    submenu_list.pop()
    dishes_list.pop()

