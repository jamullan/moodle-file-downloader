# Moodle File Downloader
...<br />
<br />
**Last updated (this file):** 9/8/2020<br />
**Author:** John Mullan<br />

## Usage
### Environment Setup
1. Install the [Google Chrome browser](<https://www.google.com/chrome/>) if not already installed
2. Clone this repository
```
$ git clone...
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
```
# Clone this repository
$ git clone ...
```
