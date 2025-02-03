@user-auth
Feature: Authentication
    Test related to user authentication
    @register
    Scenario: Regiter New User
        Given I register user with correct data
        When after verified the email
        Then I should be able to login & get my access token
    
    @reset-password
    Scenario: Reset Password
        Given: Hitting reset password endpoint w/ email & receive confirm email
        When: Hitting reset confirm endpoint w/ uid, token & $<new_password>
        Then: I should able to login with $<new_password>
        Examples:
        | new_password      |
        | testpassword_new_2 |
