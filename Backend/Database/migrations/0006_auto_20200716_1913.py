# Generated by Django 3.0.8 on 2020-07-16 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0005_auto_20200716_1249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='games',
            old_name='result_id',
            new_name='result',
        ),
        migrations.RenameField(
            model_name='loginattempts',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='practice',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='fifth_place_id',
            new_name='fifth_place',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='fourth_place_id',
            new_name='fourth_place',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='second_place_id',
            new_name='second_place',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='sixth_place_id',
            new_name='sixth_place',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='third_place_id',
            new_name='third_place',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='winner_id',
            new_name='winner',
        ),
        migrations.RenameField(
            model_name='useranswers',
            old_name='question_id',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='useranswers',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='userrelationships',
            old_name='user_first_id',
            new_name='user_first',
        ),
        migrations.RenameField(
            model_name='userrelationships',
            old_name='user_second_id',
            new_name='user_second',
        ),
        migrations.RenameField(
            model_name='userscores',
            old_name='game_id',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='userscores',
            old_name='user_id',
            new_name='user',
        ),
    ]
