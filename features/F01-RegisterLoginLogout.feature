# Created by denis_petelin at 11/5/18
Feature: Register, login and logout
  As a potential user I want to register, login and logout,
  So I'll be able to upload my files for proofreading

  Background:
    Given the user accesses the url Main Landing Page

  Scenario: Navigate to the Sign Up page
    Given I'm on the Welcome page
    When I click "Register" in the toolbar
    Then the "Sign Up" Page is opened
    When I enter user name which complies with the validation rules
    When I enter password which complies with the validation rules
    When I click "Sign Up"
    Then I'm redirected to the "Main" Page


