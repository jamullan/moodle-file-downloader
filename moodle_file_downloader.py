# Moodle File Downloader
# Copyright 2020 John Mullan
# The creator of this software, John Mullan, has made it available under the MIT license,
# as deliniated in the README.md file in the root directory of this repository
# NOTICE: Modification of the code inside the consent, consent_to_statement, or final_consent methods, 
#         or changing the nature of calls to those methods in any way is strictly forbidden, and violates terms of use.
# WARNING: do NOT redistribute software without deleting the contents of the "cookies.txt" file

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from cookie_manager import CookieManager
import subprocess
import time
import sys
import os

# Loads the Moodle page of the instution name that is provided, if such a page exists
# driver: the Chrome webdriver instance
# returns: the name of the school who's Moodle page the user is accessing
def load_institution_moodle(driver):
    validating = True
    school_name = ""

    while validating:
        school_name = input("Welcome to Moodle file downloader! Please enter the name of your school/institution: ")
        url = "https://moodle." + school_name + ".edu/"
        print("\nChecking the validity of \"" + url + "\"\n")

        driver.get(url)

        try:
            assert "Moodle" in driver.title
            assert ((school_name in driver.title) or (school_name.capitalize() in driver.title) or (school_name.lower() in driver.title))
            validating = False
        except:
            print("The url \"{}\" is not valid".format(url))
            print("Please try again\n")

    print("Success! The url \"{}\" is valid!\n".format(url))
    return school_name

# Scans a page for urls that directory or indirectly link to downloadable files
# driver: the Chrome webdriver instance
# page_href: the url of the page to be scanned
# returns: a list of urls that point to downloadable files
def get_file_urls_from_page(driver, page_href):
    driver.get(page_href)
    course_page_title = driver.title
    anchor_elements = driver.find_elements_by_css_selector("a")

    hrefs = [] #href values that contain the "/mod/resource/" substring
    file_urls = [] #urls that point to files that can be retrieved by curl

    #get href attribute values from anchors where href value contains "/mod/resource/"
    for element in anchor_elements:
        try:
            element_href = element.get_attribute("href")
            if element_href.find("/mod/resource/") != -1:
                hrefs.append(element_href)

        except:
            continue

    #check to see if href redirects
    for href in hrefs:
        driver.get(page_href) #return to course page
        driver.get(href)

        #href does not redirect; store it as a file_url
        if driver.title == course_page_title:
            file_urls.append(href)
        
        #href redirects, needs further examination
        else:

            #href redirects, but curl detects the redirection; store it as a file_url
            if "pluginfile.php" in driver.current_url:
                file_urls.append(href)
                pass
            
            #href redirects to a page that contains the href to be used for the file_url
            else:
                #obtain candidate anchor element
                anchor_elements = driver.find_elements_by_css_selector("a")
                for anchor_element in anchor_elements:
                    try:
                        #obtain a candidate href
                        element_href = anchor_element.get_attribute("href")

                        #the candidate href links to a file; store it as a file_url
                        if element_href.find("pluginfile.php") != -1:
                            file_urls.append(element_href)
                            break
                        
                        #the candidate href does not link to a file
                        else:
                            continue
                    
                    #the anchor element does nto contain an href attribute, and thus is no longer under consideration
                    except:
                        continue

    return file_urls

# Informs the user of potential risks and obtains their consent to the terms and conditions of its use
def consent():
    whoami_cmd = "$(whoami)"
    name = subprocess_cmd("echo " + whoami_cmd)
    name = (str(name)[2:-1])

    os.system("clear")
    print("***Using this utility requires that you agree to the terms and conditions.*** \n\nFor each statement that you agree with, enter the word \"yes\" (without quotes) and press the return key. Enter any other value if you disagree")
    waiting = True
    while waiting:
        if input("\nTry it now to continue: ") == "yes":
            waiting = False

    consent_to_statement("Do you promsie to not release any files downloaded with this utility nor discuss their contents to those whom the creator would not give consent to?")
    consent_to_statement("Do you realize that these files may be protected by US Federal Intellectual Property law, and that you may face legal exposure for improperly accessing, storing, or using these files?")
    consent_to_statement("Do you understand that in the process of downloading these files you may overwhelm the Moodle file system, and while unlikely, may cause system interruptions?")
    consent_to_statement("Do you understand that this program will store cookies used to authenticate you in the same folder of this program in an unencrypted format in a file \"cookies.txt\" and that you should not share this program without first deleting this file?")
    consent_to_statement("Do you indemnify and hold harmless the creator of this software for all consequences, direct or percieved, that may arise from using this software, during time of use or thereafter, \nand do you further take full responsibility for any and all actions that may arise from using this software?")
    final_consent(name)

    os.system("clear")
    print("Thank you for your consent. This program will now proceed")
    time.sleep(2)
    os.system("clear")

# Obtains consent to the statement, else quits
# statement: the text to be agreed to as a string
def consent_to_statement(statement):
    statement = statement + " "
    os.system("clear")
    if input(statement) != "yes":
        print("\nYou must agree to all terms and conditions to use this program. This program will now quit.")
        time.sleep(2)
        sys.exit()

# Obtains final consent to all previous statements
# name: the user's username
def final_consent(name):
    os.system("clear")
    statement = "Do you, {}, swear that you have answered the previous questions truthfully and voluntarily? ".format(name)
    if input(statement) != "yes":
        print("\nYou must agree to all terms and conditions to use this program. This program will now quit.")
        time.sleep(2)
        sys.exit()

    if input("\nEnter the word \"acknowledge\" without quotes and with each letter \"e\" capitalized to confirm: ") != "acknowlEdgE":
        print("You must agree to all terms and conditions to use this program. This program will now quit.")
        time.sleep(2)
        sys.exit()

# Attempts to login by automating the click of the login button
#       credentials have been supplied to the driver as cookies
#       using invalid or empty cookies will fail this attempt
# driver: the Chrome webdriver instance
def auto_login(driver):
    print("\n System now attempting auto login")

    login_button = driver.find_elements_by_class_name("btn-primary")[0]
    login_button.click()

    if driver.title == "Web Login Service":
        print("\n Auto login failed. Manual login required")

# Waits for the user to login and verifies their login
# driver: the Chrome webdriver instance
# returns: the name of the user as displayed on the Moodle page
def verify_login(driver):
    verifying = True
    logininfo = ""
    while verifying:
        try:
            logininfo = driver.find_elements_by_class_name("logininfo")[0].get_attribute("innerHTML")
            if "You are logged in as" in logininfo:
                verifying = False
            else:
                time.sleep(1)
                continue
        except Exception:
            time.sleep(1)
    
    name = logininfo.split("title=\"View profile\">")[1].split("</a>")[0]
    print("Login verified. Welcome, {}!".format(name))

    return name

# Gets a user's course names and their associated urls and organizes them into a
#       year-->term-->course hierarchy
# driver: the Chrome webdriver instance
# returns: a multi-dimensional dictionary with course names and urls of the format:
#       {academic_year_key: {term_key: [course_name, course_url]}}
def get_courses(driver):
    '''
    multi-dimensional dictionary representing hierarchy of Moodle courses
    {academic_year_key: {term_key: [course_name, course_url]}}
    '''
    courses = {}

    css_selector_year_elements = ".tree > li"
    year_elements = driver.find_elements_by_css_selector(css_selector_year_elements)

    for year_element in year_elements:
        temp_terms_dictionary = {}
        courses.update({year_element_to_string(year_element):temp_terms_dictionary})

        css_selector_term_elements = "li > ol > li"
        term_elements = year_element.find_elements_by_css_selector(css_selector_term_elements)

        refined_term_elements = []
        for term_element in term_elements:
            try:
                temp = term_element.find_element_by_css_selector("li > ol")
                refined_term_elements.append(term_element)

            except: 
                continue    

        for term_element in refined_term_elements:
            temp_classes_list = []
            temp_terms_dictionary.update({term_element_to_string(term_element):temp_classes_list})

            css_selector_class_elements = "li > ol > li > a"
            class_elements = term_element.find_elements_by_css_selector(css_selector_class_elements)

            for class_element in class_elements:
                class_name = class_element.get_attribute("innerHTML")
                class_name = decode_course_innerhtml(class_name)

                class_href = class_element.get_attribute("href")

                temp_class_list = [class_name, class_href]
                temp_classes_list.append(temp_class_list)

    return courses

# Extracts the innerHTML from a year_element's child label element
# year_element: an HTML element that represents an academic year
# returns: the innerHTML of the year element's label
def year_element_to_string(year_element):
    year_element_child_label = year_element.find_element_by_css_selector("label")
    year_element_string = year_element_child_label.get_attribute("innerHTML")

    return year_element_string

# Extracts the innerHTML from a term_element's child label element
# term_element: an HTML element that represents an academic term
# returns: the innerHTML of the term element's label
def term_element_to_string(term_element):
    term_element_child_label = term_element.find_element_by_css_selector("label")
    term_element_string = term_element_child_label.get_attribute("innerHTML")

    return term_element_string

# Decodes a course name from HTML encoding into plain text and
#       removes extraneous characters
# returns: the plain text name of the course
def decode_course_innerhtml(course_innerhtml):
    decoded = course_innerhtml.replace("&amp;", "&")
    decoded = decoded.replace("&nbsp;","")
    decoded = decoded.replace("<span>","")
    decoded = decoded.replace("</span>","")

    return decoded

# Executes a Bash command or a string of commands
# command: the Bash command to be executed
#       (may include multiple commands separated by delimiters)
# returns: the standard output from the subbprocess  
def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    
    return proc_stdout

# Escapes special values, substitutes in other values, 
#       or removes them entirely for them to be directory-name-safe
# string: the string to have characters escaped/modified within
# returns: a string with escaped/substitued characters
def clean_string(string):
    string = string.replace(" ", "\ ")
    string = string.replace("'", "\ ")
    string = string.replace("(", "\(")
    string = string.replace(")", "\)")
    string = string.replace("&", "")
    string = string.replace(":", "\ ")
    string = string.replace("?", "\?")
    string = string.replace("=", "\=")

    return string

# Downloades the files from each course page
# driver: the Chrome webdriver instance
# courses: a multi-dimensional dictionary with course names and urls of the format:
#       {academic_year_key: {term_key: [course_name, course_url]}}
# name_of_user: the name of the user as displayed on the Moodle dashboard page
def download_files(driver, courses, name_of_user):
    pwd = '$(pwd)'
    root_dir_path = subprocess_cmd('echo ' + pwd)
    root_dir_path = str(root_dir_path)[2:-1]
    root_dir_path = clean_string(root_dir_path)

    output_dir_name = name_of_user + "_Moodle Files"
    output_dir_name = clean_string(output_dir_name)
    subprocess_cmd('mkdir ' + output_dir_name)

    for i, year_values in enumerate(courses.values()):
        curr_year_dir = str(list(courses.keys())[i])
        curr_year_dir = clean_string(curr_year_dir)
        subprocess_cmd('cd ' + output_dir_name + '; mkdir ' + curr_year_dir)

        for j, term_values in enumerate(year_values.values()):
            curr_term_dir = str(list(year_values.keys())[j])
            curr_term_dir = clean_string(curr_term_dir)
            subprocess_cmd('cd ' + output_dir_name + '; cd ' + curr_year_dir + ';mkdir ' + curr_term_dir)

            for k, term_value in enumerate(term_values):
                curr_course_dir = str(term_values[k][0])
                curr_course_dir = clean_string(curr_course_dir)
                subprocess_cmd('cd ' + output_dir_name + '; cd ' + curr_year_dir + '; cd ' + curr_term_dir + '; mkdir ' + curr_course_dir)

                url = term_value[1]
                file_urls = get_file_urls_from_page(driver, url)

                for file_url in file_urls:
                    cookies_file_absolute_path = root_dir_path + "/" + "cookies.txt"
                    subprocess_cmd('cd ' + output_dir_name + '; cd ' + curr_year_dir + '; cd ' + curr_term_dir + '; cd ' + curr_course_dir + '; curl -kLOJb ' + cookies_file_absolute_path + ' ' +  file_url)

                print("Files have been downloaded from {}".format(term_value[0]))

# Creates a Chrome driver instance, initiates the transfer of cookies
# between the driver the cookies.txt, verifies user login, calls functions to identify urls
# that point to donwloadable files, and downloades those files
def main():
    consent()
    options = webdriver.ChromeOptions()

    #prohibit automatic downloading by visting a url
    prefs = {"download_restrictions": 3}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options = options)
    cookie_manager = CookieManager(driver)

    school_name = load_institution_moodle(driver)
    cookie_manager.import_cookies_from_file()

    auto_login(driver)
    name_of_user = verify_login(driver)
    cookie_manager.save_cookies()
    
    courses = get_courses(driver)

    download_files(driver, courses, name_of_user)

    driver.close()

if __name__ == '__main__':
    main()