@get_followers
Feature: Get Profile Followers or Following
 
    Scenario: Get User Followers
        Given a profile with followers exists
        When hitting profile user_follower enpdoint
        Then I should get 200 ok response from user_followers endpoint
        * the user's followers profiles data correct


    Scenario: Get User Following
        Given a profile with following of 3 exists
        When hitting profile user_following endpoint
        Then I should get 200 ok response from user_following endpoint
        * the user's following profile data correct
