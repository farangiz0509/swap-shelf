
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=124)),
                ('author', models.CharField(max_length=64)),
                ('condition', models.CharField(choices=[('new', 'New'), ('good', 'Good'), ('fair', 'Fair'), ('worn', 'Worn')], default='good')),
                ('type', models.CharField(choices=[('borrow', 'Borrow'), ('permanent', 'Permanent'), ('both', 'Both')], default='borrow')),
                ('description', models.CharField(max_length=999)),
                ('image', models.URLField()),
                ('status', models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available')),
                ('share', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='books.genre')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
