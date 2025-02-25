from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDict

from etna.articles.factories import (
    ArticleIndexPageFactory,
    ArticlePageFactory,
    FocusedArticlePageFactory,
)
from etna.collections.factories import TimePeriodPageFactory, TopicPageFactory
from etna.collections.models import PageTimePeriod, PageTopic
from etna.core.test_utils import prevent_request_warnings
from etna.home.factories import HomePageFactory


class NativeWebsiteSearchTestCase(TestCase):
    test_url = reverse_lazy("search-website")

    @classmethod
    def setUpTestData(cls):
        cls.homepage = HomePageFactory()
        cls.article_index = ArticleIndexPageFactory(parent=cls.homepage)

        # ---------------------------------------------------------------------
        # Create topic and time period pages to use in taxonomies
        # ---------------------------------------------------------------------

        # NOTE: These would normally be added under special 'index' pages, but that doesn't matter for
        # these tests

        cls.arts = TopicPageFactory(title="Arts and culture", parent=cls.homepage)
        cls.military = TopicPageFactory(title="Military and war", parent=cls.homepage)
        cls.health = TopicPageFactory(title="Health and welfare", parent=cls.homepage)
        cls.transport = TopicPageFactory(
            title="Transport and travel", parent=cls.homepage
        )

        cls.early_modern = TimePeriodPageFactory(
            title="Early modern",
            start_year=1485,
            end_year=1714,
            parent=cls.homepage,
        )
        cls.georgians = TimePeriodPageFactory(
            title="Georgians",
            start_year=1714,
            end_year=1837,
            parent=cls.homepage,
        )
        cls.interwar = TimePeriodPageFactory(
            title="Interwar",
            start_year=1918,
            end_year=1939,
            parent=cls.homepage,
        )
        cls.postwar = TimePeriodPageFactory(
            title="Postwar", start_year=1945, end_year=2030, parent=cls.homepage
        )

        # ---------------------------------------------------------------------
        # Create 'foo' pages
        # ---------------------------------------------------------------------

        # These pages should match the 'foo' search term and/or a designated set of topic/time_period filters

        cls.foo_article = ArticlePageFactory(
            parent=cls.article_index,
            title="Foo article",
            page_topics=[
                PageTopic(topic=cls.arts),
                PageTopic(topic=cls.health),
            ],
            page_time_periods=[
                PageTimePeriod(time_period=cls.early_modern),
                PageTimePeriod(time_period=cls.georgians),
            ],
        )
        cls.foo_focussed_article = FocusedArticlePageFactory(
            parent=cls.article_index,
            title="Foo focussed article",
            page_topics=[
                PageTopic(topic=cls.arts),
                PageTopic(topic=cls.health),
            ],
            page_time_periods=[
                PageTimePeriod(time_period=cls.early_modern),
                PageTimePeriod(time_period=cls.georgians),
            ],
        )

        # ---------------------------------------------------------------------
        # Create 'bar' pages
        # ---------------------------------------------------------------------

        # These pages should match the 'bar' search term and/or a designated set of topic/time_period filters

        cls.bar_article = ArticlePageFactory(
            parent=cls.article_index,
            title="Bar article",
            page_topics=[
                PageTopic(topic=cls.military),
                PageTopic(topic=cls.transport),
            ],
            page_time_periods=[
                PageTimePeriod(time_period=cls.interwar),
                PageTimePeriod(time_period=cls.postwar),
            ],
        )
        cls.bar_focussed_article = FocusedArticlePageFactory(
            parent=cls.article_index,
            title="Bar focussed article",
            page_topics=[
                PageTopic(topic=cls.military),
                PageTopic(topic=cls.transport),
            ],
            page_time_periods=[
                PageTimePeriod(time_period=cls.interwar),
                PageTimePeriod(time_period=cls.postwar),
            ],
        )

        # ---------------------------------------------------------------------
        # Create 'outlier' pages
        # ---------------------------------------------------------------------

        # We'll use these to prove searching and filtering at the same time excludes matches that don't match both criteria

        cls.foo_article_with_no_tags = ArticlePageFactory(
            title="Foo article without tags", parent=cls.article_index
        )

        cls.bar_article_without_tags = ArticlePageFactory(
            title="Bar article without tags", parent=cls.article_index
        )

        cls.foo_article_with_alternative_tags = ArticlePageFactory(
            title="Foo article with alternative tags",
            parent=cls.article_index,
            page_topics=[PageTopic(topic=cls.military)],
            page_time_periods=[PageTimePeriod(time_period=cls.interwar)],
        )

        cls.bar_article_with_alternative_tags = ArticlePageFactory(
            title="Bar article with alternative tags",
            parent=cls.article_index,
            page_topics=[PageTopic(topic=cls.arts)],
            page_time_periods=[PageTimePeriod(time_period=cls.georgians)],
        )

        cls.all_result_pages = [
            cls.arts,
            cls.military,
            cls.health,
            cls.transport,
            cls.early_modern,
            cls.georgians,
            cls.interwar,
            cls.postwar,
            cls.foo_article,
            cls.foo_focussed_article,
            cls.foo_article_with_no_tags,
            cls.bar_article,
            cls.bar_focussed_article,
            cls.bar_article_without_tags,
            cls.foo_article_with_alternative_tags,
            cls.bar_article_with_alternative_tags,
        ]

        # ---------------------------------------------------------------------
        # Setup values to use in test GET data
        # ---------------------------------------------------------------------

        cls.article_and_record_article_type_strings = [
            "articles.articlepage",
            "articles.recordarticlepage",
        ]
        cls.foo_topic_slugs = [cls.arts.slug, cls.health.slug]
        cls.foo_time_period_slugs = [cls.early_modern.slug, cls.georgians.slug]
        cls.bar_topic_slugs = [cls.military.slug, cls.transport.slug]
        cls.bar_time_period_slugs = [cls.interwar.slug, cls.postwar.slug]

    def test_view_all(self):
        """
        Tests the view without any search terms or filters applied.
        """
        response = self.client.get(self.test_url, data={"per_page": 20})
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            [p.specific for p in response.context["page"].object_list],
            self.all_result_pages,
        )

        # No filters are selected, so 'Selected filters' should not be present
        self.assertNotContains(response, '<h2 class="sr-only">Selected filters</h2>')

    def test_sorting(self):
        for sort_by, expected_results in (
            (
                "title",
                sorted(self.all_result_pages, key=lambda p: p.title),
            ),
            (
                "-title",
                sorted(self.all_result_pages, key=lambda p: p.title, reverse=True),
            ),
            (
                "first_published_at",
                sorted(
                    self.all_result_pages,
                    key=lambda p: p.first_published_at,
                ),
            ),
            (
                "-first_published_at",
                sorted(
                    self.all_result_pages,
                    key=lambda p: p.first_published_at,
                    reverse=True,
                ),
            ),
        ):
            with self.subTest(f"Sort by: {sort_by}"):
                response = self.client.get(self.test_url, data={"sort_by": sort_by})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    [p.specific for p in response.context["page"].object_list],
                    expected_results[:15],
                )

    def test_pagination(self):
        response = self.client.get(self.test_url, data={"per_page": 10})
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(
            response,
            'role="button" rel="prev" data-link-type="Pagination" data-link="Previous page"',
            html=True,
        )
        self.assertContains(
            response,
            '<a class="tna-button tna-button--accent tna-pagination__link" href="?per_page=10&amp;page=1" aria-label="Page 1" data-link-type="Pagination" data-link="1" role="button" aria-current="page">1</a>',
            html=True,
        )
        self.assertContains(
            response,
            '<a class="tna-button tna-pagination__link" href="?per_page=10&amp;page=2" aria-label="Page 2" data-link-type="Pagination" data-link="2" role="button">2</a>',
            html=True,
        )
        self.assertContains(
            response,
            '<a class="tna-button tna-pagination__link" href="?per_page=10&amp;page=2" role="button" rel="next" data-link-type="Pagination" data-link="Next page"><span class="tna-pagination__link-title">Next</span><svg class="tna-pagination__icon tna-pagination__icon--next" xmlns="http://www.w3.org/2000/svg" height="13" width="15" aria-hidden="true" focusable="false" viewBox="0 0 15 13"><path d="m8.107-0.0078125-1.4136 1.414 4.2926 4.293h-12.986v2h12.896l-4.1855 3.9766 1.377 1.4492 6.7441-6.4062-6.7246-6.7266z"></path></svg></a>',
            html=True,
        )

    def test_filter_by_format(self):
        """
        Tests the view with only the 'format' filter applied.
        """
        response = self.client.get(
            self.test_url,
            data=MultiValueDict(
                {"format": self.article_and_record_article_type_strings}
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            [p.specific for p in response.context["page"].object_list],
            [
                self.foo_article,
                self.foo_article_with_no_tags,
                self.foo_article_with_alternative_tags,
                self.bar_article,
                self.bar_article_without_tags,
                self.bar_article_with_alternative_tags,
            ],
        )

        # 'Selected filters' should reflect the values in GET
        self.assertContains(response, '<h2 class="sr-only">Selected filters</h2>')
        for label in ["article", "record article"]:
            self.assertContains(response, f"Remove Format: {label} from search")
        for label in [
            "highlight gallery page",
            "time period page",
            "topic page",
        ]:
            self.assertNotContains(response, f"Remove Format: {label} from search")

    def test_filter_by_topic(self):
        """
        Tests the view with only the 'topic' filter applied.
        """
        response = self.client.get(
            self.test_url, data=MultiValueDict({"topic": self.foo_topic_slugs})
        )
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            [p.specific for p in response.context["page"].object_list],
            [
                # these have two matching topics
                self.foo_article,
                self.foo_focussed_article,
                # this has one matching topic
                self.bar_article_with_alternative_tags,
            ],
        )

        # 'Selected filters' should reflect the values in GET
        self.assertContains(response, '<h2 class="sr-only">Selected filters</h2>')
        for topic in [self.arts, self.health]:
            self.assertContains(response, f"Remove Topic: {topic.title} from search")
        for topic in [self.military, self.transport]:
            self.assertNotContains(response, f"Remove Topic: {topic.title} from search")

    def test_filter_by_time_period(self):
        """
        Tests the view with ONLY the 'time_period' filter applied.
        """
        response = self.client.get(
            self.test_url,
            data=MultiValueDict({"time_period": self.bar_time_period_slugs}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            [p.specific for p in response.context["page"].object_list],
            [
                # these have two matching time periods
                self.bar_article,
                self.bar_focussed_article,
                # this has one matching time period
                self.foo_article_with_alternative_tags,
            ],
        )

        # 'Selected filters' should reflect the values in GET
        self.assertContains(response, '<h2 class="sr-only">Selected filters</h2>')
        for time_period in [self.interwar, self.postwar]:
            self.assertContains(
                response, f"Remove Time period: {time_period.title} from search"
            )
        for time_period in [self.early_modern, self.georgians]:
            self.assertNotContains(
                response, f"Remove Time period: {time_period.title} from search"
            )

    def test_search_for_foo(self):
        """
        Tests the view using the 'foo' search term in isolation (without any filters)
        """
        response = self.client.get(self.test_url, data={"q": "foo"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p.specific for p in response.context["page"].object_list],
            [
                self.foo_article,
                self.foo_focussed_article,
                self.foo_article_with_alternative_tags,
                self.foo_article_with_no_tags,
            ],
        )

    def test_search_for_foo_ordered_by_title(self):
        response = self.client.get(self.test_url, data={"q": "foo", "sort_by": "title"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p.specific for p in response.context["page"].object_list],
            [
                self.foo_article,
                self.foo_article_with_alternative_tags,
                self.foo_article_with_no_tags,
                self.foo_focussed_article,
            ],
        )

    def test_search_for_foo_with_multiple_filters(self):
        """
        Tests the view using the 'foo' search term AND a combination of filters that
        should match most 'foo' pages.
        """
        response = self.client.get(
            self.test_url,
            data=MultiValueDict(
                {
                    "q": "foo",
                    # This will rule out 'foo_focussed_article'
                    "format": self.article_and_record_article_type_strings,
                    # This will rule out 'foo_article_with_no_tags' and 'foo_article_with_alternative_tags'
                    "topic": self.foo_topic_slugs,
                }
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p.specific for p in response.context["page"].object_list],
            [self.foo_article],
        )

    def test_search_for_bar(self):
        """
        Tests the view using the 'bar' search term in isolation (without any filters)
        """
        response = self.client.get(
            self.test_url,
            data={
                "q": "bar",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p.specific for p in response.context["page"].object_list],
            [
                self.bar_article,
                self.bar_focussed_article,
                self.bar_article_with_alternative_tags,
                self.bar_article_without_tags,
            ],
        )

    def test_search_for_bar_ordered_by_title(self):
        """
        Tests the view using the 'bar' search term in isolation (without any filters)
        """
        response = self.client.get(self.test_url, data={"q": "bar", "sort_by": "title"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p.specific for p in response.context["page"].object_list],
            [
                self.bar_article,
                self.bar_article_with_alternative_tags,
                self.bar_article_without_tags,
                self.bar_focussed_article,
            ],
        )

    def test_search_for_bar_with_multiple_filters(self):
        """
        Tests the view using the 'bar' search term AND a combination of filters that
        should match most 'bar' pages.
        """
        response = self.client.get(
            self.test_url,
            data=MultiValueDict(
                {
                    "q": "bar",
                    # This will rule out 'bar_focussed_article'
                    "format": self.article_and_record_article_type_strings,
                    # This will rule out 'bar_article_without_tags' and 'bar_article_with_alternative_tags'
                    "time_period": self.bar_time_period_slugs,
                }
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p.specific for p in response.context["page"].object_list],
            [self.bar_article],
        )

    def test_search_with_custom_AND_operator(self):
        for search_terms, expected_result_count in (
            ("foo AND article", 4),
            ("foo AND article AND focussed", 1),
            ("foo AND bar", 0),
        ):
            with self.subTest(f"Searching for: {search_terms}"):
                response = self.client.get(self.test_url, data={"q": search_terms})
                self.assertEqual(
                    response.context_data["paginator"].count,
                    expected_result_count,
                )

    def test_no_results_search(self):
        """
        Tests the view using the 'baz' search term, which should match zero pages.
        """
        response = self.client.get(self.test_url, data={"q": "baz"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["paginator"].count, 0)
        self.assertContains(
            response,
            '<h2 class="tna-heading-l featured-search__heading">We did not find any results for your search</h2>',
            html=True,
        )

    @prevent_request_warnings
    def test_httpresponsebadrequest_recieved_when_bad_values_provided(self):
        for field_name, value in [
            ("per_page", "bar"),
            ("per_page", 10000),
            ("sort_by", "baz"),
            ("display", "foo"),
        ]:
            with self.subTest(f"{field_name} = {value}"):
                response = self.client.get(self.test_url, data={field_name: value})
                self.assertEqual(response.status_code, 400)
