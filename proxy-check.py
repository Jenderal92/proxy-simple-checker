import requests
import time
import os

def check_proxy(proxy):
    url = 'https://httpbin.org/ip'
    
    if not (proxy.startswith("http://") or proxy.startswith("socks4://") or proxy.startswith("socks5://")):
        proxy = "http://" + proxy

    proxies = {'http': proxy, 'https': proxy}

    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxies, timeout=2)
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200 and response_time < 2000:
            print "Proxy {} valid dengan waktu respons {} ms".format(proxy, int(response_time))
            return True
        else:
            print "Proxy {} tidak valid atau melebihi batas waktu respons: {} ms".format(proxy, int(response_time))
            return False

    except requests.exceptions.Timeout:
        print "Proxy {} tidak valid, request timeout.".format(proxy)
        return False
    except requests.exceptions.ConnectionError:
        print "Proxy {} tidak valid, tidak bisa terhubung ke server.".format(proxy)
        return False
    except requests.exceptions.TooManyRedirects:
        print "Proxy {} tidak valid, terlalu banyak redirect.".format(proxy)
        return False
    except requests.exceptions.RequestException as e:
        print "Proxy {} tidak valid, error: {}".format(proxy, str(e))
        return False

def read_proxy_list(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except IOError:
        print "File '{}' tidak ditemukan."
        return []
    except Exception as e:
        print "Gagal membuka file '{}', error: {}".format(file_path, str(e))
        return []

def save_valid_proxy(proxy, output_file):
    existing_proxies = set()
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            existing_proxies.update(line.strip() for line in f)
    if proxy not in existing_proxies:
        with open(output_file, 'a') as f:
            f.write(proxy + '\n')
        print "Proxy {} disimpan ke file.".format(proxy)
    else:
        print "Proxy {} sudah ada di file.".format(proxy)

print "Proxy Checker | Shin Code\n"
input_ = raw_input('Ur list: ')
proxy_list = read_proxy_list(input_)

output_file = 'valid_proxies.txt'
for proxy in proxy_list:
    if check_proxy(proxy):
        save_valid_proxy(proxy, output_file)

print "Pengecekan selesai. Proxy valid telah disimpan di '{}'.".format(output_file)
