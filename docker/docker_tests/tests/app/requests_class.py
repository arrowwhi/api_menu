import pytest
import requests
import logging

logger = logging.getLogger("test_menu_api")


class MenuTest:
    def __init__(self, url):
        self.url = url
    
    path = '/api/v1/menus/'
    path_submenu = '/submenus/'
    path_dishes = '/dishes/'

    def get_menu_list(self):
        response = requests.get(f'{self.url}{self.path}')
        logger.info(response.text)
        return response
    
    def get_menu(self, menu_id):
        response = requests.get(f'{self.url}{self.path}{menu_id}')
        logger.info(response.text)
        return response

    def input_menu(self, body:dict):
        response = requests.post(f'{self.url}{self.path}', json=body)
        logger.info(response.text)
        return response

    def update_menu(self, menu_id, body:dict):
        response = requests.patch(f'{self.url}{self.path}{menu_id}', json=body)
        logger.info(response.text)
        return response

    def delete_menu(self, menu_id):
        response = requests.delete(f'{self.url}{self.path}{menu_id}')
        logger.info(response.text)
        return response

    def get_submenu_list(self, menu_id):
        response = requests.get(f'{self.url}{self.path}{menu_id}{self.path_submenu}')
        logger.info(response.text)
        return response

    def get_submenu(self, menu_id, submenu_id):
        response = requests.get(f'{self.url}{self.path}{menu_id}{self.path_submenu}{submenu_id}')
        logger.info(response.text)
        return response

    def input_submenu(self, menu_id, body:dict):
        response = requests.post(f'{self.url}{self.path}{menu_id}{self.path_submenu}', json=body)
        logger.info(response.text)
        return response

    def update_submenu(self, menu_id, submenu_id, body:dict):
        response = requests.patch(f'{self.url}{self.path}{menu_id}{self.path_submenu}{submenu_id}', json=body)
        logger.info(response.text)
        return response

    def delete_submenu(self, menu_id, submenu_id):
        response = requests.delete(f'{self.url}{self.path}{menu_id}{self.path_submenu}{submenu_id}')
        logger.info(response.text)
        return response

    def get_dishes_list(self, menu_id, submenu_id):
        response = requests.get(f'{self.url}{self.path}{menu_id}{self.path_submenu}{submenu_id}{self.path_dishes}')
        logger.info(response.text)
        return response
        
    def get_dish(self, menu_id, submenu_id, dish_id):
        response = requests.get(f'{self.url}{self.path}{menu_id}{self.path_submenu}{submenu_id}{self.path_dishes}{dish_id}')
        logger.info(response.text)
        return response

    def input_dish(self, menu_id, submenu_id, body:dict):
        response = requests.post(f'{self.url}{self.path}{menu_id}{self.path_submenu}{submenu_id}{self.path_dishes}', json=body)
        logger.info(response.text)
        return response

    def update_dish(self, menu_id, submenu_id, dish_id, body:dict):
        response = requests.patch(f'{self.url}{self.path}{menu_id}{self.path_submenu}{submenu_id}{self.path_dishes}{dish_id}', json=body)
        logger.info(response.text)
        return response

    def delete_dish(self, menu_id, submenu_id, dish_id):
        response = requests.delete(f'{self.url}{self.path}{menu_id}{self.path_submenu}{submenu_id}{self.path_dishes}{dish_id}')
        logger.info(response.text)
        return response

# import consts
# t = MenuTest(consts.URL)
# menu_body = {
#     "title": "menu_1",
#     "description": "desc_1"
# }

# response = t.input_menu(menu_body)
# print(response.status_code)
# print(type(response.json()))

