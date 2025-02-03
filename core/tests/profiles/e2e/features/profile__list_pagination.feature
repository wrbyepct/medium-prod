Feature: Profile list pagination

    Scenario: Hit all_profiles endpoint max page size correct
        Given an authenticated client hit all_profiles endpoint with <page_size>
        Then response status code is 200 ok
        * response data contains the <expected> number of results
        Examples:
            | page_size | expected|
            | 7  |  7 |
            | 12 | 12 |
            | 21 | 20 | 

    Scenario: Hit all_profiles endpoint page links work correctly
        Given number of pages derived from <page_size_num> 
        When an authenticated client hit all_profiles endpoint with <page_size_num>
        Then response next page link works correctly
        Examples:
            | page_size_num |
            | 0  |
            | 5 |
            | 21 |
    
