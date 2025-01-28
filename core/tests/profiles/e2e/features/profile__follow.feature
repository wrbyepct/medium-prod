Feature: Follow profile
    
    Background:
        Given a fan user with profile exists
        * an idol user with profile exists
        * client authenticate with fan
    
    # Follow
    Scenario: Follow other user successful
        When fan follows idol, email should be sent
        Then fan should get 200 ok & success message
    
    Scenario: Follow non-existing user should fail
        When fan follows none-existing user
        Then fan should get 404 not found & follow failed message

    Scenario: Repeat follow should fail
        Given fan has followed idol
        When fan follows idol
        Then the fan should get 400 bad request & repeat follow failed message
    
    Scenario: Follow self should fail
        When the fan follows self
        Then the fan should get 400 bad request & follow self failed message

    # Unfollow
    Scenario: Unfollow a user success
        Given fan has followed idol
        When the fan unfollows idol
        Then fan should get 200 ok & unfollow success message

    Scenario: Unfollow non-existing user should fail
        When fan unfollows none-existing user
        Then fan should get 404 not found & unfollow failed message
    
    Scenario: Unfollow user you haven't followed should fail
        When fan tries to unfollow a user that they haven't followed
        Then fan should get 400 bad request & unfollow failed message
