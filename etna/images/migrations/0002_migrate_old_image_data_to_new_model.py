# Generated by Django 3.2.14 on 2022-09-20 15:53

from django.db import migrations


def migrate_forwards(apps, schema_editor):
    # Copy images to new table, retaining IDs and all other values
    Image = apps.get_model("wagtailimages", "Image")
    CustomImage = apps.get_model("images", "CustomImage")
    to_create = []
    for item in Image.objects.all().values().iterator():
        to_create.append(CustomImage(**item))
        # Save in batches of 1000 to avoid memory spikes
        if len(to_create) > 1000:
            CustomImage.objects.bulk_create(to_create)
            to_create.clear()
    # Save any left-overs
    CustomImage.objects.bulk_create(to_create)

    # Get content types for tag copying
    ContentType = apps.get_model("contenttypes", "ContentType")
    old_ctype = ContentType.objects.get(app_label="wagtailimages", model="image")
    new_ctype, _ = ContentType.objects.get_or_create(
        app_label="images", model="CustomImage"
    )

    # Copy image tags
    TaggedItem = apps.get_model("taggit.TaggedItem")
    to_create = []
    for tag_id, object_id in (
        TaggedItem.objects.filter(content_type=old_ctype)
        .values_list("tag_id", "object_id")
        .iterator()
    ):
        to_create.append(
            TaggedItem(tag_id=tag_id, object_id=object_id, content_type=new_ctype)
        )
        # Save in batches of 1000 to avoid memory spikes
        if len(to_create) > 1000:
            TaggedItem.objects.bulk_create(to_create)
            to_create.clear()
    # Save any left-overs
    TaggedItem.objects.bulk_create(to_create)


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0024_index_image_file_hash"),
        ("taggit", "0004_alter_taggeditem_content_type_alter_taggeditem_tag"),
        ("images", "0001_initial"),
    ]

    operations = [
        # Copy data from existing tables
        migrations.RunPython(migrate_forwards, migrations.RunPython.noop),
        # When running forwards, increment autoid to reflect additions
        migrations.RunSQL(
            'SELECT setval(pg_get_serial_sequence(\'"images_customimage"\',\'id\'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "images_customimage";',
            migrations.RunSQL.noop,
        ),
    ]
