
import core.models._Advisor
import core.models._Guide
import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_no', models.CharField(max_length=20)),
                ('user_type', models.CharField(choices=[('individual', 'Individual'), ('high_school_counsellor', 'High School Counsellor')], max_length=50)),
                ('high_school_name', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', '0'), ('approved', '1'), ('rejected', '2'), ('scheduled', '3')], default='pending', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('reviewRating', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('director', 'Director'), ('secretary', 'Secretary'), ('coordinator', 'Coordinator'), ('advisor', 'Advisor'), ('guide', 'Guide'), ('visitor', 'Visitor')], max_length=20)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('profile_picture', models.URLField(blank=True, default='https://via.placeholder.com/150?text=No+Profile', max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorizedDay', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=core.models._Advisor.default_authorized_day, size=7)),
                ('isCoordinator', models.BooleanField(default=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advisor_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('participant1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats_as_participant1', to=settings.AUTH_USER_MODEL)),
                ('participant2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats_as_participant2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('participant1', 'participant2')},
            },
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=0.0)),
                ('availability', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=core.models._Guide.default_availability, size=28)),
                ('reviewCount', models.IntegerField(default=0)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guide_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(choices=[('broadcast', 'Broadcast Message'), ('direct', 'Direct Message')], default='direct', max_length=20)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.chat')),
                ('is_seen', models.ManyToManyField(blank=True, related_name='seen_messages', to=settings.AUTH_USER_MODEL)),
                ('receivers', models.ManyToManyField(blank=True, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('slot', models.CharField(choices=[('09.00 AM', '0'), ('11.00 AM', '1'), ('13.30 PM', '2'), ('16.00 PM', '3')], max_length=10)),
                ('status', models.CharField(choices=[('UNASSIGNED', 'Unassigned'), ('ASSIGNED', 'Assigned'), ('COMPLETED', 'Completed')], default='UNASSIGNED', max_length=10)),
                ('guides', models.ManyToManyField(blank=True, related_name='tours', to='core.guide')),
                ('review', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='core.review')),
            ],
        ),
        migrations.CreateModel(
            name='TourReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.TextField()),
                ('finishedAtHour', models.IntegerField()),
                ('finishedAtMinute', models.IntegerField()),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='core.guide')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='core.tour')),
            ],
        ),
        migrations.CreateModel(
            name='TourRequestBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', '0'), ('approved', '1'), ('rejected', '2'), ('scheduled', '3')], default='pending', max_length=10)),
                ('additional_notes', models.TextField(blank=True, null=True)),
                ('number_of_visitors', models.IntegerField(default=1)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('tour', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tour_request_batch', to='core.tour')),
            ],
        ),
        migrations.CreateModel(
            name='TourRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(default=None)),
                ('time_slot', models.CharField(choices=[('09.00 AM', '0'), ('11.00 AM', '1'), ('13.30 PM', '2'), ('16.00 PM', '3')], max_length=11)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_requests', to='core.tourrequestbatch')),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('individual', 'Individual'), ('high-school', 'High School')], max_length=20)),
                ('highSchoolName', models.TextField(blank=True, null=True)),
                ('contactNumber', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visitor_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tourrequestbatch',
            name='visitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_request_batch', to='core.visitor'),
        ),
        migrations.AddField(
            model_name='tour',
            name='visitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='core.visitor'),
        ),
        migrations.CreateModel(
            name='Fair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explanation', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending', max_length=50)),
                ('date', models.DateField(default=None)),
                ('visitor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fair', to='core.visitor')),
            ],
        ),
    ]
