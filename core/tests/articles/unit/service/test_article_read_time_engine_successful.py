# ruff: noqa: ARG002

import pytest

from core.apps.articles.read_time_engine import ArticleReadTimeEngine

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "text, expected_count",
    [
        # 1. Basic text with normal spacing
        ("Hello world", 2),
        # 2. Text with punctuation
        ("Hello, world! This is a test.", 6),
        # Explanation: The words are ["Hello", "world", "This", "is", "a", "test"]
        # 3. Mixed punctuation and numbers
        ("Count 123 apples, oranges, and bananas!", 5),
        # Explanation: ["Count", "123", "apples", "oranges", "and", "bananas"]
        # 4. Empty string
        ("", 0),
        # 5. Only whitespace
        ("   \t   \n   ", 0),
        # 6. Multiple spaces between words
        ("Multiple   spaces   between words", 4),
        # Explanation: ["Multiple", "spaces", "between", "words"]
        # 7. Special characters & symbols
        ("@#$%^&*()_+ ~!?", 0),
        # Explanation: No alphanumeric substrings found by \w+
        # 8. Multiline input
        (
            """Line one
       Line two 
       Line three""",
            6,
        ),
        # 9. Unicode characters (letters with accents)
        ("Café müßten wir besuchen", 4),
        # 10. Mixed Unicode (emojis, non-Latin scripts)
        ("Hello 😊 你好 Привет", 3),
    ],
)
def test_article_read_time_engine__word_count_correct(text, expected_count):
    assert ArticleReadTimeEngine.word_count(text) == expected_count


# Mock the function .update() called by ArticleDocument to prevent index update


def test_artciel_read_time_engine__get_read_time_with_tags_no_image(
    mock_article_index_update,
    article_factory,
):
    """
    Scenario:
      - Article has:
        2 words in the title
        3 words in the description
        1000 words in the body
        2 tags
        No banner image
      - Words per minute: 250 (default)
      - secs_per_image: 10 (default) → not used (no image)
      - secs_per_tag: 2 (default) → 2 tags
    """
    # Arrange: Create an article instance
    article = article_factory.create(
        title="Short Title",  # 2 words
        description="Great article content",  # 3 words
        body=" ".join(["Hello world again now thanks"] * 200),  # 1000 words
        banner_image=None,  # No banner
        tags=["django", "python"],  # 2 tags
    )

    # Act: Calculate reading time
    reading_time = ArticleReadTimeEngine.get_reading_time(article)

    # Let's manually compute what we expect:
    # 1) Word count = (1000 + 2 + 3) = 10 words total.
    # 2) Base read_time = 1005 words / 250 wpm = 4 minutes.
    # 3) No banner image => no additional time from secs_per_image.
    # 4) 2 tags => 2 * 2 secs = 4 seconds -> 4 / 60 = 0.0667 minutes
    # 5) Total read_time = 4 + 0.0667 = 4.1067 => ceil(4.1067) = 5
    assert reading_time == 5  # noqa: PLR2004
