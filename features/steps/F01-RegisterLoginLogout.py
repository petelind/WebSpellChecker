from behave import *
from django.contrib.auth.models import User
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

use_step_matcher("re")


@given("the user accesses the url Main Landing Page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.selenium = WebDriver()
    context.selenium.implicitly_wait(5)

    context.username = 'valid_user'
    context.password = 'Valid_password1'

    context.live_server_url = context.get_url()
    # context.live_server_url = 'localhost:8000'

@given("I'm on the Welcome page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.selenium.get(context.live_server_url)
    header = context.selenium.find_element_by_tag_name('h1')
    assert ('Typonator' == header.text)


@when('I click "Register" in the toolbar')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    signup_link = context.selenium.find_element_by_id('signup')
    signup_link.click()


@then('the "Sign Up" Page is opened')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    form_header = context.selenium.find_element_by_class_name('lead')
    assert (form_header.text == 'Sign up')


@given('i\'m on the "Sign Up" Page')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    form_header = context.selenium.find_element_by_class_name('lead')
    assert (form_header.text == 'Sign up')


@when("I enter user name which complies with the validation rules")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    username_field = context.selenium.find_element(By.NAME, 'username')
    username_field.send_keys(context.username)


@when("I enter password which complies with the validation rules")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    username_field = context.selenium.find_element(By.NAME, 'password1')
    username_field.send_keys(context.password)

    username_field = context.selenium.find_element(By.NAME, 'password2')
    username_field.send_keys(context.password)


@when('I click "Sign Up"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    signup_button = context.selenium.find_element(By.ID, 'submitButton')
    signup_button.click()
    context.selenium.implicitly_wait(1)

@then('I\'m redirected to the "Main" Page')
def step_impl(context):
    """
    :type context: behave.runner.Context SpellChecker - Your Files
    """
    page_header = context.selenium.find_element(By.TAG_NAME, 'h1')
    welcome_message = context.selenium.find_element(By.ID, 'hello')
    print(welcome_message.text)
    assert (page_header.text == 'Typonator')
    assert (welcome_message.text == 'Hello, ' + context.username + '!')

    context.selenium.quit()

