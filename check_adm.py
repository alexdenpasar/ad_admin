from ldap3 import Server, Connection, ALL, NTLM
import configparser
import time


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
    
def check_adm():
    server_ad, user_ad, password_user_ad, search_base_ad, search_filter_ad, attributes_ad = read_config()

    server = Server(server_ad, get_info=ALL)
    conn = Connection(server, user=user_ad, password=password_user_ad, authentication=NTLM, auto_bind=True)

    conn.search(f'DC={search_base_ad.split(".")[0]},DC={search_base_ad.split(".")[1]}', f'(CN={search_filter_ad})', attributes=[f'{attributes_ad}'])

    members = conn.entries[0].member.values if conn.entries else []

    print(f"Администраторы домена: {len(members)}")
    for member in members:
        print(member)

    conn.unbind()

if __name__ == "__main__":

    check_adm()
