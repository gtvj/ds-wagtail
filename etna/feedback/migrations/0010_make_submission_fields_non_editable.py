# Generated by Django 4.2.2 on 2023-07-04 16:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedback", "0009_feedbackpromptpagetype"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="comment",
            field=models.TextField(editable=False, verbose_name="comment"),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="comment_prompt_text",
            field=models.CharField(
                editable=False,
                max_length=200,
                verbose_name="comment prompt text",
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="full_url",
            field=models.TextField(editable=False, verbose_name="full URL"),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="page",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="wagtailcore.page",
                verbose_name="wagtail page",
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="page_revision",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.revision",
                verbose_name="page revision",
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="page_revision_published",
            field=models.DateTimeField(
                editable=False,
                null=True,
                verbose_name="page revision published at",
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="path",
            field=models.CharField(
                db_index=True,
                editable=False,
                max_length=255,
                verbose_name="path",
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="prompt",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="submissions",
                to="feedback.feedbackprompt",
                verbose_name="prompt",
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="prompt_revision",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.revision",
                verbose_name="prompt revision",
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="prompt_text",
            field=models.CharField(
                editable=False, max_length=200, verbose_name="prompt text"
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="query_params",
            field=models.JSONField(
                default=dict, editable=False, verbose_name="query params"
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="response_label",
            field=models.CharField(
                db_index=True,
                editable=False,
                max_length=100,
                verbose_name="response label",
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="response_sentiment",
            field=models.SmallIntegerField(
                db_index=True, editable=False, verbose_name="response sentiment"
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="site",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.PROTECT,
                to="wagtailcore.site",
                verbose_name="site",
            ),
        ),
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="user",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
    ]
