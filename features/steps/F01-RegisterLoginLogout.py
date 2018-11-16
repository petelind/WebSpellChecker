from behave import *
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from datetime import date


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


@given("I'm on the Welcome page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.selenium.get(context.live_server_url)
    header = context.selenium.find_element_by_tag_name('h1')
    assert ('Typonator' == header.text)


@when('I click "{action}"')
def step_impl(context, action):
    """
    :param action:
    :type context: behave.runner.Context
    """
    action_link = context.selenium.find_element_by_id(action)
    action_link.click()


@then('the "{view_name}" Form is opened saying "{header}"')
def step_impl(context, view_name, header):
    """
    :type context: behave.runner.Context
    """
    form_header = context.selenium.find_element_by_class_name('lead')
    assert (form_header.text == header)


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

@then('I\'m redirected to the "Main" Page')
def step_impl(context):
    """
    :type context: behave.runner.Context SpellChecker - Your Files
    """
    page_header = context.selenium.find_element(By.TAG_NAME, 'h1')

    assert (page_header.text == 'Typonator')



@step("I'm Logged In")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    welcome_message = context.selenium.find_element(By.ID, 'hello')

    assert (welcome_message.text == 'Hello, ' + context.username + '!')

@given("Valid user exists")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    new_user = User.objects.create_user(username=context.username, password=context.password, email="valid@email.com")

@when("I Log in as a valid user")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.selenium.get(context.live_server_url)
    login_button = context.selenium.find_element(By.ID, 'login')
    login_button.click()

    username_field = context.selenium.find_element(By.ID, 'id_username')
    username_field.send_keys(context.username)

    password_field = context.selenium.find_element(By.ID, 'id_password')
    password_field.send_keys(context.password)

    submit_button = context.selenium.find_element(By.ID, 'btnSubmit')
    submit_button.click()


@then("I'm logged out")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    login_button = context.selenium.find_element(By.ID, 'login')

    assert (login_button.text == 'Log in')

    context.selenium.quit()


@when("I Log in as an invalid user")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.selenium.get(context.live_server_url)
    login_button = context.selenium.find_element(By.ID, 'login')
    login_button.click()

    username_field = context.selenium.find_element(By.ID, 'id_username')
    username_field.send_keys(context.username + 'a')

    password_field = context.selenium.find_element(By.ID, 'id_password')
    password_field.send_keys(context.password + 'a')

    submit_button = context.selenium.find_element(By.ID, 'btnSubmit')
    submit_button.click()


@then('I\'m getting message "{message}"')
def step_impl(context, message):
    """
    :type context: behave.runner.Context
    """
    error = context.selenium.find_element(By.TAG_NAME, 'li')
    assert (error.text == message)


@step("Cannot access Files")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # files_url = context.live_server_url + reversed('home')
    context.selenium.get(context.live_server_url + reverse('home'))

    form_name = context.selenium.find_element(By.CLASS_NAME, 'lead')
    assert form_name.text == 'Please login'

