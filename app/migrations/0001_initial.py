# Generated by Django 5.1.5 on 2025-05-09 14:47

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nom', models.CharField(max_length=255, verbose_name='full name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('tel', models.CharField(max_length=20, verbose_name='phone number')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField(default=1)),
                ('date_commande', models.DateTimeField(auto_now_add=True)),
                ('date_livraison', models.DateField(blank=True, null=True)),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('statut', models.CharField(choices=[('pending', 'En attente'), ('confirmed', 'Confirmée'), ('canceled', 'Annulée'), ('delivered', 'Livrée')], default='pending', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'proxy': False,
            },
            bases=('app.utilisateur',),
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('app.utilisateur',),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('lue', models.BooleanField(default=False)),
                ('commande', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.commande')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('disponible', models.BooleanField(default=True)),
                ('quantite_stock', models.PositiveIntegerField(default=0)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produits', to='app.categorie')),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produits', to='app.fournisseur')),
            ],
        ),
        migrations.AddField(
            model_name='commande',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandes', to='app.produit'),
        ),
        migrations.AddField(
            model_name='commande',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandes', to='app.client'),
        ),
    ]
