"""'Static' API argument options used in making API calls."""


class RESTRICT: # pylint: disable=too-few-public-methods
    """Restriction options for API calls."""

    PUBLIC = 'public'
    PRIVATE = 'private'


class FILTER:   # pylint: disable=too-few-public-methods
    """Filter options for API calls."""

    FOR_ANDROID = 'for_android'
    FOR_IOS = 'for_ios'


class ARTICLE_CATEGORY: # pylint: disable=too-few-public-methods,invalid-name
    """Category options for article-related API calls."""

    ALL = 'all'             # All of the articles across all categories
    SPOTLIGHT = 'spotlight' # Spotlight articles, featured Pixiv articles


class RANK_MODE:        # pylint: disable=too-few-public-methods,invalid-name
    """Mode options for specifying retrieving rankings."""

    # Time-only based modes
    DAY = 'day'     # The most popular rankings for today.
    WEEK = 'week'   # The most popular rankings for this week.
    MONTH = 'month' # The most popular rankings for this month.
    # Time and gender based modes.
    DAY_MALE = DAY+'_male'      # The most popular rankings for today amongst males.
    DAY_FEMALE = DAY+'_female'  # The most popular rankings for today amongst females.
