import os
import subprocess

from nose.tools import istest, assert_equals
from selenium import webdriver

from tempdir import create_temporary_dir


# TODO: select free port
@istest
def running_apache2_after_installation_shows_default_page():
    with create_temporary_dir() as temp_dir:
        install_apache2(temp_dir, port=54321)
        process = start_apache2(temp_dir)
        try:
            assert_default_apache_page_is_visible(port=54321)
        finally:
            process.terminate()

def install_apache2(directory, port):
    path = os.path.join(os.path.dirname(__file__), "..")
    subprocess.check_call(["whack", "install", path, directory, "-pport={0}".format(port), "--no-cache"])

def start_apache2(temp_dir):
    return subprocess.Popen(["bin/httpd", "-DNO_DETACH"], cwd=temp_dir)

def assert_default_apache_page_is_visible(port):
    url = "http://localhost:{0}/".format(port)
    browser = webdriver.Firefox()
    try:
        browser.get(url)
        element = browser.find_element_by_css_selector("h1")
        assert_equals("It works!", element.text)
    finally:
        browser.close()
