# Moodle File Downloader
A Python-based program that uses Selenium to automate the process of downloading files across all of a student's Moodle course pages<br />
<br />
**NOTICE**: This program interacts with enterprise file storage systems and downloads files that despite you having authorized access to, you may not be able to share with others (e.g., solutions provided to you by your instructor). If you are *not* provided with a series of questions that you can agree or disagree to in the command line by the program, you should NOT continue its use.
**Last updated (this file):** 9/8/2020<br />
**Author:** John Mullan<br />

## Usage
### Environment Setup
1. Install the [Google Chrome browser](<https://www.google.com/chrome/>) if not already installed
2. Clone this repository
```
$ git clone https://github.com/jamullan/moodle-file-downloader.git
```
3. Download the [ChromeDriver](<https://chromedriver.chromium.org>) and place the `chromedriver` executable in the root directory of this repository
4. Create a Python virtual environment in the root directory
```
$ python3 -m venv my_venv
```
5. Grant yourself execution permission for the activation executable within the Python virtual environment
```
$ chmod u+x my_venv/bin/activate
```
6. Activate the Python virtual environment
```
$ . my_venv/bin/activate
```
7. Install Selenium
```
$ pip3 install selenium
```
8. Replace Selenium's Chrome `webdriver.py` file with the one in the root directory of this repository to set Selenium's executable path to the `chromedriver` in the root directory of this repository(**NOTE: if this fails, you may be using a newer version of Python. Replace** `python3.7` **in the path with the appropriate version**)
```
$ mv webdriver.py my_venv/lib/python3.7/site-packages/selenium/webdriver/chrome
```
Alternatively, you can perform the following insertions into the existing `webdriver.py` file in `my_venv/lib/python3.7/site-packages/selenium/webdriver/chrome`:
* Along with the other package import:
```python
import os
```
* At the very top of the `__init__` method:
```python
curr_file_path = os.path.abspath(".")
executable_path = curr_file_path + "/" + "chromedriver"
```
### How to Run
1. Navigate to the root directory of this repository
2. Activate the Python virtual environment
```
$ . my_venv/bin/activate
```
3. Start the program and follow the prompts in the command line. **NOTE**: If you are *not* provided with a series of questions that you can agree or disagree to in the command line by the program, you should NOT continue its use.
```
$ python3 moodle_file_downloader.py
```
4. If using Duo or another 2FA, you must check "remember me for 60 days" (or its equivalent option) when prompted
5. When complete, a directory within the root directory of this repository will have your downloaded files (note: this will NOT work for courses where each week's files require you to click on the week to view them, nor will it download a file of folders; videos may be inconsistently downloaded)
