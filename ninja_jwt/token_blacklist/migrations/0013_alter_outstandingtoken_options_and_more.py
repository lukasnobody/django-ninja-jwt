import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('token_blacklist', '0012_alter_outstandingtoken_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='outstandingtoken',
            options={'ordering': ('user_object_id',)},
        ),
        migrations.RemoveField(
            model_name='outstandingtoken',
            name='user',
        ),
        migrations.AddField(
            model_name='outstandingtoken',
            name='user_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='outstandingtoken',
            name='user_object_id',
            field=models.CharField(max_length=255, null=True, blank=True)
        ),
    ]
