__author__ = 'mnowotka'

from django.db import models
from django.conf import settings
from django.db.models.base import ModelBase
import re
import sys
import inspect
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps
import copy

# ----------------------------------------------------------------------------------------------------------------------


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s1 = re.sub('(.)([0-9]+)', r'\1_\2', s1)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# ----------------------------------------------------------------------------------------------------------------------


class ChemblCoreAbstractModel(models.Model):
    class Meta:
        abstract = True
        app_label = 'chembl_core_model'
        managed = False

# ----------------------------------------------------------------------------------------------------------------------


class ChemblAppAbstractModel(models.Model):
    class Meta:
        abstract = True
        managed = False

# ----------------------------------------------------------------------------------------------------------------------


class ChemblAbstractModel(models.Model):
    class Meta:
        abstract = True

# ----------------------------------------------------------------------------------------------------------------------


class ChemblModelMetaClass(ModelBase):
    def __new__(cls, name, bases, attrs):
        n = name
        if "Meta" in attrs:
            meta = attrs["Meta"]
            if hasattr(meta, "db_table"):
                n = meta.db_table
        klas = super(ChemblModelMetaClass, cls).__new__(cls, name, bases, attrs)
        klas._meta.db_table = str(convert(n))
        return klas

# ----------------------------------------------------------------------------------------------------------------------


def remove_field(cls, f_name):
    if hasattr(cls, f_name):
        delattr(cls, f_name)

# ----------------------------------------------------------------------------------------------------------------------

def rebase(module, klas):
    if isinstance(klas, str):
        relClsName = klas.split('.')[-1]
    else:
        relClsName = klas.__name__

    lst = inspect.getmembers(sys.modules[module], lambda x: inspect.isclass(x) and x.__name__ == relClsName)
    if len(lst):
        return lst[0][1]

    return module.split('.')[0] + '.' + relClsName

# ----------------------------------------------------------------------------------------------------------------------


class ModifiedModelMetaclass(ChemblModelMetaClass):

    def __new__(cls, name, bases, attrs):
        try:
            metaCls = attrs['Meta']
            meta = metaCls()
        except KeyError:
            raise ImproperlyConfigured("Helper class %s hasn't a Meta subclass!" % name)

        # Find model class for this helper
        try:
            model = getattr(meta, 'model')
        except AttributeError:
            return super(ModifiedModelMetaclass, cls).__new__(cls, name, bases, attrs)

        if isinstance(model, str):
            model_class = apps.get_model(*model.split('.'))
        elif issubclass(model, models.Model):
            model_class = model
        else:
            raise ImproperlyConfigured("Model informed by Meta subclass of %s is improperly!" % name)
        remove_field(metaCls, 'model')

        module = attrs['__module__']
        excludes = getattr(meta, 'exclude', ())
        if excludes is None:
            excludes = ()
        remove_field(metaCls, 'exclude')
        attrs['Meta'] = metaCls

        fields = [f for f in list(model_class._meta.fields) + list(model_class._meta.local_many_to_many) if f.name not in excludes]
        for field in fields:
            f = copy.deepcopy(field)
            if hasattr(f, 'rel') and f.rel:
                if hasattr(f.rel, 'through'):
                    f.rel.through = rebase(module, f.rel.through)
                f.rel.model = rebase(module, f.rel.model)
            attrs[f.name] = f

        return super(ModifiedModelMetaclass, cls).__new__(cls, name, bases, attrs)

# ----------------------------------------------------------------------------------------------------------------------


