from ldap3 import Server, Connection, ALL, NTLM
import configparser
import time
import json

current_user_list = []

def read_config():
    while True:
        config = configparser.ConfigParser()
        config.read("config.ini", encoding='utf-8')
        c_server_ad = config["AD"]["server"]
        c_user_ad = config["AD"]["user"]
        c_password_user_ad = config["AD"]["password"]
        c_search_base_ad = config["AD"]["search_base"]
        c_search_filter_ad = config["AD"]["search_filter"]
        c_attributes_ad = config["AD"]["attributes"]
        
        time.sleep(1)

        return c_server_ad, c_user_ad, c_password_user_ad,c_search_base_ad, c_search_filter_ad, c_attributes_ad

def check_users():

    with open('users.json', 'r', encoding='utf-8') as f:
        prev_user_list = json.load(f)
        #print(prev_user_list)

    only_in_prev_user_list = [item for item in prev_user_list if item not in current_user_list]
    only_in_current_user_list = [item for item in current_user_list if item not in prev_user_list]

    if len(only_in_current_user_list) > 0:
        for user in only_in_current_user_list:  
            username = str(user).split(",")[0].replace("CN=","")
            print(f"User '{username}' was granted {read_config()[4]} rights.")

    if len(only_in_prev_user_list) >  0:        
        for user in only_in_prev_user_list:  
            username = str(user).split(",")[0].replace("CN=","")
            print(f"User '{username}' no longer has {read_config()[4]} rights.")

    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(current_user_list, f, ensure_ascii=False, indent=4)
    
    only_in_prev_user_list.clear()
    only_in_current_user_list.clear()
    current_user_list.clear()

def read_AD():
    server_ad, user_ad, password_user_ad, search_base_ad, search_filter_ad, attributes_ad = read_config()

    server = Server(server_ad, get_info=ALL)
    conn = Connection(server, user=user_ad, password=password_user_ad, authentication=NTLM, auto_bind=True)

    conn.search(f'DC={search_base_ad.split(".")[0]},DC={search_base_ad.split(".")[1]}', f'(CN={search_filter_ad})', attributes=[f'{attributes_ad}'])

    members = conn.entries[0].member.values if conn.entries else []

    #print(f"Администраторы домена: {len(members)}")
    for member in members:
        current_user_list.append(member)
        #print(member)

    conn.unbind()

    check_users()

if __name__ == "__main__":

    while True:
        read_AD()
        time.sleep(30)
