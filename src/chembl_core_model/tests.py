"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.db.models import F
from decimal import Decimal
import datetime

class SimpleTest(TestCase):

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_Docs_from_Chembl(self):
        from chembl_core_model.models import Docs

        docs = Docs.objects.all()
        self.assertTrue(docs.exists())
        self.assertFalse(Docs.objects.filter(doc_id__isnull=True).exists())
        self.assertFalse(Docs.objects.filter(doi__isnull=False).exclude(doi__startswith="10.").exists())

        doc = Docs.objects.get(doc_id=7050)
        self.assertEqual(doc.journal, 'J. Med. Chem.')
        self.assertEqual(doc.year, 1980) # this should be date!
        self.assertEqual(doc.volume, '23')
        self.assertEqual(doc.issue, '3')
        self.assertEqual(doc.first_page, '335')
        self.assertEqual(doc.last_page, '338')
        self.assertEqual(doc.pubmed_id, 6102608)
        self.assertEqual(doc.doc_type, 'PUBLICATION')
        docs = Docs.objects.filter(updated_by__isnull=False)
        docs = docs.filter(updated_by__contains='lcon')
        self.assertTrue(docs.exists())
        start_date = datetime.date(2008, 5, 7)
        end_date = datetime.date(2008, 5, 9)
        docs = docs.filter(updated_on__range=(start_date, end_date))
        self.assertTrue(docs.exists())
        docs = Docs.objects.filter(title__startswith='Genomics')
        self.assertTrue(docs.exists())
        lookup = doc.chembl
        self.assertEqual(lookup.chembl_id, u'CHEMBL1121415')
        self.assertEqual(lookup.entity_type, 'DOCUMENT')
        self.assertEqual(lookup.entity_id, 7050)
        self.assertEqual(lookup.status, 'ACTIVE')

        doc = Docs.objects.get(pk=57482)
        self.assertEqual(doc.assays_set.count(), 16)
        self.assertEqual(doc.compoundrecords_set.count(), 6)
        self.assertEqual(doc.moleculedictionary_set.count(), 6)
        self.assertEqual(doc.targetdictionary_set.count(), 16)

        for pages in Docs.objects.filter(first_page__gt=F('last_page')).values_list('first_page', 'last_page'):
            if int(pages[0]) > int(pages[1]):
                self.assertTrue(False)

        today = datetime.date.today()
        self.assertFalse(Docs.objects.filter(updated_on__gt=today).exists())

        currentYear = today.year
        self.assertFalse(Docs.objects.filter(year__gt=str(currentYear)).exists())
        self.assertFalse(Docs.objects.filter(year__lt="1900").exists())

        self.assertFalse(
            Docs.objects.filter(chembl__isnull=False).exclude(chembl__entity_type__exact='DOCUMENT').exists())

        self.assertTrue(Docs.objects.filter(authors__contains="Selin Somersan").exists())
        self.assertTrue(Docs.objects.filter(abstract__icontains="trypanosoma brucei").exists())

        self.assertTrue(Docs.objects.filter(journal__isnull=False).filter(journal_id__iso_abbreviation__isnull=False).exclude(journal__exact=F('journal_id__iso_abbreviation')).count() > Docs.objects.count() * 0.01)

        docTypeChoices = map(lambda x: x[0], Docs.DOC_TYPE_CHOICES)
        self.assertFalse(Docs.objects.exclude(doc_type__in=docTypeChoices).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_Docs_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_Docs_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_Activities_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_Activities_from_Chembl(self):
        from chembl_core_model.models import Activities

        self.assertTrue(Activities.objects.exists())

        self.assertFalse(Activities.objects.filter(record__isnull=True).exists())
        self.assertFalse(Activities.objects.filter(doc__isnull=True).exists())
        self.assertFalse(Activities.objects.filter(molecule__isnull=True).exists())
        self.assertFalse(Activities.objects.filter(assay__isnull=True).exists())

        self.assertFalse(Activities.objects.filter(activity_id__isnull=True).exists())
        self.assertTrue(Activities.objects.filter(original_activity_id__isnull=False).exists())

        act = Activities.objects.get(activity_id=87834)
        self.assertEqual(act.activity_type, 'IC50')
        self.assertEqual(act.standard_relation, '=')
        self.assertEqual(act.published_relation, '=')
        self.assertAlmostEqual(act.published_value, Decimal("2.0E-9"), 10)
        self.assertEqual(act.published_units, 'M')
        self.assertAlmostEqual(act.standard_value, Decimal('2.0'), 2)
        self.assertEqual(act.standard_units, 'nM')
        self.assertEqual(act.standard_type, 'IC50')
        self.assertEqual(act.activity_type, 'IC50')
        self.assertEqual(act.published_type, 'IC50')
        self.assertEqual(act.predictedbindingdomains_set.count(), 1)
        self.assertAlmostEqual(act.pchembl_value, Decimal('8.70'), 2)

        #test OneToOneFields:
        act1 = Activities.objects.get(activity_id=2473157)
        self.assertAlmostEqual(act1.ligandeff.bei, Decimal('20.73'), 2)

        assay = act.assay
        self.assertEqual(assay.assay_id, 195099)
        doc = act.doc
        self.assertEqual(doc.doc_id, 17064)
        record = act.record
        self.assertEqual(record.record_id, 283926)
        molecule = act.molecule
        self.assertEqual(molecule.molregno, 644625)

        acts = Activities.objects.filter(updated_by__endswith='SQL')
        self.assertTrue(acts.exists())
        start_date = datetime.date(2008, 5, 7)
        end_date = datetime.date(2010, 5, 9)
        acts = Activities.objects.filter(updated_on__range=(start_date, end_date))
        self.assertTrue(acts.exists())
        today = datetime.date.today()

        self.assertTrue(Activities.objects.filter(activity_comment__icontains='active').exists())

        self.assertFalse(Activities.objects.filter(updated_on__gt=today).exists())

        self.assertTrue(Activities.objects.filter(ligandeff__isnull=False).exists())

        self.assertFalse(
            Activities.objects.filter(standard_flag__isnull=False).exclude(standard_flag__in=[0, 1]).exists())
        self.assertFalse(Activities.objects.filter(manual_curation_flag__isnull=False).exclude(
            manual_curation_flag__in=[0, 1, 2]).exists())

        manual_curation_choices = map(lambda x: x[0], Activities.MANUAL_CURATION_FLAG_CHOICES)
        self.assertFalse(Activities.objects.filter(manual_curation_flag__isnull=False).exclude(
            manual_curation_flag__in=manual_curation_choices).exists())

        self.assertFalse(Activities.objects.filter(potential_duplicate__isnull=False).exclude(
            potential_duplicate__in=[0,1]).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_Activities_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_Activities_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_AssayType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_AssayType_from_Chembl(self):
        from chembl_core_model.models import AssayType

        self.assertTrue(AssayType.objects.exists())
        self.assertFalse(AssayType.objects.filter(assay_type__isnull=True).exists())

        admet = AssayType.objects.get(assay_type__exact='A')
        self.assertEqual(admet.assay_desc, 'ADMET')
        self.assertTrue(admet.assays_set.count() > 0)
        assay = admet.assays_set.filter(assay_organism__isnull=False)[0]
        self.assertEquals(assay.assay_organism, "Rattus norvegicus")

        func = AssayType.objects.get(assay_type__exact='F')
        self.assertEqual(func.assay_desc, 'Functional')

        bind = AssayType.objects.get(assay_type__exact='B')
        self.assertEqual(bind.assay_desc, 'Binding')

        unas = AssayType.objects.get(assay_type__exact='U')
        self.assertEqual(unas.assay_desc, 'Unassigned')

        prop = AssayType.objects.get(assay_type__exact='P')
        self.assertEqual(prop.assay_desc, 'Property')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_AssayType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_AssayType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ChemblIdLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ChemblIdLookup_from_Chembl(self):
        from chembl_core_model.models import ChemblIdLookup

        self.assertTrue(ChemblIdLookup.objects.exists())
        self.assertFalse(ChemblIdLookup.objects.filter(chembl_id__isnull=True).exists())

        # sanity check if entity types are mutually exclusive
        self.assertFalse(ChemblIdLookup.objects.filter(moleculedictionary__isnull=False).exclude(
            entity_type__exact='COMPOUND').exists())
        self.assertFalse(
            ChemblIdLookup.objects.filter(targetdictionary__isnull=False).exclude(entity_type__exact='TARGET').exists())
        self.assertFalse(
            ChemblIdLookup.objects.filter(assays__isnull=False).exclude(entity_type__exact='ASSAY').exists())
        self.assertFalse(
            ChemblIdLookup.objects.filter(docs__isnull=False).exclude(entity_type__exact='DOCUMENT').exists())

        # COMPOUND
        cil = ChemblIdLookup.objects.get(chembl_id='CHEMBL100953')
        self.assertEqual(cil.entity_id, 164125)
        self.assertEquals(cil.moleculedictionary_set.count(), 1)
        self.assertEqual(cil.entity_type, 'COMPOUND')
        molecule = cil.moleculedictionary_set.all()[0]
        self.assertEquals(molecule.structure_type, 'MOL')

        #ASSAY
        cil = ChemblIdLookup.objects.filter(entity_type__exact='ASSAY')[0]
        self.assertEquals(cil.assays_set.count(), 1)
        assay = cil.assays_set.all()[0]
        self.assertEquals(assay.assay_organism, 'Rattus norvegicus')

        #TARGET
        cil = ChemblIdLookup.objects.filter(entity_type__exact='TARGET')[0]
        self.assertEquals(cil.targetdictionary_set.count(), 1)
        target = cil.targetdictionary_set.all()[0]
        self.assertEquals(target.organism, 'Mus musculus')

        #DOCUMENT
        cil = ChemblIdLookup.objects.filter(entity_type__exact='DOCUMENT')[0]
        self.assertEquals(cil.docs_set.count(), 1)
        doc = cil.docs_set.all()[0]
        self.assertEquals(doc.last_page, '328')

        entityTypeChoices = map(lambda x: x[0], ChemblIdLookup.ENTITY_TYPE_CHOICES)
        self.assertFalse(ChemblIdLookup.objects.filter(entity_type__isnull=False).exclude(
            entity_type__in=entityTypeChoices).exists())

        statusChoices = map(lambda x: x[0], ChemblIdLookup.STATUS_CHOICES)
        self.assertFalse(ChemblIdLookup.objects.filter(status__isnull=False).exclude(status__in=statusChoices).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ChemblIdLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ChemblIdLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_Source_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_Source_from_Chembl(self):
        from chembl_core_model.models import Source

        self.assertTrue(Source.objects.exists())
        self.assertFalse(Source.objects.filter(src_id__isnull=True).exists())

        orangeBook = Source.objects.get(src_description__icontains='orange')

        # No assays in orange book
        self.assertEquals(orangeBook.assays_set.count(), 0)

        # Many compounds in orange book
        self.assertTrue(orangeBook.compoundrecords_set.count() > 0)

        literature = Source.objects.get(src_short_name__iexact="literature")

        # Both assays and compounds in literature
        self.assertTrue(literature.assays_set.count() > 0)
        self.assertTrue(literature.compoundrecords_set.count() > 0)

        self.assertEqual(orangeBook.src_description, 'Orange Book')
        self.assertEqual(orangeBook.src_short_name, 'ORANGE_BOOK')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_Source_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_Source_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_Assays_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_Assays_from_Chembl(self):
        from chembl_core_model.models import Assays

        self.assertTrue(Assays.objects.exists())
        self.assertFalse(Assays.objects.filter(assay_id__isnull=True).exists())

        assay = Assays.objects.get(assay_id=336)
        self.assertEqual(assay.assay_source, "ORIGINAL")
        self.assertEqual(assay.target.pref_name, 'Thyroid hormone receptor beta-1')
        self.assertEqual(assay.relationship_type.relationship_desc, 'Homologous protein target assigned')
        self.assertEqual(assay.compoundrecords_set.count(), 1)

        self.assertTrue(assay.activities_set.count() > 0)

        act = assay.activities_set.all()[0]
        self.assertEquals(act.activity_type, 'Relative IC50')

        #test Many 2 Many relationship:

        self.assertTrue(Assays.objects.filter(assay_type__assay_type='F').exists())
        self.assertTrue(Assays.objects.filter(doc__doc_id=9964).exists())
        self.assertTrue(Assays.objects.filter(src__src_id=1).exists())
        self.assertFalse(
            Assays.objects.filter(chembl__isnull=False).exclude(chembl__entity_type__exact='ASSAY').exists())

        assays = Assays.objects.filter(updated_by__startswith='SQL')
        self.assertTrue(assays.exists())
        assays = Assays.objects.filter(a2t_updated_by__startswith='SQL')
        self.assertTrue(assays.exists())
        start_date = datetime.date(2008, 5, 7)
        end_date = datetime.date(2010, 5, 9)
        assays = Assays.objects.filter(updated_on__range=(start_date, end_date))
        self.assertTrue(assays.exists())
        today = datetime.date.today()
        self.assertFalse(Assays.objects.filter(updated_on__gt=today).exists())
        self.assertFalse(Assays.objects.filter(a2t_updated_on__gt=today).exists())
        assays = Assays.objects.filter(curated_by__curated_by__startswith='Expert')
        self.assertTrue(assays.exists())

        self.assertFalse(Assays.objects.filter(confidence_score__isnull=False).exclude(confidence_score__confidence_score__range=(0, 9)).exists())
        self.assertFalse(Assays.objects.filter(assay_test_type__isnull=False).exclude(
            assay_test_type__in=['In vitro', 'In vivo', 'Ex vivo']).exists())
        self.assertTrue(Assays.objects.filter(src_assay_id__isnull=False).exists())
        self.assertTrue(Assays.objects.filter(assay_tax_id__isnull=False).exists())
        self.assertTrue(Assays.objects.filter(description__icontains='affinity').exists())
        self.assertTrue(Assays.objects.filter(assay_organism__exact='Homo sapiens').exists())
        self.assertTrue(Assays.objects.filter(assay_subcellular_fraction__iexact='Membranes').exists())
        self.assertTrue(Assays.objects.filter(assay_strain__startswith='SBRI').exists())
        self.assertTrue(Assays.objects.filter(assay_cell_type__startswith='CHO').exists())
        self.assertTrue(Assays.objects.filter(assay_tissue__endswith='Brain').exists())
        self.assertTrue(Assays.objects.filter(orig_description__icontains='affinity').exists())
        self.assertFalse(Assays.objects.filter(activity_count__isnull=False).exclude(activity_count__gte=0).exists())

        self.assertFalse(
            Assays.objects.filter(a2t_complex__isnull=False).exclude(a2t_complex__in=[0, 1]).exists())
        self.assertFalse(
            Assays.objects.filter(a2t_multi__isnull=False).exclude(a2t_multi__in=[0, 1]).exists())
        self.assertFalse(
            Assays.objects.filter(mc_tax_id__isnull=False).exclude(mc_tax_id__gte=0).exists())
        self.assertFalse(
            Assays.objects.filter(a2t_assay_tax_id__isnull=False).exclude(a2t_assay_tax_id__gte=0).exists())
        self.assertTrue(Assays.objects.filter(mc_organism__exact="Homo sapiens").exists())
        self.assertTrue(Assays.objects.filter(mc_target_type__startswith="Protein").exists())
        self.assertTrue(Assays.objects.filter(mc_target_name__contains="Chlorella").exists())
        self.assertTrue(Assays.objects.filter(mc_target_accession__endswith="505").exists())
        self.assertTrue(Assays.objects.filter(a2t_assay_organism__icontains="lupus").exists())

        assayCategoryChoices = map(lambda x: x[0], Assays.ASSAY_CATEGORY_CHOICES)
        self.assertFalse(Assays.objects.filter(assay_category__isnull=False).exclude(
            assay_category__in=assayCategoryChoices).exists())

        assayTestTypeChoices = map(lambda x: x[0], Assays.ASSAY_TEST_TYPE_CHOICES)
        self.assertFalse(Assays.objects.filter(assay_test_type__isnull=False).exclude(
            assay_test_type__in=assayTestTypeChoices).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_Assays_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_Assays_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_MoleculeDictionary_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_MoleculeDictionary_from_Chembl(self):
        from chembl_core_model.models import MoleculeDictionary

        self.assertTrue(MoleculeDictionary.objects.exists())
        self.assertFalse(MoleculeDictionary.objects.filter(molregno__isnull=True).exists())

        molecule = MoleculeDictionary.objects.get(molregno=97)
        self.assertEqual(molecule.pref_name, 'PRAZOSIN')
        self.assertEqual(molecule.molecule_type, 'Small molecule')
        self.assertEqual(molecule.structure_key, 'IENZQIKPVFGBNW-UHFFFAOYSA-N')
        self.assertEqual(molecule.chebi_id, 100097)
        self.assertEqual(molecule.chebi_par_id, 8364)

        self.assertTrue(molecule.activities_set.count() > 0)
        self.assertEqual(molecule.docs.count(), 149)

        # test OneToOneFields:
        self.assertEquals(molecule.compoundproperties.molecular_species, 'NEUTRAL')
        self.assertEquals(molecule.moleculehierarchy.parent_molecule, molecule)
        self.assertEquals(molecule.compoundstructures.standard_inchi_key, 'IENZQIKPVFGBNW-UHFFFAOYSA-N')
        molecule1 = MoleculeDictionary.objects.get(molregno=675503)
        self.assertEquals(molecule1.biotherapeutics.description, 'Purified porcine insulin isophane suspension')
        self.assertEquals(molecule.compoundimages.molecule_id, 97)
        self.assertEquals(molecule.compoundmols.molecule_id, 97)

        self.assertEquals(molecule1.drugmechanism_set.all().count(), 1)

        act = molecule.activities_set.all()[0]
        self.assertEquals(act.activity_type, 'Ki')

        self.assertTrue(molecule.compoundrecords_set.count() > 0)

        rec = molecule.compoundrecords_set.all()[0]
        self.assertEqual(rec.compound_name,
            '[4-(4-Amino-6,7-dimethoxy-quinazolin-2-yl)-piperazin-1-yl]-furan-2-yl-methanone')

        self.assertTrue(molecule.moleculesynonyms_set.count() > 0)

        synonyms = molecule.moleculesynonyms_set.all()[0]
        self.assertEquals(synonyms.synonyms, 'CP-12299')

        self.assertTrue(molecule.atcclassification_set.count() > 0)

        atc = molecule.atcclassification_set.all()[0]
        self.assertEqual(atc.level4_description, 'Alpha-adrenoreceptor antagonists')

        molecule = MoleculeDictionary.objects.get(molregno=674977)
        self.assertTrue(molecule.formulations_set.count() > 0)
        form = molecule.formulations_set.all()[0]
        self.assertEquals(form.ingredient, 'ALBUTEROL SULFATE')
        self.assertEquals(molecule.usan_stem_definition, 'bronchodilators (phenethylamine derivatives)')
        self.assertEquals(molecule.indication_class, 'Bronchodilator')

        molecule = MoleculeDictionary.objects.get(molregno=545075)
        self.assertEquals(molecule.products.count(), 29)

        molecule = MoleculeDictionary.objects.filter(replacement_mrn__isnull=False)[0]
        self.assertEqual(molecule.replacement_mrn, 543200)

        molecule = MoleculeDictionary.objects.get(molregno=1540533)
        self.assertEqual(molecule.usan_substem, '-; -grastim')

        self.assertFalse(MoleculeDictionary.objects.filter(insert_date__gt=F('molfile_update')).exists())
        today = datetime.date.today()
        self.assertFalse(MoleculeDictionary.objects.filter(insert_date__gt=today).exists())
        self.assertFalse(MoleculeDictionary.objects.filter(molfile_update__gt=today).exists())

        currentYear = today.year
        self.assertFalse(
            MoleculeDictionary.objects.filter(first_approval__gt=str(currentYear)).exists()) # this should be date!
        self.assertFalse(MoleculeDictionary.objects.filter(first_approval__lt="1900").exists())

        self.assertTrue(MoleculeDictionary.objects.filter(downgrade_reason__icontains='structure').exists())
        self.assertTrue(MoleculeDictionary.objects.filter(nomerge_reason__exact='PDBE').exists())
        self.assertTrue(MoleculeDictionary.objects.filter(molecule_type__endswith='molecule').exists())

        self.assertFalse(MoleculeDictionary.objects.filter(chembl__isnull=False).exclude(
            chembl__entity_type__exact='COMPOUND').exists())

        self.assertFalse(MoleculeDictionary.objects.filter(polymer_flag__isnull=False).exclude(polymer_flag__in=[0, 1]).exists())
        self.assertFalse(
            MoleculeDictionary.objects.filter(max_phase__isnull=False).exclude(max_phase__range=(0, 4)).exists())
        self.assertFalse(MoleculeDictionary.objects.exclude(
            therapeutic_flag__in=[0, 1]).exists())
        self.assertFalse(MoleculeDictionary.objects.exclude(
            dosed_ingredient__in=[0, 1]).exists())
        self.assertFalse(MoleculeDictionary.objects.exclude(nomerge__in=[0, 1]).exists())
        self.assertFalse(MoleculeDictionary.objects.exclude(oral__in=[0, 1]).exists())
        self.assertFalse(
            MoleculeDictionary.objects.exclude(parenteral__in=[0, 1]).exists())
        self.assertFalse(MoleculeDictionary.objects.exclude(topical__in=[0, 1]).exists())
        self.assertFalse(MoleculeDictionary.objects.exclude(
            black_box_warning__in=[0, 1, -1]).exists())
        self.assertFalse(MoleculeDictionary.objects.exclude(
            natural_product__in=[0, 1, -1]).exists())
        self.assertFalse(
            MoleculeDictionary.objects.exclude(first_in_class__in=[0, 1, -1]).exists())
        self.assertFalse(MoleculeDictionary.objects.exclude(prodrug__in=[0, 1, -1]).exists())
        self.assertFalse(MoleculeDictionary.objects.exclude(exclude__in=[0, 1]).exists())
        self.assertFalse(
            MoleculeDictionary.objects.exclude(inorganic_flag__in=[0, 1, -1]).exists())

        self.assertFalse(MoleculeDictionary.objects.exclude(downgraded__in=[0,1]).exists())
        self.assertTrue(MoleculeDictionary.objects.filter(checked_by__icontains=".sdf").exists())
        self.assertFalse(MoleculeDictionary.objects.filter(usan_year__isnull=False).exclude(usan_year__range=(1900, currentYear)).exists())

        structureTypeChoices = map(lambda x: x[0], MoleculeDictionary.STRUCTURE_TYPE_CHOICES)
        self.assertFalse(MoleculeDictionary.objects.filter(structure_type__isnull=False).exclude(
            structure_type__in=structureTypeChoices).exists())

        chirallyPureChoices = map(lambda x: x[0], MoleculeDictionary.CHIRALITY_CHOICES)
        self.assertFalse(MoleculeDictionary.objects.exclude(
            chirality__in=chirallyPureChoices).exists())

        self.assertFalse(MoleculeDictionary.objects.filter(availability_type__isnull=False).exclude(
            availability_type__in=[-1,0,1,2]).exists())


#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_MoleculeDictionary_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_MoleculeDictionary_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ActionType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ActionType_from_Chembl(self):
        from chembl_core_model.models import ActionType

        self.assertTrue(ActionType.objects.exists())
        self.assertFalse(ActionType.objects.filter(description__isnull=True).exists())

        inhibitor = ActionType.objects.get(pk='INHIBITOR')
        self.assertEqual(inhibitor.description, 'Negatively effects (inhibits) the normal functioning of the protein e.g., prevention of enzymatic reaction or activation of downstream pathway')
        self.assertEqual(inhibitor.parent_type, 'NEGATIVE MODULATOR')

        inhibitorParent = ActionType.objects.get(pk=inhibitor.parent_type)
        self.assertEqual(inhibitorParent.description, 'Negatively effects the normal functioning of a protein e.g., receptor antagonist, inverse agonist or negative allosteric modulator')

        self.assertTrue(inhibitor.drugmechanism_set.all().count() > 900)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ActionType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ActionType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_MechanismRefs_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_MechanismRefs_from_Chembl(self):
        from chembl_core_model.models import MechanismRefs

        self.assertTrue(MechanismRefs.objects.exists())
        self.assertFalse(MechanismRefs.objects.filter(mecref_id__isnull=True).exists())
        self.assertFalse(MechanismRefs.objects.filter(mechanism__isnull=True).exists())
        self.assertFalse(MechanismRefs.objects.filter(ref_type__isnull=True).exists())

        mr = MechanismRefs.objects.get(pk=423)
        self.assertEqual(mr.ref_type, 'DailyMed')
        self.assertEqual(mr.ref_id, 'setid=7b8e5b26-b9e4-4704-921b-3c3c0d159916#nlm34090-1')
        self.assertEqual(mr.ref_url, 'http://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=7b8e5b26-b9e4-4704-921b-3c3c0d159916#nlm34090-1')
        self.assertEqual(mr.mechanism.mechanism_of_action, 'Dopamine D2 receptor antagonist')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_MechanismRefs_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_MechanismRefs_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_DrugMechanism_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_DrugMechanism_from_Chembl(self):
        from chembl_core_model.models import DrugMechanism

        self.assertTrue(DrugMechanism.objects.exists())
        self.assertFalse(DrugMechanism.objects.filter(mec_id__isnull=True).exists())
        self.assertFalse(DrugMechanism.objects.filter(record__isnull=True).exists())

        self.assertTrue(DrugMechanism.objects.filter(binding_site_comment__startswith='16s').exists())
        self.assertTrue(DrugMechanism.objects.filter(selectivity_comment__endswith='spectrum').exists())
        self.assertTrue(DrugMechanism.objects.filter(mechanism_comment__contains='then').exists())

        self.assertFalse(DrugMechanism.objects.exclude(direct_interaction=True).exists())
        self.assertFalse(DrugMechanism.objects.exclude(molecular_mechanism=True).exists())
        self.assertFalse(DrugMechanism.objects.exclude(disease_efficacy=True).exists())

        self.assertFalse(DrugMechanism.objects.exclude(curated_by__isnull=True).exists())
        self.assertFalse(DrugMechanism.objects.exclude(date_removed__isnull=True).exists())
        self.assertFalse(DrugMechanism.objects.exclude(downgraded__isnull=True).exists())
        self.assertFalse(DrugMechanism.objects.exclude(downgrade_reason__isnull=True).exists())

        dm = DrugMechanism.objects.get(pk=166)
        self.assertEqual(dm.record.compound_name, 'Antazoline Phosphate')
        self.assertEqual(dm.molecule.pref_name, 'ANTAZOLINE PHOSPHATE')
        self.assertEqual(dm.mechanism_of_action, 'Histamine H1 receptor antagonist')
        self.assertEqual(dm.target.pref_name, 'Histamine H1 receptor')
        self.assertEqual(dm.action_type.description, 'Binds to a receptor and prevents activation by an agonist through competing for the binding site')
        self.assertTrue(dm.direct_interaction)
        self.assertTrue(dm.molecular_mechanism)
        self.assertTrue(dm.disease_efficacy)

        dm = DrugMechanism.objects.get(pk=1592)
        self.assertTrue(dm.site.site_name, 'Benzodiazepine binding site')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_DrugMechanism_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_DrugMechanism_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_CompoundRecords_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_CompoundRecords_from_Chembl(self):
        from chembl_core_model.models import CompoundRecords

        self.assertTrue(CompoundRecords.objects.exists())
        self.assertFalse(CompoundRecords.objects.filter(record_id__isnull=True).exists())

        record = CompoundRecords.objects.get(record_id=5652)
        self.assertEqual(record.compound_name,
            '2-{[3-Azido-5-(5-methyl-2,4-dioxo-3,4-dihydro-2H-pyrimidin-1-yl)-tetrahydro-furan-2-ylmethoxy]-phenoxy-phosphorylamino}-propionic acid methyl ester')

        self.assertTrue(record.activities_set.count() > 0)
        act = record.activities_set.all()[0]
        self.assertEquals(act.activity_type, 'CC50')
        self.assertEqual(record.assays.count(), 3)

        record = CompoundRecords.objects.get(record_id=1343959)
        self.assertEqual(record.formulations_set.count(), 71)
        self.assertEqual(record.drugmechanism_set.all().count(), 1)

        record = CompoundRecords.objects.get(pk=1344689)
        self.assertEqual(record.products.count(), 29)

        self.assertTrue(CompoundRecords.objects.filter(molecule__molregno=1319474).exists())
        self.assertTrue(CompoundRecords.objects.filter(doc__doc_id=51887).exists())
        self.assertTrue(CompoundRecords.objects.filter(src__src_id=7).exists())

        records = CompoundRecords.objects.filter(updated_by__startswith='LJB')
        self.assertTrue(records.exists())
        start_date = datetime.date(2008, 5, 7)
        end_date = datetime.date(2010, 5, 9)
        records = CompoundRecords.objects.filter(updated_on__range=(start_date, end_date))
        self.assertTrue(records.exists())
        today = datetime.date.today()
        self.assertFalse(CompoundRecords.objects.filter(updated_on__gt=today).exists())

        self.assertFalse(CompoundRecords.objects.filter(src_compound_id_version__isnull=False).exclude(
            src_compound_id_version__range=(0, 8)).exists())
        self.assertTrue(CompoundRecords.objects.filter(src_compound_id__isnull=False).exists())
        self.assertTrue(CompoundRecords.objects.filter(compound_key__exact='atropine').exists())
        self.assertTrue(CompoundRecords.objects.filter(filename__startswith='/data/').exists())
        self.assertTrue(CompoundRecords.objects.filter(old_compound_key__startswith='compound').exists())

        self.assertFalse(CompoundRecords.objects.exclude(removed__in=[0, 1]).exists())
        self.assertFalse(CompoundRecords.objects.exclude(curated__in=[0, 1]).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_CompoundRecords_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_CompoundRecords_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_TargetType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_TargetType_from_Chembl(self):
        from chembl_core_model.models import TargetType

        self.assertTrue(TargetType.objects.exists())
        self.assertFalse(TargetType.objects.filter(target_type__isnull=True).exists())

        protein = TargetType.objects.get(target_type__iexact="tissue")
        self.assertEquals(protein.target_desc, 'Target is a healthy or diseased tissue')

        self.assertTrue(protein.targetdictionary_set.count() > 0)
        target = protein.targetdictionary_set.all()[0]
        self.assertEquals(target.target_type.target_desc, 'Target is a healthy or diseased tissue')

        self.assertFalse(TargetType.objects.filter(parent_type__isnull=False).exclude(parent_type__in=map(lambda x: x[0],TargetType.objects.values_list('target_type').distinct())).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_TargetType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_TargetType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_TargetDictionary_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_TargetDictionary_from_Chembl(self):
        from chembl_core_model.models import TargetDictionary

        self.assertTrue(TargetDictionary.objects.exists())
        self.assertFalse(TargetDictionary.objects.filter(tid__isnull=True).exists())

        td = TargetDictionary.objects.get(pk=10978)
        self.assertEqual(td.tax_id, 9606)
        self.assertEqual(td.targetcomponents_set.count(), 1)
        self.assertEqual(td.assays_set.count(), 2)
        td = TargetDictionary.objects.get(pk=104088)
        self.assertEqual(td.bindingsites_set.count(), 1)
        self.assertEqual(td.component_sequences.count(), 1)
        self.assertEqual(td.docs.count(), 4)

        td = TargetDictionary.objects.get(pk=104688)
        self.assertEqual(td.drugmechanism_set.all().count(), 45)

        targets = TargetDictionary.objects.filter(updated_by__exact='ylight')
        self.assertTrue(targets.exists())
        start_date = datetime.date(2008, 5, 7)
        end_date = datetime.date(2010, 5, 9)
        targets = TargetDictionary.objects.filter(updated_on__range=(start_date, end_date))
        self.assertTrue(targets.exists())
        today = datetime.date.today()
        self.assertFalse(TargetDictionary.objects.filter(updated_on__gt=today).exists())
        self.assertFalse(TargetDictionary.objects.filter(insert_date__gt=F('updated_on')).exists())
        self.assertFalse(TargetDictionary.objects.filter(insert_date__gt=today).exists())

        self.assertTrue(TargetDictionary.objects.filter(target_type__target_type='TISSUE').exists())
        self.assertFalse(
            TargetDictionary.objects.filter(chembl__isnull=False).exclude(chembl__entity_type__exact='TARGET').exists())
        self.assertTrue(TargetDictionary.objects.filter(target_type__target_desc__icontains='disruption').exists())
        self.assertTrue(TargetDictionary.objects.filter(pref_name__endswith='synthase').exists())
        self.assertTrue(TargetDictionary.objects.filter(organism__contains='Escherichia coli').exists())
        self.assertFalse(TargetDictionary.objects.filter(popularity__lt=0).exists())

        self.assertFalse(TargetDictionary.objects.filter(to=F('from')).exists())
        self.assertFalse(TargetDictionary.objects.filter(species_group_flag__isnull=False).exclude(species_group_flag__in=[0, 1]).exists())

        self.assertFalse(
            TargetDictionary.objects.filter(in_starlite__isnull=False).exclude(in_starlite__in=[0, 1]).exists())

        self.assertFalse(
            TargetDictionary.objects.filter(target_parent_type__isnull=False).exclude(target_parent_type__in=['PROTEIN', 'UNDEFINED', 'MOLECULAR', 'NON-MOLECULAR']).exists()) # TODO: define a constraint

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_TargetDictionary_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_TargetDictionary_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_TargetRelations_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_TargetRelations_from_Chembl(self):
        from chembl_core_model.models import TargetRelations

        self.assertTrue(TargetRelations.objects.exists())
        self.assertFalse(TargetRelations.objects.filter(targrel_id__isnull=True).exists())
        self.assertFalse(TargetRelations.objects.filter(target__isnull=True).exists())
        self.assertFalse(TargetRelations.objects.filter(relationship__isnull=True).exists())
        self.assertFalse(TargetRelations.objects.filter(related_target__isnull=True).exists())

        self.assertFalse(TargetRelations.objects.filter(target__tid=F('related_target__tid')).exists())

        self.assertTrue(TargetRelations.objects.exclude(target__organism=F('related_target__organism')).exists()) # TODO: should be assertFalse sometime in future!

        rel = TargetRelations.objects.get(pk=1936)
        self.assertEqual(rel.target.organism, 'Rattus norvegicus')
        self.assertEqual(rel.target.organism, 'Rattus norvegicus')

        relationshipChoices = map(lambda x: x[0], TargetRelations.RELATIONSHIP_CHOICES)
        self.assertFalse(TargetRelations.objects.exclude(
            relationship__in=relationshipChoices).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_TargetRelations_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_TargetRelations_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ProteinClassSynonyms_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ProteinClassSynonyms_from_Chembl(self):
        from chembl_core_model.models import ProteinClassSynonyms

        self.assertTrue(ProteinClassSynonyms.objects.exists())
        self.assertFalse(ProteinClassSynonyms.objects.filter(protclasssyn_id__isnull=True).exists())
        self.assertFalse(ProteinClassSynonyms.objects.filter(protein_class__isnull=True).exists())

        syn = ProteinClassSynonyms.objects.get(pk=40103)
        self.assertEqual(syn.protein_class_synonym, 'raf MAP Kinase Kinase Kinases')
        self.assertEqual(syn.protein_class.short_name, 'Raf')

        synonymTypeChoices = map(lambda x: x[0], ProteinClassSynonyms.SYN_TYPE_CHOICES)
        self.assertFalse(ProteinClassSynonyms.objects.exclude(
            syn_type__in=synonymTypeChoices).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ProteinClassSynonyms_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ProteinClassSynonyms_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ProteinClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ProteinClassification_from_Chembl(self):
        from chembl_core_model.models import ProteinClassification

        self.assertTrue(ProteinClassification.objects.exists())
        self.assertFalse(ProteinClassification.objects.filter(protein_class_id__isnull=True).exists())
        self.assertFalse(ProteinClassification.objects.filter(protein_class_desc__isnull=True).exists())

        pc = ProteinClassification.objects.get(pk=415)
        self.assertEqual(pc.pref_name, 'CAMK serine/threonine protein kinase NUAK subfamily')
        self.assertEqual(pc.short_name, 'Nuak')
        self.assertEqual(pc.definition, None)

        self.assertEqual(pc.proteinclasssynonyms_set.all().count(), 1)
        self.assertEqual(pc.proteinclasssynonyms_set.all()[0].syn_type, 'CONCEPT_WIKI')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ProteinClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ProteinClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_RelationshipType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_RelationshipType_from_Chembl(self):
        from chembl_core_model.models import RelationshipType

        self.assertTrue(RelationshipType.objects.exists())
        self.assertFalse(RelationshipType.objects.filter(relationship_type__isnull=True).exists())

        direct = RelationshipType.objects.get(relationship_type__exact='D')
        self.assertTrue(direct.assays_set.count() > 100)
        self.assertEquals(direct.relationship_desc, "Direct protein target assigned")


#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_RelationshipType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_RelationshipType_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ConfidenceScoreLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ConfidenceScoreLookup_from_Chembl(self):
        from chembl_core_model.models import ConfidenceScoreLookup

        self.assertTrue(ConfidenceScoreLookup.objects.exists())
        self.assertFalse(ConfidenceScoreLookup.objects.filter(confidence_score__isnull=True).exists())
        self.assertFalse(ConfidenceScoreLookup.objects.exclude(confidence_score__range=(0,9)).exists())

        multipleProteins = ConfidenceScoreLookup.objects.get(confidence_score__exact='5')
        self.assertEquals(multipleProteins.description, "Multiple direct protein targets may be assigned")
        self.assertEquals(multipleProteins.target_mapping, "Multiple proteins")
        self.assertTrue(multipleProteins.assays_set.count() > 100)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ConfidenceScoreLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ConfidenceScoreLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_CompoundProperties_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_CompoundProperties_from_Chembl(self):
        from chembl_core_model.models import CompoundProperties

        self.assertTrue(CompoundProperties.objects.exists())

        compoundProp = CompoundProperties.objects.get(molecule__molregno=89695)
        molecule = compoundProp.molecule
        self.assertEquals(molecule.structure_type, 'MOL')
        self.assertAlmostEqual(compoundProp.mw_freebase, Decimal('383.52'), 2)
        self.assertAlmostEqual(compoundProp.alogp, Decimal('5.82'), 2)
        self.assertEquals(compoundProp.hba, 3)
        self.assertEquals(compoundProp.hbd, 2)
        self.assertAlmostEqual(compoundProp.psa, Decimal('66.4'), 1)
        self.assertEquals(compoundProp.rtb, 7)
        self.assertEquals(compoundProp.num_ro5_violations, 1)
        self.assertAlmostEqual(compoundProp.acd_most_apka, Decimal('4.64'), 2)
        self.assertAlmostEqual(compoundProp.acd_most_bpka, Decimal('1.42'), 2)
        self.assertAlmostEqual(compoundProp.acd_logp, Decimal('4.76'), 2)
        self.assertAlmostEqual(compoundProp.acd_logd, Decimal('2.00'), 2)
        self.assertAlmostEqual(compoundProp.full_mwt, Decimal('383.52'), 2)
        self.assertAlmostEqual(compoundProp.mw_monoisotopic, Decimal('383.2460'), 4)
        self.assertEquals(compoundProp.aromatic_rings, 1)
        self.assertEquals(compoundProp.heavy_atoms, 28)
        self.assertAlmostEqual(compoundProp.qed_weighted, Decimal('0.46'), 2)
        self.assertEqual(compoundProp.full_molformula, 'C24 H33 N O3')

        today = datetime.date.today()
        self.assertFalse(CompoundProperties.objects.filter(updated_on__gt=today).exists())

        self.assertFalse(CompoundProperties.objects.filter(med_chem_friendly__isnull=False).exclude(
            med_chem_friendly__in=['Y', 'N']).exists())
        self.assertFalse(CompoundProperties.objects.filter(ro3_pass__isnull=False).exclude(
            ro3_pass__in=['Y', 'N']).exists())
        self.assertFalse(CompoundProperties.objects.filter(hba__isnull=False).exclude(hba__range=(0, 35)).exists())
        self.assertFalse(CompoundProperties.objects.filter(hbd__isnull=False).exclude(hbd__range=(0, 36)).exists())
        self.assertFalse(CompoundProperties.objects.filter(rtb__isnull=False).exclude(rtb__range=(0, 67)).exists())
        self.assertFalse(CompoundProperties.objects.filter(num_ro5_violations__isnull=False).exclude(
            num_ro5_violations__range=(0, 4)).exists())
        molecularSpiecesChoices = map(lambda x: x[0], CompoundProperties.MOLECULAR_SPECIES_CHOICES)
        self.assertFalse(CompoundProperties.objects.filter(molecular_species__isnull=False).exclude(
            molecular_species__in=molecularSpiecesChoices).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_CompoundProperties_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_CompoundProperties_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_Version_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_Version_from_Chembl(self):
        from chembl_core_model.models import Version

        self.assertTrue(Version.objects.exists())
        self.assertFalse(Version.objects.filter(name__isnull=True).exists())

        chembl17 = Version.objects.get(name__iexact="ChEMBL_17")
        self.assertTrue(chembl17.creation_date, datetime.date(2013, 8, 29))
        self.assertTrue(chembl17.comments, "ChEMBL Release 17")

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_Version_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_Version_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_MoleculeHierarchy_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_MoleculeHierarchy_from_Chembl(self):
        from chembl_core_model.models import MoleculeHierarchy

        self.assertTrue(MoleculeHierarchy.objects.exists())
        self.assertFalse(MoleculeHierarchy.objects.filter(molecule__isnull=True).exists())

        hier = MoleculeHierarchy.objects.exclude(molecule__exact=F("parent_molecule")).exclude(
            molecule__exact=F("active_molecule")).exclude(parent_molecule__exact=F("active_molecule"))[0]
        parent = hier.parent_molecule
        active = hier.active_molecule

        self.assertEquals(hier.molecule, hier.molecule)
        self.assertNotEquals(hier.molecule_id, parent.molregno)
        self.assertNotEquals(hier.molecule_id, active.molregno)
        self.assertNotEquals(active.molregno, parent.molregno)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_MoleculeHierarchy_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_MoleculeHierarchy_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_MoleculeSynonyms_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_MoleculeSynonyms_from_Chembl(self):
        from chembl_core_model.models import MoleculeSynonyms

        self.assertTrue(MoleculeSynonyms.objects.exists())
        self.assertFalse(MoleculeSynonyms.objects.filter(molsyn_id__isnull=True).exists())

        self.assertFalse(MoleculeSynonyms.objects.filter(molecule__isnull=True).exists())
        self.assertFalse(MoleculeSynonyms.objects.filter(synonyms__isnull=True).exists())
        self.assertFalse(MoleculeSynonyms.objects.filter(syn_type__isnull=True).exists())

        synonyms = MoleculeSynonyms.objects.select_related().filter(molecule__pref_name__exact="RISEDRONATE SODIUM")[0]
        self.assertEquals(synonyms.synonyms, "Actonel")
        self.assertEquals(synonyms.syn_type, "TRADE_NAME")

        self.assertTrue(MoleculeSynonyms.objects.filter(res_stem__research_stem__exact="BMS").exists())

        synonyms = MoleculeSynonyms.objects.get(pk=423)
        self.assertEqual(synonyms.res_stem.research_stem, 'P')
        self.assertEqual(synonyms.molecule.pref_name, 'DOXEPIN HYDROCHLORIDE')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_MoleculeSynonyms_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_MoleculeSynonyms_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_Products_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_Products_from_Chembl(self):
        from chembl_core_model.models import Products

        self.assertTrue(Products.objects.exists())
        self.assertFalse(Products.objects.filter(product_id__isnull=True).exists())

        product = Products.objects.get(pk="PRODUCT_083161_001")
        formulation = product.formulations_set.all()[0]
        self.assertEquals(formulation.ingredient, "DEXAMETHASONE SODIUM PHOSPHATE")
        self.assertEquals(product.compoundrecords_set.count(), 1)
        self.assertEquals(product.moleculedictionary_set.count(), 1)

        self.assertTrue(product.formulations_set.count() > 0)
        form = product.formulations_set.all()[0]
        self.assertEquals(form.ingredient, 'DEXAMETHASONE SODIUM PHOSPHATE')

        self.assertTrue(Products.objects.filter(dosage_form__exact="TABLET").exists())
        self.assertTrue(Products.objects.filter(route__exact="INJECTION").exists())
        self.assertTrue(Products.objects.filter(trade_name__endswith="INSULIN").exists())
        self.assertTrue(Products.objects.filter(ad_type__exact="DISCN").exists())
        self.assertTrue(Products.objects.filter(applicant_full_name__contains="NORDISK").exists())

        start_date = datetime.date(2008, 5, 7)
        end_date = datetime.date(2010, 8, 9)
        self.assertTrue(Products.objects.filter(approval_date__range=(start_date, end_date)).exists())
        self.assertTrue(Products.objects.filter(load_date__range=(start_date, end_date)).exists())
        self.assertTrue(Products.objects.filter(removed_date__range=(start_date, end_date)).exists())

        today = datetime.date.today()
        self.assertFalse(Products.objects.filter(approval_date__gt=today).exists())
        self.assertFalse(Products.objects.filter(load_date__gt=today).exists())
        self.assertFalse(Products.objects.filter(removed_date__gt=today).exists())

        self.assertFalse(Products.objects.filter(removed_date__lt=F("load_date")).exists())
        self.assertFalse(Products.objects.filter(approval_date__gt=F("removed_date")).exists())

        informationSourceChoices = map(lambda x: x[0], Products.INFORMATION_SOURCE_CHOICES)
        self.assertFalse(Products.objects.filter(information_source__isnull=False).exclude(
            information_source__in=informationSourceChoices).exists())

        productClassChoices = map(lambda x: x[0], Products.PRODUCT_CLASS_CHOICES)
        self.assertFalse(Products.objects.filter(product_class__isnull=False).exclude(
            product_class__in=productClassChoices).exists())

        ndaTypeChoices = map(lambda x: x[0], Products.NDA_TYPE_CHOICES)
        self.assertFalse(Products.objects.filter(nda_type__isnull=False).exclude(nda_type__in=ndaTypeChoices).exists())

        adTypeChoices = map(lambda x: x[0], Products.AD_TYPE_CHOICES)
        self.assertFalse(Products.objects.filter(ad_type__isnull=False).exclude(ad_type__in=adTypeChoices).exists())

        self.assertFalse(
            Products.objects.filter(tmp_ingred_count__isnull=False).exclude(tmp_ingred_count__range=(0, 13)).exists())
        self.assertFalse(Products.objects.filter(oral__isnull=False).exclude(oral__in=[0, 1]).exists())
        self.assertFalse(Products.objects.filter(topical__isnull=False).exclude(topical__in=[0, 1]).exists())
        self.assertFalse(Products.objects.filter(parenteral__isnull=False).exclude(parenteral__in=[0, 1]).exists())
        self.assertFalse(
            Products.objects.filter(black_box_warning__isnull=False).exclude(black_box_warning__in=[0, 1]).exists())
        self.assertFalse(
            Products.objects.filter(innovator_company__isnull=False).exclude(innovator_company__in=[0, 1]).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_Products_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_Products_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_Formulations_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_Formulations_from_Chembl(self):
        from chembl_core_model.models import Formulations

        self.assertTrue(Formulations.objects.exists())
        self.assertFalse(Formulations.objects.filter(formulation_id__isnull=True).exists())

        self.assertFalse(Formulations.objects.filter(product__isnull=True).exists())
        self.assertFalse(Formulations.objects.filter(ingredient__isnull=True).exists())

        self.assertTrue(Formulations.objects.filter(ingredient__icontains="sodium").exists())
        self.assertTrue(Formulations.objects.filter(strength__startswith="EQ").exists())

        form = Formulations.objects.filter(product__trade_name__exact="DEXAMETHASONE SODIUM PHOSPHATE").filter(
            product__applicant_full_name__startswith="AKORN")[0]
        self.assertEquals(form.product.dosage_form, "INJECTABLE")
        self.assertEquals(form.molecule.pref_name, "DEXAMETHASONE SODIUM PHOSPHATE")
        self.assertEquals(form.record_id, 1344178)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_Formulations_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_Formulations_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_OrganismClass_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_OrganismClass_from_Chembl(self):
        from chembl_core_model.models import OrganismClass

        self.assertTrue(OrganismClass.objects.exists())
        self.assertFalse(OrganismClass.objects.filter(oc_id__isnull=True).exists())

        oc = OrganismClass.objects.get(pk=955)
        self.assertEquals(oc.tax_id, 662)

        self.assertTrue(OrganismClass.objects.filter(l1__exact="Bacteria").exists())
        self.assertTrue(OrganismClass.objects.filter(l2__endswith="Positive").exists())
        self.assertTrue(OrganismClass.objects.filter(l3__iexact="bacillus").exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_OrganismClass_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_OrganismClass_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_AtcClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_AtcClassification_from_Chembl(self):
        from chembl_core_model.models import AtcClassification

        self.assertTrue(AtcClassification.objects.exists())
        self.assertFalse(AtcClassification.objects.filter(level5__isnull=True).exists())

        atc = AtcClassification.objects.get(pk="A04AA01")
        self.assertEqual(atc.molecules.all().count(), 1)
        molecule = atc.molecules.all()[0]
        self.assertEqual(molecule.pref_name, "ONDANSETRON")

        self.assertTrue(atc.defineddailydose_set.count() > 0)
        ddd = atc.defineddailydose_set.all()[0]
        self.assertEquals(ddd.ddd_units, 'mg')

        self.assertTrue(AtcClassification.objects.filter(who_name__contains="acid").exists())
        self.assertTrue(AtcClassification.objects.filter(level1__exact="A").exists())
        self.assertTrue(AtcClassification.objects.filter(level2__exact="A03").exists())
        self.assertTrue(AtcClassification.objects.filter(level3__exact="A03C").exists())
        self.assertTrue(AtcClassification.objects.filter(level4__startswith="A03C").exists())
        self.assertTrue(AtcClassification.objects.filter(level5__startswith="A03C").exists())
        self.assertTrue(AtcClassification.objects.filter(who_id__startswith="who").exists())
        self.assertTrue(AtcClassification.objects.filter(level1_description__startswith="ALIMENTARY").exists())
        self.assertTrue(AtcClassification.objects.filter(level2_description__endswith="DISORDERS").exists())
        self.assertTrue(AtcClassification.objects.filter(level3_description__contains="COMBINATION").exists())
        self.assertTrue(AtcClassification.objects.filter(level4_description__contains="agents").exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_AtcClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_AtcClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_MoleculeAtcClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_MoleculeAtcClassification_from_Chembl(self):
        from chembl_core_model.models import MoleculeAtcClassification

        self.assertTrue(MoleculeAtcClassification.objects.exists())
        self.assertFalse(MoleculeAtcClassification.objects.filter(mol_atc_id__isnull=True).exists())
        self.assertFalse(MoleculeAtcClassification.objects.filter(atc_classification__isnull=True).exists())
        self.assertFalse(MoleculeAtcClassification.objects.filter(molecule__isnull=True).exists())

        mac = MoleculeAtcClassification.objects.get(pk=4)
        self.assertEqual(mac.atc_classification.level5, 'A07BA51')
        self.assertEqual(mac.molecule.pref_name, 'CHARCOAL, ACTIVATED')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_MoleculeAtcClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_MoleculeAtcClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_CurationLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_CurationLookup_from_Chembl(self):
        from chembl_core_model.models import CurationLookup

        self.assertTrue(CurationLookup.objects.exists())
        self.assertFalse(CurationLookup.objects.filter(curated_by__isnull=True).exists())

        auto = CurationLookup.objects.get(pk='Autocuration')
        self.assertTrue(auto.assays_set.count() > 100000)
        intermediate = CurationLookup.objects.get(pk='Intermediate')
        self.assertTrue(intermediate.assays_set.count() > 100000)
        expert = CurationLookup.objects.get(pk='Expert')
        self.assertTrue(expert.assays_set.count() > 10000)

        self.assertEquals(auto.description, 'Curated against extractor target assignment')
        self.assertEquals(intermediate.description, 'Curated against ChEMBL target assignment from assay description')
        self.assertEquals(expert.description, 'Curated against ChEMBL target assignment from original publication')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_CurationLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_CurationLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_UsanStems_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_UsanStems_from_Chembl(self):
        from chembl_core_model.models import UsanStems

        self.assertTrue(UsanStems.objects.exists())
        self.assertFalse(UsanStems.objects.filter(stem__isnull=True).exists())
        self.assertFalse(UsanStems.objects.filter(usan_stem_id__isnull=True).exists())

        stemClassChoices = map(lambda x: x[0], UsanStems.STEM_CLASS_CHOICES)
        self.assertFalse(UsanStems.objects.filter(stem_class__isnull=False).exclude(stem_class__in=stemClassChoices).exists())

        self.assertFalse(UsanStems.objects.filter(who_extra__isnull=False).exclude(who_extra__exact='WHO').exists())
        self.assertFalse(UsanStems.objects.exclude(stem__contains='-').exists())
        self.assertTrue(UsanStems.objects.filter(annotation__endswith="derivative").exists())
        self.assertFalse(UsanStems.objects.filter(major_class__isnull=False).exclude(major_class__in=['PDE', 'protease','GPCR','ion channel','kinase','NR']).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_UsanStems_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_UsanStems_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_BindingSites_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_BindingSites_from_Chembl(self):
        from chembl_core_model.models import BindingSites

        self.assertTrue(BindingSites.objects.exists())
        self.assertFalse(BindingSites.objects.filter(site_id__isnull=True).exists())

        self.assertTrue(BindingSites.objects.filter(site_name__contains="dependent").exists())

        bd = BindingSites.objects.get(pk=9)
        self.assertEqual(bd.target.pref_name, '3-phosphoinositide dependent protein kinase-1')
        self.assertEqual(bd.sitecomponents_set.count(), 1)
        self.assertEqual(bd.domains.count(), 1)
        self.assertEqual(bd.predictedbindingdomains_set.count(), 175)

        bd = BindingSites.objects.get(pk=2616)
        self.assertEqual(bd.drugmechanism_set.all().count(),1)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_BindingSites_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_BindingSites_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_Domains_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_Domains_from_Chembl(self):
        from chembl_core_model.models import Domains

        self.assertTrue(Domains.objects.exists())
        self.assertFalse(Domains.objects.filter(domain_id__isnull=True).exists())

        domainTypeChoices = map(lambda x: x[0], Domains.DOMAIN_TYPE_CHOICES)
        self.assertFalse(Domains.objects.filter(domain_type__isnull=False).exclude(domain_type__in=domainTypeChoices).exists())
        self.assertTrue(Domains.objects.filter(domain_name__contains="hydro").exists())
        self.assertFalse(Domains.objects.exclude(source_domain_id__startswith="P").exists())
        self.assertFalse(Domains.objects.filter(domain_description__isnull=False).exists()) # hopefully to be removed...

        domain = Domains.objects.get(pk=3077)
        self.assertEqual(domain.sitecomponents_set.count(), 7)
        self.assertEqual(domain.bindingsites_set.count(), 7)
        self.assertEqual(domain.componentdomains_set.count(), 33)
        self.assertEqual(domain.component_sequences.count(), 33)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_Domains_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_Domains_from_Chembl(self):
        pass
#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ComponentDomains_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ComponentDomains_from_Chembl(self):
        from chembl_core_model.models import ComponentDomains

        self.assertTrue(ComponentDomains.objects.exists())
        self.assertFalse(ComponentDomains.objects.filter(compd_id__isnull=True).exists())

        self.assertFalse(ComponentDomains.objects.filter(start_position__isnull=False).exclude(start_position__range=(1,8000)).exists())
        self.assertFalse(ComponentDomains.objects.filter(end_position__isnull=False).exclude(end_position__range=(1,8000)).exists())
        self.assertFalse(ComponentDomains.objects.filter(start_position__gt=F('end_position')).exists())

        cd = ComponentDomains.objects.get(pk=68239)
        self.assertEqual(cd.domain.domain_name, 'CUB')
        self.assertEqual(cd.component.description, 'Suppressor of tumorigenicity 14 protein')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ComponentDomains_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ComponentDomains_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_SiteComponents_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_SiteComponents_from_Chembl(self):
        from chembl_core_model.models import SiteComponents

        self.assertTrue(SiteComponents.objects.exists())
        self.assertFalse(SiteComponents.objects.filter(sitecomp_id__isnull=True).exists())

        self.assertFalse(SiteComponents.objects.filter(site_residues__isnull=False).exists()) # hopefully to be removed...

        sd = SiteComponents.objects.get(pk=2)
        self.assertEqual(sd.site.site_name, 'Serine/threonine-protein phosphatase, Metallophos domain')
        self.assertEqual(sd.component.description, 'Serine/threonine-protein phosphatase')
        self.assertEqual(sd.domain.domain_type, 'Pfam-A')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_SiteComponents_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_SiteComponents_from_Chembl(self):
        pass


#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ResearchStem_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ResearchStem_from_Chembl(self):
        from chembl_core_model.models import ResearchStem

        self.assertTrue(ResearchStem.objects.exists())
        self.assertFalse(ResearchStem.objects.filter(res_stem_id__isnull=True).exists())
        self.assertFalse(ResearchStem.objects.filter(research_stem__isnull=True).exists())

        rs = ResearchStem.objects.get(pk=2)
        self.assertEqual(rs.researchcompanies_set.count(), 1)

        rs = ResearchStem.objects.get(pk=464)
        self.assertEqual(rs.moleculesynonyms_set.count(), 48)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ResearchStem_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ResearchStem_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ResearchCompanies_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ResearchCompanies_from_Chembl(self):
        from chembl_core_model.models import ResearchCompanies

        self.assertTrue(ResearchCompanies.objects.exists())
        self.assertFalse(ResearchCompanies.objects.filter(co_stem_id__isnull=True).exists())

        self.assertTrue(ResearchCompanies.objects.filter(company__icontains='pharma').exists())
        self.assertTrue(ResearchCompanies.objects.filter(previous_company__icontains='pharma').exists())
        self.assertTrue(ResearchCompanies.objects.filter(country__iexact='belgium').exists())

        rc = ResearchCompanies.objects.get(pk=690)
        self.assertEqual(rc.res_stem.research_stem, 'BY')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ResearchCompanies_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ResearchCompanies_from_Chembl(self):
        pass


#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_Biotherapeutics_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_Biotherapeutics_from_Chembl(self):
        from chembl_core_model.models import Biotherapeutics

        self.assertTrue(Biotherapeutics.objects.exists())
        self.assertFalse(Biotherapeutics.objects.filter(molecule__isnull=True).exists())

        self.assertTrue(Biotherapeutics.objects.filter(description__icontains='immunoglobulin').exists())

        bio = Biotherapeutics.objects.get(pk=675485)
        self.assertEqual(bio.molecule.pref_name, 'OMALIZUMAB')
        self.assertEqual(bio.biotherapeuticcomponents_set.count(), 2)
        self.assertEqual(bio.bio_component_sequences.count(), 2)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_Biotherapeutics_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_Biotherapeutics_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_BioComponentSequences_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_BioComponentSequences_from_Chembl(self):
        from chembl_core_model.models import BioComponentSequences
        import hashlib

        self.assertTrue(BioComponentSequences.objects.exists())
        self.assertFalse(BioComponentSequences.objects.filter(component_id__isnull=True).exists())

        self.assertFalse(BioComponentSequences.objects.exclude(component_type__exact="PROTEIN").exists())
        self.assertTrue(BioComponentSequences.objects.filter(description__icontains="light").exists())
        self.assertTrue(BioComponentSequences.objects.filter(organism__exact="Homo sapiens").exists())
        self.assertTrue(BioComponentSequences.objects.filter(db_source__endswith="candidates").exists())

        self.assertFalse(BioComponentSequences.objects.filter(updated_by__isnull=False).exists()) # hopefully to be removed...
        self.assertFalse(BioComponentSequences.objects.filter(updated_on__isnull=False).exists()) # hopefully to be removed...
        self.assertFalse(BioComponentSequences.objects.filter(accession__isnull=False).exists()) # hopefully to be removed...
        #self.assertFalse(BioComponentSequences.objects.filter(insert_date__isnull=False).exclude(insert_date=datetime.date(2013, 1, 17)).exists()) # hopefully to be removed...
        self.assertFalse(BioComponentSequences.objects.filter(db_version__isnull=False).exclude(db_version__exact="24_09_12").exists()) # hopefully to be removed...

        seq = BioComponentSequences.objects.get(pk=6407)
        m = hashlib.md5()
        m.update(seq.sequence)
        self.assertEqual(m.hexdigest(), seq.sequence_md5sum)
        self.assertEqual(seq.tax_id, 9606)
        self.assertEqual(seq.biotherapeuticcomponents_set.count(), 1)
        self.assertEqual(seq.biotherapeutics_set.count(), 1)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_BioComponentSequences_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_BioComponentSequences_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_BiotherapeuticComponents_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_BiotherapeuticComponents_from_Chembl(self):
        from chembl_core_model.models import BiotherapeuticComponents

        self.assertTrue(BiotherapeuticComponents.objects.exists())
        self.assertFalse(BiotherapeuticComponents.objects.filter(biocomp_id__isnull=True).exists())

        bc = BiotherapeuticComponents.objects.get(pk=496)
        self.assertEqual(bc.biotherapeutics.description, 'Oxytocin-neurophysin 1 [Precursor]')
        self.assertEqual(bc.component.component_type, 'PROTEIN')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_BiotherapeuticComponents_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_BiotherapeuticComponents_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_DataValidityLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_DataValidityLookup_from_Chembl(self):
        from chembl_core_model.models import DataValidityLookup

        self.assertTrue(DataValidityLookup.objects.exists())
        self.assertFalse(DataValidityLookup.objects.filter(data_validity_comment__isnull=True).exists())

        self.assertFalse(DataValidityLookup.objects.exclude(data_validity_comment__in=['Author confirmed error', 'Manually validated', 'Potential author error', 'Outside typical range', 'Non standard unit for type', 'Potential missing data', 'Potential transcription error']).exists())

        outsideRange = DataValidityLookup.objects.get(pk='Outside typical range')
        self.assertTrue(outsideRange.activities_set.count() < 200000)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_DataValidityLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_DataValidityLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ActivityStdsLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ActivityStdsLookup_from_Chembl(self):
        from chembl_core_model.models import ActivityStdsLookup

        self.assertTrue(ActivityStdsLookup.objects.exists())
        self.assertFalse(ActivityStdsLookup.objects.filter(std_act_id__isnull=True).exists())

        self.assertTrue(ActivityStdsLookup.objects.filter(standard_type__iexact="MIC50").exists())
        self.assertTrue(ActivityStdsLookup.objects.filter(definition__endswith="life").exists())
        self.assertTrue(ActivityStdsLookup.objects.filter(standard_units__icontains="kg").exists())

        asl = ActivityStdsLookup.objects.get(pk=6)
        self.assertEqual(asl.normal_range_max, 1000000000)
        self.assertEqual(asl.normal_range_min, 100)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ActivityStdsLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ActivityStdsLookup_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_PredictedBindingDomains_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_PredictedBindingDomains_from_Chembl(self):
        from chembl_core_model.models import PredictedBindingDomains

        self.assertTrue(PredictedBindingDomains.objects.exists())
        self.assertFalse(PredictedBindingDomains.objects.filter(predbind_id__isnull=True).exists())

        confidenceChoices = map(lambda x: x[0], PredictedBindingDomains.CONFIDENCE_CHOICES)
        self.assertFalse(PredictedBindingDomains.objects.filter(confidence__isnull=False).exclude(confidence__in=confidenceChoices).exists())

        self.assertFalse(PredictedBindingDomains.objects.filter(prediction_method__isnull=False).exclude(prediction_method__in=['Single domain','Multi domain', 'Manual']).exists())

        pbd = PredictedBindingDomains.objects.get(pk=1944)
        self.assertEqual(pbd.activity.published_type, 'Ki')
        self.assertEqual(pbd.site.site_name, 'Neurokinin 2 receptor, 7tm_1 domain')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_PredictedBindingDomains_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_PredictedBindingDomains_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_Journals_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_Journals_from_Chembl(self):
        from chembl_core_model.models import Journals

        self.assertTrue(Journals.objects.exists())
        self.assertFalse(Journals.objects.filter(journal_id__isnull=True).exists())

        journal = Journals.objects.get(pk=507)
        self.assertEqual(journal.title, 'The American journal of pathology.')
        self.assertEqual(journal.iso_abbreviation, 'Am. J. Pathol.')
        self.assertEqual(journal.issn_print, '0002-9440')
        self.assertEqual(journal.issn_electronic, '1525-2191')
        self.assertEqual(journal.publication_start_year, 1925)
        self.assertEqual(journal.nlm_id, '0370502')
        self.assertEqual(journal.doc_journal, 'Am. J. Pathol.')

        self.assertEqual(journal.docs_set.count(), 1)
        self.assertEqual(journal.journalarticles_set.count(), 1)

        self.assertFalse(
            Journals.objects.filter(core_journal_flag__isnull=False).exclude(core_journal_flag__in=[0, 1]).exists())

        today = datetime.date.today()
        currentYear = today.year
        self.assertFalse(Journals.objects.filter(publication_start_year__gt=currentYear).exists())
        self.assertFalse(Journals.objects.filter(publication_start_year__lt=1869).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_Journals_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_Journals_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_JournalArticles_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_JournalArticles_from_Chembl(self):
        from chembl_core_model.models import JournalArticles

        article = JournalArticles.objects.get(pk=314583)
        self.assertEqual(article.volume, 53)
        self.assertEqual(article.issue, 3)
        self.assertEqual(article.year, 2010)
        self.assertEqual(article.month, 2)
        self.assertEqual(article.day, 11)
        self.assertEqual(article.pagination, '1172-89')
        self.assertEqual(article.first_page, '1172')
        self.assertEqual(article.last_page, '1189')
        self.assertEqual(article.volume, 53)
        self.assertEqual(article.issue_raw, '3')
        self.assertEqual(article.year_raw, '2010')
        self.assertEqual(article.month_raw, 'Feb')
        self.assertEqual(article.day_raw, '11')

        self.assertEqual(article.journal.title, 'Journal of medicinal chemistry')

        self.assertTrue(JournalArticles.objects.exists())
        self.assertFalse(JournalArticles.objects.filter(int_pk__isnull=True).exists())

        #TODO: Uncomment this:
        #for pages in JournalArticles.objects.filter(first_page__gt=F('last_page')).values_list('first_page', 'last_page'):
        #    try:
        #        if int(pages[0]) > int(pages[1]):
        #            self.assertTrue(False, "first_page = " + str(pages[0]) + ", last_page = " + str(pages[1]))
        #    except ValueError:
        #        continue

        self.assertFalse(JournalArticles.objects.filter(doi__isnull=False).exclude(doi__startswith="10.").exists())

        today = datetime.date.today()
        self.assertFalse(JournalArticles.objects.filter(date_loaded__gt=today).exists())

        currentYear = today.year
        self.assertFalse(JournalArticles.objects.filter(year_raw__gt=str(currentYear)).exists())
        self.assertFalse(JournalArticles.objects.filter(year_raw__lt="1900").exists())

        self.assertFalse(JournalArticles.objects.filter(year__gt=currentYear).exists())
        self.assertFalse(JournalArticles.objects.filter(year__lt=1900).exists())

        self.assertTrue(JournalArticles.objects.filter(authors__contains="Augustyniak").exists())
        self.assertTrue(JournalArticles.objects.filter(abstract__icontains="trypanosoma brucei").exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_JournalArticles_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_JournalArticles_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ComponentSequences_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ComponentSequences_from_Chembl(self):
        from chembl_core_model.models import ComponentSequences
        import hashlib

        self.assertTrue(ComponentSequences.objects.exists())
        self.assertFalse(ComponentSequences.objects.filter(component_id__isnull=True).exists())

        componentTypeChoices = map(lambda x: x[0], ComponentSequences.COMPONENT_TYPE_CHOICES)
        self.assertFalse(ComponentSequences.objects.filter(component_type__isnull=False).exclude(component_type__in=componentTypeChoices).exists())

        seq = ComponentSequences.objects.get(pk=27)
        m = hashlib.md5()
        m.update(seq.sequence)
        self.assertEqual(m.hexdigest(), seq.sequence_md5sum)
        self.assertEqual(seq.tax_id, 10116)
        self.assertEqual(seq.accession, 'P18506')
        self.assertEqual(seq.targetcomponents_set.count(), 3)
        self.assertEqual(seq.targetdictionary_set.count(),3)
        self.assertEqual(seq.componentsynonyms_set.count(), 3)
        self.assertEqual(seq.componentclass_set.count(), 1)
        self.assertEqual(seq.proteinclassification_set.count(), 1)
        self.assertEqual(seq.componentdomains_set.count(), 2)
        self.assertEqual(seq.domains_set.count(), 2)

        seq = ComponentSequences.objects.get(pk=4968)
        self.assertEqual(seq.sitecomponents_set.count(), 1)

        self.assertTrue(ComponentSequences.objects.filter(description__icontains="receptor").exists())
        self.assertTrue(ComponentSequences.objects.filter(organism__exact="Homo sapiens").exists())
        self.assertTrue(ComponentSequences.objects.filter(db_source__iexact="trembl").exists())

        self.assertTrue(ComponentSequences.objects.filter(insert_date__isnull=False).exclude(insert_date__range=(datetime.date(2012, 5, 30), datetime.date(2012, 11, 2))).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ComponentSequences_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ComponentSequences_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ComponentSynonyms_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ComponentSynonyms_from_Chembl(self):
        from chembl_core_model.models import ComponentSynonyms

        self.assertTrue(ComponentSynonyms.objects.exists())
        self.assertFalse(ComponentSynonyms.objects.filter(compsyn_id__isnull=True).exists())

        synTypeChoices = map(lambda x: x[0], ComponentSynonyms.SYN_TYPE_CHOICES)
        self.assertFalse(ComponentSynonyms.objects.filter(syn_type__isnull=False).exclude(syn_type__in=synTypeChoices).exists())

        self.assertTrue(ComponentSynonyms.objects.filter(component_synonym__icontains="peptide").exists())

        cs = ComponentSynonyms.objects.get(pk=221449)
        self.assertEqual(cs.component.description, 'Leucyl-cystinyl aminopeptidase')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ComponentSynonyms_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ComponentSynonyms_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_TargetComponents_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_TargetComponents_from_Chembl(self):
        from chembl_core_model.models import TargetComponents

        self.assertTrue(TargetComponents.objects.exists())
        self.assertFalse(TargetComponents.objects.filter(targcomp_id__isnull=True).exists())

        tc = TargetComponents.objects.get(pk=410)
        self.assertEqual(tc.target.pref_name, 'Metallo-beta-lactamase')
        self.assertEqual(tc.component.description, 'Metallo-beta-lactamase')

        self.assertFalse(TargetComponents.objects.exclude(relationship__in=['SUBUNIT', 'PROTEIN SUBUNIT', 'SINGLE PROTEIN','FUSION PROTEIN','GROUP MEMBER','INTERACTING PROTEIN','COMPARATIVE PROTEIN', 'RNA SUBUNIT', 'RNA']).exists())
        self.assertFalse(TargetComponents.objects.exclude(stoichiometry__in=[0,1,2,3]).exists())
        self.assertFalse(TargetComponents.objects.exclude(
            homologue__in=[0, 1, 2]).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_TargetComponents_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_TargetComponents_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ProteinFamilyClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ProteinFamilyClassification_from_Chembl(self):
        from chembl_core_model.models import ProteinFamilyClassification

        self.assertTrue(ProteinFamilyClassification.objects.exists())
        self.assertFalse(ProteinFamilyClassification.objects.filter(protein_class_id__isnull=True).exists())

        self.assertTrue(ProteinFamilyClassification.objects.filter(protein_class_desc__icontains="smallmol").exists())
        self.assertTrue(ProteinFamilyClassification.objects.filter(l1__startswith="Membrane").exists())
        self.assertTrue(ProteinFamilyClassification.objects.filter(l2__endswith="Receptor").exists())
        self.assertTrue(ProteinFamilyClassification.objects.filter(l3__startswith="Peptide").exists())
        self.assertTrue(ProteinFamilyClassification.objects.filter(l4__contains="like").exists())
        self.assertTrue(ProteinFamilyClassification.objects.filter(l5__icontains="amine").exists())
        self.assertTrue(ProteinFamilyClassification.objects.filter(l6__startswith="K").exists())
        self.assertTrue(ProteinFamilyClassification.objects.filter(l7__icontains="alpha").exists())
        self.assertTrue(ProteinFamilyClassification.objects.filter(l8__endswith="-TYPE").exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ProteinFamilyClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ProteinFamilyClassification_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_ComponentClass_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_ComponentClass_from_Chembl(self):
        from chembl_core_model.models import ComponentClass

        self.assertTrue(ComponentClass.objects.exists())
        self.assertFalse(ComponentClass.objects.filter(comp_class_id__isnull=True).exists())

        cc = ComponentClass.objects.get(pk=1)
        self.assertEqual(cc.component.description, 'Gamma-aminobutyric acid receptor subunit pi')
        self.assertEqual(cc.protein_class.protein_class_desc, 'ion channel  lgic  cys_loop  gabaa  anionic  cl  gaba-a pi')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_ComponentClass_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_ComponentClass_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_CellDictionary_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_CellDictionary_from_Chembl(self):
        from chembl_core_model.models import CellDictionary

        self.assertTrue(CellDictionary.objects.exists())
        self.assertFalse(CellDictionary.objects.filter(cell_id__isnull=True).exists())

        self.assertTrue(CellDictionary.objects.filter(cell_name__startswith="MDA").exists())
        self.assertTrue(CellDictionary.objects.filter(cell_description__endswith="sarcoma").exists())
        self.assertTrue(CellDictionary.objects.filter(cell_source_tissue__contains="lymph").exists())
        self.assertTrue(CellDictionary.objects.filter(cell_source_organism__exact="Homo sapiens").exists())

        cd = CellDictionary.objects.get(pk=10)
        self.assertEqual(cd.cell_source_tax_id, 9606)

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_CellDictionary_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_CellDictionary_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_DefinedDailyDose_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_DefinedDailyDose_from_Chembl(self):
        from chembl_core_model.models import DefinedDailyDose

        self.assertTrue(DefinedDailyDose.objects.exists())
        self.assertFalse(DefinedDailyDose.objects.filter(ddd_id__isnull=True).exists())

        ddd = DefinedDailyDose.objects.get(pk=1795)
        self.assertEquals(ddd.atc_code.level1_description, 'MUSCULO-SKELETAL SYSTEM')
        self.assertAlmostEqual(ddd.ddd_value, Decimal('0.1'), 1)
        self.assertEquals(ddd.ddd_units, 'g')
        self.assertEquals(ddd.ddd_comment, 'refers to indometacin')

        self.assertTrue(DefinedDailyDose.objects.filter(ddd_admr__contains="O").exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_DefinedDailyDose_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_DefinedDailyDose_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_LigandEff_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_LigandEff_from_Chembl(self):
        from chembl_core_model.models import LigandEff

        self.assertTrue(LigandEff.objects.exists())
        self.assertFalse(LigandEff.objects.filter(activity_id__isnull=True).exists())

        leff = LigandEff.objects.get(pk=2473157)
        self.assertAlmostEqual(leff.bei, Decimal("20.73"), 2)
        self.assertAlmostEqual(leff.sei, Decimal("21"), 0)
        self.assertAlmostEqual(leff.le, Decimal("0.39"), 2)
        self.assertAlmostEqual(leff.lle, Decimal("4.89"), 2)

        self.assertFalse(LigandEff.objects.filter(sei__gt=350).exists())
        self.assertFalse(LigandEff.objects.filter(sei__lt=0).exists())

        self.assertFalse(LigandEff.objects.filter(bei__gt=460).exists())
        self.assertFalse(LigandEff.objects.filter(bei__lt=0).exists())

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_LigandEff_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_LigandEff_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_CompoundImages_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_CompoundImages_from_Chembl(self):
        from chembl_core_model.models import CompoundImages
        from PIL import Image
        import StringIO

        self.assertTrue(CompoundImages.objects.exists())
        self.assertFalse(CompoundImages.objects.filter(molecule__isnull=True).exists())

        compoundImage = CompoundImages.objects.defer("png", "png_500").get(pk=779371)
        self.assertEquals(compoundImage.molecule.structure_key, 'KPWGETCUPMCFCF-LJQANCHMSA-N')

        im = Image.open(StringIO.StringIO(compoundImage.png))
        im.verify()
        self.assertEquals(im.size, (128, 128))

        im = Image.open(StringIO.StringIO(compoundImage.png_500))
        im.verify()
        self.assertEquals(im.size, (500, 500))

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_CompoundImages_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_CompoundImages_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_CompoundMols_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_CompoundMols_from_Chembl(self):
        from chembl_core_model.models import CompoundMols

        self.assertTrue(CompoundMols.objects.exists())
        self.assertFalse(CompoundMols.objects.filter(molecule__isnull=True).exists())

        mol = CompoundMols.objects.defer("ctab").get(pk=1930)
        self.assertEquals(mol.molecule.structure_type, 'MOL')

#-----------------------------------------------------------------------------------------------------------------------

    def test_Update_CompoundMols_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_CompoundMols_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Create_CompoundStructures_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Retrieve_CompoundStructures_from_Chembl(self):
        """
        This test will pass for django 1.5 (and possibly earlier versions - don't know about the later since
        that's the latest in the moment of writing this test) when a patch in django core is applied
        (https://code.djangoproject.com/ticket/11580):
        in https://code.djangoproject.com/ticket/11580, change:

        def field_cast_sql(self, db_type):
        if db_type and db_type.endswith('LOB'):
            return "DBMS_LOB.SUBSTR(%s)"
        else:
            return "%s"

        to:

        def field_cast_sql(self, db_type):
            return "%s"
        """

        from chembl_core_model.models import CompoundStructures


        self.assertTrue(CompoundStructures.objects.exists())
        self.assertFalse(CompoundStructures.objects.filter(molecule__isnull=True).exists())

        struct = CompoundStructures.objects.get(pk=1146)
        struct.validate_unique()
        self.assertEquals(struct.standard_inchi_key, 'ONYNMSUZCIJSTA-UHFFFAOYSA-N')
        self.assertEquals(struct.canonical_smiles, 'CC1(C)N=C(N)N=C(N)N1c2cccc(F)c2')
        self.assertEquals(struct.molecule.structure_type, 'MOL')

        self.assertFalse(CompoundStructures.objects.filter(molfile__isnull=True).exists())
        self.assertTrue(CompoundStructures.objects.filter(standard_inchi__isnull=False).exists())

#-----------------------------------------------------------------------------------------------------------------------


    def test_Update_CompoundStructures_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------

    def test_Delete_CompoundStructures_from_Chembl(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------
