# Generated by Ginger 5.3.4 on 2024-07-13 15:55

from gingerdj.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("src", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="owners",
            field=models.ManyToManyField(related_name="managed_groups", to="src.user"),
        ),
    ]
