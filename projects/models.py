from django.db import models
from django.contrib.auth.models import User
from taggit_autosuggest.managers import TaggableManager


class Project(models.Model):
    """PyAr projects."""

    REPOSITORY_TYPES = (
        ('G','Github'),
        ('B','Bitbucket'),
        ('O','Other')
    )
    REPOSITORY_STATUS = (
        ('0','Inactivo'),
        ('1','Activo'),
    )
    LICENSES = (
        ("GPL2", "GPLv2"),
        ("GPL3", "GPLv3"),
        ("AGPL", "Affero GPL"),
        ("APCH", "Apache License"),
        ("MITL", "MIT License"),
        ("BSD2", "BSD (2-Clause) License"),
        ("BSD3", "BSD (3-Clause) License"),
        ("ECLP", "Eclipse License"),
        ("LGP2", "LGPL v2.1"),
        ("LGP3", "LGPL v3"),
        ("MPL2", "Mozilla License"),
        ("NOLC", "No License"),
        ("PBDM", "Public Domain"),
        ("OTHER", "Other")
    )  # ToDo: Armar un listado de licencias exhaustivo
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User)
    description = models.TextField()
    repository = models.URLField()
    repositoryType = models.CharField(max_length=1, choices=REPOSITORY_TYPES)
    license = models.CharField(max_length=4, choices=LICENSES)
    state = models.CharField(max_length=1, default="1", choices=REPOSITORY_STATUS)
    tags = models.CharField(max_length=255)
    #tags = TaggableManager()
    mail = models.EmailField()
    contribution = models.BooleanField()
    logo = models.ImageField(upload_to='static/projects/logos', null=True, blank=True)

    def __str__(self):
        return self.name
