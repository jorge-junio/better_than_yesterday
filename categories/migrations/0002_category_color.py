# Generated manually to add a display color to categories.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(default='#0f766e', max_length=7, verbose_name='cor'),
        ),
    ]

