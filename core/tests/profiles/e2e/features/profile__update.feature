Feature: Profile update
    @qqq
    Scenario: Hitting update profile endpoint successfully
        Given user update info
        When hitting me_update_profile with authed client
        Then I should get response 200 ok 
        * response data updated correct
