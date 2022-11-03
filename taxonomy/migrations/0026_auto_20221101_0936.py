# Generated by Django 3.2.16 on 2022-11-01 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0025_industry'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobskills',
            name='industry',
            field=models.ForeignKey(blank=True, help_text='Industry associated with the job-skill. None industry indicates non-industry specific data.', null=True, on_delete=django.db.models.deletion.CASCADE, to='taxonomy.industry'),
        ),
        migrations.AlterField(
            model_name='jobskills',
            name='job',
            field=models.ForeignKey(help_text='Job associated with the job-skill.', on_delete=django.db.models.deletion.CASCADE, to='taxonomy.job'),
        ),
        migrations.AlterField(
            model_name='jobskills',
            name='skill',
            field=models.ForeignKey(help_text='Skill associated with the job-skill.', on_delete=django.db.models.deletion.CASCADE, to='taxonomy.skill'),
        ),
        migrations.AlterUniqueTogether(
            name='jobskills',
            unique_together={('job', 'skill', 'industry')},
        ),
    ]