Feature: Profile list

    Scenario: Hit all_profiles endpoint unauthed should fail
        Given an unauthed client hitting 'all_profiles' endpoint
        Then I should get 401 unauthorized

    Scenario: Hit all_profiles endpoint authed success
        Given there are <size> profiles in databases
        * an authenticated client hit all_profiles endpoint without params
        Then response status code is 200 ok
        * response data contains the <num_of_result> profiles result
        Examples:
            | size | num_of_result |
            | 5  |  5 |
            | 11 | 11 |
    


    
