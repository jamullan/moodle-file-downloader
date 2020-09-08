# Moodle File Downloader: CookieManager
# Copyright 2020 John Mullan
# The creator of this software, John Mullan, has made it available under the MIT license,
# as deliniated in the README.md file in the root directory of this repository

# Facilitates the bi-directional transfer of cookie data between the Chrome driver instance and cookies.txt
#       as to allow authentication cookies to effectively persist between Chrome driver sessions
#       (note that the cookies themselves may expire after a set amount of time, however)
class CookieManager:

    # Initialize an instance of the class with the Chrome driver
    # driver: the Chrome webdriver instance created in the moodle_file_downloader module
    def __init__(self, driver):
        self.driver = driver

    # Remove all cookies from the driver and from cookies.txt
    def reset(self):
        self.driver.delete_all_cookies()
        
        file = open("cookies.txt", "w")
        file.write("")
        file.close()

    # Imports cookies from cookies.txt and saves them to the Chrome driver instance
    def import_cookies_from_file(self):
        self.driver.delete_all_cookies()

        cookies_file = open("cookies.txt","r")
        for line in cookies_file:
            temp_cookie_list = line.split("\t")
            temp_cookie_dictionary = {}

            temp_cookie_dictionary.update({"domain":temp_cookie_list[0]})

            http_only_bool = False
            if temp_cookie_list[1] == "TRUE":
                http_only_bool = True 
            temp_cookie_dictionary.update({"httpOnly":http_only_bool})
            temp_cookie_dictionary.update({"path":temp_cookie_list[2]})

            secure_bool = False
            if temp_cookie_list[3] == "TRUE":
                secure_bool = True
            temp_cookie_dictionary.update({"secure":secure_bool})
            temp_cookie_dictionary.update({"name":temp_cookie_list[5]})
            temp_cookie_dictionary.update({"value":temp_cookie_list[6][:-1]}) #[:-1] excludes \n

            self.driver.add_cookie(temp_cookie_dictionary)
        
        cookies_file.close()

    # Saves cookies from the driver to cookies.txt
    def save_cookies(self):
        cookies = self.driver.get_cookies()

        cookies_file = open("cookies.txt", "w")
        cookies_file.write("")
        cookies_file.close()
        for cookie in cookies:
            self.write_cookie_to_file(cookie)
    
    # Writes a single cookie to the cookies.txt file having the following tab-delimited values:
    #       domain, subdomains bool, path, secure bool, placeholder expiration time, name, value
    # cookie: a cookie dictionary from the Chrome driver to write to cookies.txt
    #       that has the following attributes:
    #       'domain','httpOnly','name','path','secure','value'
    def write_cookie_to_file(self, cookie):
        cookie_to_write = []
        
        cookie_to_write.append(cookie.get('domain')) #add domain
        cookie_to_write.append(str(cookie.get('httpOnly')).upper()) #add subdomains bool
        cookie_to_write.append(cookie.get('path')) #add path
        cookie_to_write.append(str(cookie.get('secure')).upper()) #add secure bool
        cookie_to_write.append(str(0)) #add placeholder expiration time
        cookie_to_write.append(cookie.get('name')) #add name
        cookie_to_write.append(cookie.get('value')) #add value

        cookies_file = open("cookies.txt", "a")

        for item in cookie_to_write[:-1]:
            cookies_file.write(item)
            cookies_file.write("\t")
        cookies_file.write(cookie_to_write[-1])
        
        cookies_file.write("\n")
        cookies_file.close()

    # Counts the lines in a file
    # file_name: the name of the file to analyze
    # NOTE: this method not currently in use
    # returns: the number of lines in the supplied file
    def count_lines(self, file_name):
        file = open(file_name, "r")
        num_lines = 0
        
        try:
            for line in file:
                num_lines += 1
        except:
            pass

        file.close()
        
        return num_lines