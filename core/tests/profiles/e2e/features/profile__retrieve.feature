Feature: Profile retrieve
    
    Scenario: Hit 'me' endpoint unauthed should fail
        Given an unauthed client hitting 'all_profiles' endpoint
        Then I should get response 401 unauthorized

    Scenario: Hit 'me' endpoint authed success
        Given a user with profile
        When hitting 'me' url with client authend by the user
        Then I should get response 200 ok
