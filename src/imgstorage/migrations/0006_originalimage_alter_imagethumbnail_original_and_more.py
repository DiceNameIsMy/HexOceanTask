# Generated by Django 4.0.4 on 2022-05-20 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imgstorage.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('imgstorage', '0005_alter_accounttier_resolutions'),
    ]

    operations = [
        migrations.CreateModel(
            name='OriginalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('image', models.ImageField(upload_to=imgstorage.models.get_upload_path)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_related_name': 'images',
            },
        ),
        migrations.AlterField(
            model_name='imagethumbnail',
            name='original',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imgstorage.originalimage'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
