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
    

    Scenario: Hit all_profiles endpoint max page size correct
        Given there are 21 profiles in databases
        When an authenticated client hit all_profiles endpoint with <page_size>
        Then response status code is 200 ok
        * response data contains the <expected> number of results
        Examples:
            | page_size | expected|
            | 7  |  7 |
            | 12 | 12 |
            | 21 | 20 | 

    Scenario: Hit all_profiles endpoint page links work correctly
        Given there are 21 profiles in databases
        * number of pages derived from <page_size_num>
        When an authenticated client hit all_profiles endpoint with <page_size_num>
        Then response status code is 200 ok
        * response next page link works correctly
        Examples:
            | page_size_num |
            | 0  |
            | 5 |
            | 21 |
    
