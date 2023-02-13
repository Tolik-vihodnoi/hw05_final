# Generated by Django 2.2.16 on 2023-02-13 16:57

from django.db import migrations, models
import django.db.models.expressions


def forwards_func(apps, schema_editor):
    Follow = apps.get_model("posts", "Follow")
    db_alias = schema_editor.connection.alias
    Follow.objects.using(db_alias).filter(user=models.F("author")).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20230210_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='Текст комментария', verbose_name='Текст комментария'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Картинка', upload_to='posts/', verbose_name='Изображение'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_follow'),
        ),
        migrations.RunPython(
            code=forwards_func,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name="user isn't an author"),
        ),
    ]