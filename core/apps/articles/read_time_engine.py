"""Utility class for calculate Medium reading time."""

import re
from math import ceil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Article  # Import only for type checking


class ArticleReadTimeEngine:
    """Utility class for calculate Medium reading time."""

    @staticmethod
    def word_count(text: str) -> int:
        """
        Count the number of words in a Medium article.

        Args:
            text (str): Medium article body text.

        Returns:
            int: Number of words count.

        """
        words = re.findall(r"[^\W\d_]+", text, flags=re.UNICODE)
        return len(words)

    @staticmethod
    def get_reading_time(
        article: "Article",
        words_per_min: int = 250,  # Average adult read time
        secs_per_image: int = 10,
        secs_per_tag: int = 2,
    ) -> int:
        """
        Calculate reading by considering article body, image, and tags.

        Args:
            article (Article): Aritcle model instance.
            words_per_min (int, optional): Word reading speed per minutes. Defaults to 250.
            secs_per_image (int, optional): Reading speed per image. Defaults to 10.
            secs_per_tag (int, optional): Reading speed per tag. Defaults to 2.

        Returns:
            float: Calculated reading time (article perminute)

        """
        article_word_count = (
            ArticleReadTimeEngine.word_count(
                article.body,
            )
            + ArticleReadTimeEngine.word_count(article.title)
            + ArticleReadTimeEngine.word_count(article.description)
        )

        read_time = article_word_count / words_per_min

        if article.banner_image:
            read_time += secs_per_image / 60

        read_time += (article.tags.count() * secs_per_tag) / 60

        return ceil(read_time)
