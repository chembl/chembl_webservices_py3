__author__ = 'mnowotka'

from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from django.conf.urls import url
from tastypie.utils import trailing_slash
from chembl_webservices.core.resource import ChemblModelResource
from chembl_webservices.core.meta import ChemblResourceMeta
from chembl_webservices.core.serialization import ChEMBLApiSerializer
from chembl_webservices.core.utils import NUMBER_FILTERS, CHAR_FILTERS
from django.db.models import Prefetch

from chembl_core_model.models import Assays
from chembl_core_model.models import AssayClassification
from chembl_core_model.models import AssayParameters
from chembl_core_model.models import AssayType
from chembl_core_model.models import BioassayOntology
from chembl_core_model.models import CellDictionary
from chembl_core_model.models import ChemblIdLookup
from chembl_core_model.models import ConfidenceScoreLookup
from chembl_core_model.models import Docs
from chembl_core_model.models import RelationshipType
from chembl_core_model.models import Source
from chembl_core_model.models import TargetDictionary
from chembl_core_model.models import TissueDictionary
from chembl_core_model.models import VariantSequences


from chembl_webservices.core.fields import monkeypatch_tastypie_field
monkeypatch_tastypie_field()

# ----------------------------------------------------------------------------------------------------------------------


class VariantSequenceResource(ChemblModelResource):

    class Meta(ChemblResourceMeta):
        queryset = VariantSequences.objects.all()
        excludes = ['variant_id']
        resource_name = 'variant_sequence'

        filtering = {
            'variant_id': ALL,
            'mutation': ALL,
            'accession': ALL,
            'version': ALL,
            'isoform': ALL,
            'sequence': ALL,
            'organism': ALL,
            'tax_id': ALL,
        }

# ----------------------------------------------------------------------------------------------------------------------


class AssayClassResource(ChemblModelResource):

    class Meta(ChemblResourceMeta):
        queryset = AssayClassification.objects.all()
        resource_name = 'assay_class'
        collection_name = 'assay_classifications'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name})
        filtering = {
            'l1': CHAR_FILTERS,
            'l2': CHAR_FILTERS,
            'l3': CHAR_FILTERS,
            'class_type': CHAR_FILTERS,
            'bao_id': CHAR_FILTERS,
            'source': CHAR_FILTERS,
        }
        ordering = list(filtering.keys())

        fields = (
            'assay_class_id',
            'l1',
            'l2',
            'l3',
            'class_type',
            'bao_id',
            'source',
        )

# ----------------------------------------------------------------------------------------------------------------------


class AssayParametersResource(ChemblModelResource):
    class Meta(ChemblResourceMeta):
        queryset = AssayParameters.objects.all()
        resource_name = 'assay_parameters'
        collection_name = 'assay_parameters'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name})

        filtering = {
            'type': CHAR_FILTERS,
            'relation': CHAR_FILTERS,
            'value': NUMBER_FILTERS,
            'units': CHAR_FILTERS,
            'standard_type': CHAR_FILTERS,
            'standard_relation': CHAR_FILTERS,
            'standard_value': CHAR_FILTERS,
            'standard_units': CHAR_FILTERS,
            'standard_type_fixed': CHAR_FILTERS,
            'active': NUMBER_FILTERS,
        }
        ordering = list(filtering.keys())

        fields = (
            'type',
            'relation',
            'value',
            'units',
            'text_value',
            'standard_type',
            'standard_relation',
            'standard_value',
            'standard_units',
            'standard_text_value',
            'comments',
            'standard_type_fixed',
            'active',
        )


class AssayResource(ChemblModelResource):

    assay_chembl_id = fields.CharField('chembl_id', null=True, blank=True)
    document_chembl_id = fields.CharField('doc__chembl_id', null=True, blank=True)
    target_chembl_id = fields.CharField('target__chembl_id', null=True, blank=True)
    tissue_chembl_id = fields.CharField('tissue__chembl_id', null=True, blank=True)
    cell_chembl_id = fields.CharField('cell__chembl_id', null=True, blank=True)
    assay_type = fields.CharField('assay_type__assay_type', null=True, blank=True)
    assay_type_description = fields.CharField('assay_type__assay_desc', null=True, blank=True)
    relationship_type = fields.CharField('relationship_type__relationship_type', null=True, blank=True)
    relationship_description = fields.CharField('relationship_type__relationship_desc', null=True, blank=True)
    confidence_score = fields.IntegerField('confidence_score__confidence_score', null=True, blank=True)
    confidence_description = fields.CharField('confidence_score__description', null=True, blank=True)
    src_id = fields.IntegerField('src_id', null=True, blank=True)
    bao_format = fields.CharField('bao_format_id', null=True, blank=True)
    bao_label = fields.CharField('bao_format__label', null=True, blank=True)
    score = fields.FloatField('score', use_in='search', null=True, blank=True)
    assay_classifications = fields.ToManyField('chembl_webservices.resources.assays.AssayClassResource', 'assayclassification_set', full=True, null=True, blank=True)
    assay_parameters = fields.ToManyField('chembl_webservices.resources.assays.AssayParametersResource', 'assayparameters_set', full=True, null=True, blank=True)
    variant_sequence = fields.ForeignKey('chembl_webservices.resources.assays.VariantSequenceResource',
                                           'variant', full=True, null=True, blank=True)

    class Meta(ChemblResourceMeta):
        queryset = Assays.objects.all()
        es_join_column = 'chembl_id'
        excludes = ['assay_id']
        resource_name = 'assay'
        collection_name = 'assays'
        detail_uri_name = 'chembl_id'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name, 'assay_classifications': 'assay_class', 'assay_parameters': 'assay_parameters'})
        prefetch_related = [Prefetch('assay_type', queryset=AssayType.objects.only('assay_type', 'assay_desc')),
                            Prefetch('cell', queryset=CellDictionary.objects.only('chembl_id')),
                            Prefetch('confidence_score', queryset=ConfidenceScoreLookup.objects.only('confidence_score', 'description')),
                            Prefetch('doc', queryset=Docs.objects.only('chembl_id')),
                            Prefetch('relationship_type', queryset=RelationshipType.objects.only('relationship_type', 'relationship_desc')),
                            Prefetch('src', queryset=Source.objects.only('src_id')),
                            Prefetch('target', queryset=TargetDictionary.objects.only('chembl_id')),
                            Prefetch('tissue', queryset=TissueDictionary.objects.only('chembl_id')),
                            Prefetch('bao_format', queryset=BioassayOntology.objects.only('bao_id', 'label')),
                            Prefetch('assayclassification_set'),
                            Prefetch('assayparameters_set'),
                            Prefetch('variant'),
                            ]

        fields = (
            'assay_classifications',
            'assay_category',
            'assay_cell_type',
            'assay_chembl_id',
            'assay_organism',
            'assay_strain',
            'assay_subcellular_fraction',
            'assay_tax_id',
            'assay_test_type',
            'assay_tissue',
            'assay_type',
            'assay_type_description',
            'bao_format',
            'cell_chembl_id',
            'confidence_description',
            'confidence_score',
            'description',
            'document_chembl_id',
            'relationship_description',
            'relationship_type',
            'src_assay_id',
            'src_id',
            'target_chembl_id',
            'variant_sequence',
        )

        filtering = {
            'assay_parameters': ALL_WITH_RELATIONS,
            'assay_classifications': ALL_WITH_RELATIONS,
            'assay_category': CHAR_FILTERS,
            'assay_cell_type': CHAR_FILTERS,
            'assay_chembl_id': ALL,
            'assay_organism': CHAR_FILTERS,
            'assay_strain': CHAR_FILTERS,
            'assay_subcellular_fraction': CHAR_FILTERS,
            'assay_tax_id': NUMBER_FILTERS,
            'assay_test_type': CHAR_FILTERS,
            'assay_tissue': CHAR_FILTERS,
            'assay_type': CHAR_FILTERS,
#            'assay_type_description': ALL,
            'bao_format': ALL,
            'cell_chembl_id': CHAR_FILTERS,
#            'confidence_description': ALL,
            'confidence_score': NUMBER_FILTERS,
            'description': CHAR_FILTERS, #TODO: remove from ordering
            'document_chembl_id': ALL,
#            'relationship_description': ALL,
            'relationship_type': CHAR_FILTERS,
            'src_assay_id': NUMBER_FILTERS,
            'src_id': NUMBER_FILTERS,
            'target_chembl_id': ALL,
            'variant_sequence': ALL_WITH_RELATIONS
        }
        ordering = [field for field in list(filtering.keys()) if not ('comment' in field or 'description' in field)]

# ----------------------------------------------------------------------------------------------------------------------

    def prepend_urls(self):
        """
        Returns a URL scheme based on the default scheme to specify
        the response format as a file extension, e.g. /api/v1/users.json
        """
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
            url(r"^(?P<resource_name>%s)/search\.(?P<format>xml|json|jsonp|yaml)$" % self._meta.resource_name, self.wrap_view('get_search'), name="api_get_search"),
            url(r"^(?P<resource_name>%s)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/datatables\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_datatables'), name="api_get_datatables"),
            url(r"^(?P<resource_name>%s)/set/(?P<%s_list>\w[\w/;-]*)\.(?P<format>\w+)$" % (self._meta.resource_name,  self._meta.detail_uri_name), self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r"^(?P<resource_name>%s)/(?P<%s>\w[\w/-]*)\.(?P<format>\w+)$" % (self._meta.resource_name, self._meta.detail_uri_name), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

# ----------------------------------------------------------------------------------------------------------------------
