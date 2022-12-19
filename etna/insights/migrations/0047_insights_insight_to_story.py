# Generated by Django 4.0.8 and condensed to single file.

from django.db import migrations, models
import django.db.models.deletion
import etna.analytics.mixins
import etna.core.blocks.page_list
import etna.insights.blocks
import etna.media.blocks
import etna.records.blocks
import etna.core.blocks.page_list
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks
import wagtailmetadata.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("collections", "0026_collections_insight_to_story"),
        ("home", "0015_home_insight_to_story"),
        ("wagtailimages", "0024_index_image_file_hash"),
        ("wagtailcore", "0077_alter_revision_user"),
        ("insights", "0046_remove_insightsindexpage_featured_collections_and_more"),
    ]

    operations = [
        # _rename_insightspage_storiespage_and_more
        migrations.RenameModel(
            old_name="InsightsPage",
            new_name="StoriesPage",
        ),
        migrations.AlterField(
            model_name="insightsindexpage",
            name="featured_pages",
            field=wagtail.fields.StreamField(
                [
                    (
                        "featuredpages",
                        wagtail.blocks.StructBlock(
                            [
                                ("heading", wagtail.blocks.CharBlock(max_length=100)),
                                (
                                    "description",
                                    wagtail.blocks.TextBlock(max_length=200),
                                ),
                                (
                                    "items",
                                    etna.core.blocks.page_list.PageListBlock(
                                        "insights.StoriesPage", max_num=9, min_num=3
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        # _rename_insightsindexpage_storiesindexpage
        migrations.RenameModel(
            old_name="InsightsIndexPage",
            new_name="StoriesIndexPage",
        ),
        # _rename_featured_insight_storiesindexpage_featured_story
        migrations.RenameField(
            model_name="storiesindexpage",
            old_name="featured_insight",
            new_name="featured_story",
        ),
        # _rename_insightstag_storiestag
        migrations.RenameModel(
            old_name="InsightsTag",
            new_name="StoriesTag",
        ),
        # _alter_storiestag_options
        migrations.AlterModelOptions(
            name="storiestag",
            options={
                "verbose_name": "stories tag",
                "verbose_name_plural": "stories tags",
            },
        ),
        # _rename_taggedinsights_taggedstories
        migrations.RenameModel(
            old_name="TaggedInsights",
            new_name="TaggedStories",
        ),
        # _alter_taggedstories_tag
        migrations.AlterField(
            model_name="taggedstories",
            name="tag",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tagged_stories",
                to="insights.storiestag",
            ),
        ),
        # _rename_insight_tag_names_storiespage_story_tag_names
        migrations.RenameField(
            model_name="storiespage",
            old_name="insight_tag_names",
            new_name="story_tag_names",
        ),
    ]
