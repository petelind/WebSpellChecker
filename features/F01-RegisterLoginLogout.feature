# Created by denis_petelin at 11/5/18
Feature: Register, login and logout
  As a potential user I want to register, login and logout,
  So I'll be able to upload my files for proofreading

  Background:
    Given the user accesses the url Main Landing Page

  Scenario: Register New User
    Given I'm on the Welcome page
    When I click "signup"
    Then the "Sign Up" Form is opened saying "Sign up"
    When I enter user name which complies with the validation rules
    When I enter password which complies with the validation rules
    When I click "submitButton"
    Then I'm redirected to the "Main" Page
    And I'm Logged In

  Scenario: Login and Logout as a Valid User
    Given Valid user exists
    When I Log in as a valid user
    Then I'm Logged In
    When I click "logout"
    Then I'm logged out

  Scenario: Login as non-existent user
    When I Log in as an invalid user
    Then I'm getting message "Please enter a correct username and password. Note that both fields may be case-sensitive."
    And Cannot access Files