# -*- coding: utf-8 -*-
"""
Tests for the taxonomy models.
"""

from pytest import mark

from django.db import IntegrityError, transaction
from django.test import TestCase

from taxonomy.models import Industry, Job, JobPostings, JobSkills
from test_utils import factories


@mark.django_db
class TestJobPostings(TestCase):
    """
    Tests for the ``JobPostings`` model.
    """

    def setUp(self):
        super(TestJobPostings, self).setUp()
        self.job_title = 'Software Engineer'
        self.job = Job.objects.create(name=self.job_title)
        self.median_salary = 6500000
        self.median_posting_duration = 28
        self.unique_postings = 1345
        self.unique_companies = 148
        self.job_posting = JobPostings.objects.create(
            job=self.job,
            median_salary=self.median_salary,
            median_posting_duration=self.median_posting_duration,
            unique_postings=self.unique_postings,
            unique_companies=self.unique_companies
        )

    def test_string_representation(self):
        """
        Test the string representation of the JobPostings model.
        """
        expected_str = '<Job postings for job: {}, have a median_salary: ${}, median_posting_duration: {}, ' \
                       'unique_postings: {}, unique hiring companies: {} >'.format(
                           self.job_title, self.median_salary, self.median_posting_duration, self.unique_postings,
                           self.unique_companies)

        expected_repr = '<JobPosting id="{0}" job="{1!r}" median_salary="${2!r}" median_posting_duration="{3!r}" ' \
                        'unique_postings="{4!r} unique_companies={5!r}">'.format(
                            self.job_posting.id, self.job, self.median_salary, self.median_posting_duration,
                            self.unique_postings, self.unique_companies)

        assert expected_str == self.job_posting.__str__()
        assert expected_repr == self.job_posting.__repr__()


@mark.django_db
class TestSkill(TestCase):
    """
    Tests for the ``Skill`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the Skill model.
        """
        skill = factories.SkillFactory()
        expected_str = '<Skill name="{}" external_id="{}">'.format(skill.name, skill.external_id)
        expected_repr = '<Skill id="{}" name="{}">'.format(skill.id, skill.name)

        assert expected_str == skill.__str__()
        assert expected_repr == skill.__repr__()


@mark.django_db
class TestCourseSkills(TestCase):
    """
    Tests for the ``CourseSkills`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the CourseSkill model.
        """
        course_skill = factories.CourseSkillsFactory()
        expected_str = '<CourseSkills name="{}" course_key="{}">'.format(
            course_skill.skill.name, course_skill.course_key
        )
        expected_repr = '<CourseSkills id="{0}" skill="{1!r}">'.format(course_skill.id, course_skill.skill)

        assert expected_str == course_skill.__str__()
        assert expected_repr == course_skill.__repr__()


@mark.django_db
class TestXBlockSkills(TestCase):
    """
    Tests for the ``XBlockSkills`` model.
    """

    def test_xblock_skill_string_representation(self):
        """
        Test the string representation of the XBlockSkills model.
        """
        xblock_skill_through = factories.XBlockSkillThroughFactory()
        xblock_skills = xblock_skill_through.xblock
        expected_str = '<XBlockSkills usage_key="{}">'.format(
            xblock_skills.usage_key
        )
        expected_repr = '<XBlockSkills id="{0}">'.format(xblock_skills.id)

        assert expected_str == xblock_skills.__str__()
        assert expected_repr == xblock_skills.__repr__()

    def test_xblock_skill_through_string_representation(self):
        """
        Test the string representation of the XBlockSkillThrough model.
        """
        xblock_skill_through = factories.XBlockSkillThroughFactory()
        expected_str = '<XBlockSkillThrough usage_key="{}" skill="{}" verified="{}">'.format(
            xblock_skill_through.xblock.usage_key,
            xblock_skill_through.skill.name,
            xblock_skill_through.verified,
        )
        expected_repr = '<XBlockSkillThrough id="{0}">'.format(xblock_skill_through.id)

        assert expected_str == xblock_skill_through.__str__()
        assert expected_repr == xblock_skill_through.__repr__()


@mark.django_db
class TestJobSkills(TestCase):
    """
    Tests for the ``JobSkills`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the JobSkills model.
        """
        job_skill = factories.JobSkillFactory()
        expected_str = '<JobSkills skill="{}" significance="{}" unique_postings="{}">'.format(
            job_skill.skill.name, job_skill.significance, job_skill.unique_postings
        )
        expected_repr = '<JobSkills id="{0}" skill="{1}" job="{2!r}" industry="{3!r}">'.format(
            job_skill.id, job_skill.skill.name, job_skill.job, job_skill.industry
        )

        assert expected_str == job_skill.__str__()
        assert expected_repr == job_skill.__repr__()

    def test_unique_together_constraint(self):
        """
        Test unique together constraint of the JobSkills model.
        """
        skill = factories.SkillFactory()
        job = factories.JobFactory()
        industry = factories.IndustryFactory()

        # We should be able to create JobSkill object
        JobSkills.objects.create(skill=skill, job=job, industry=industry, significance='1.0', unique_postings='1')
        assert JobSkills.objects.filter(skill=skill, job=job, industry=industry).count() == 1

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                JobSkills.objects.create(
                    skill=skill, job=job, industry=industry, significance='1.0', unique_postings='1'
                )

        # we should be able to create record without industry
        JobSkills.objects.create(skill=skill, job=job, significance='2.0', unique_postings='2')
        assert JobSkills.objects.filter(skill=skill, job=job, industry=None).count() == 1

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                JobSkills.objects.create(
                    skill=skill, job=job, industry=industry, significance='1.0', unique_postings='1'
                )


@mark.django_db
class TestProgramSkill(TestCase):
    """
    Tests for the ``ProgramSkill`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the ProgramSkill model.
        """
        program_skill = factories.ProgramSkillFactory()
        expected_str = '<ProgramSkill name="{}" program_uuid="{}">'.format(
            program_skill.skill.name, program_skill.program_uuid
        )
        expected_repr = '<ProgramSkill id="{0}" skill="{1!r}">'.format(program_skill.id, program_skill.skill)

        assert expected_str == str(program_skill)
        assert expected_repr == repr(program_skill)


@mark.django_db
class TestTranslation(TestCase):
    """
    Tests for the ``Translation`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the Translation model.
        """
        translation = factories.TranslationFactory()
        expected_str = '<Translation for source_record_identifier={} source_language={} translated_text_language={}>'.\
            format(
                translation.source_record_identifier,
                translation.source_language,
                translation.translated_text_language
            )
        expected_repr = '<Translation source_model_name="{}" source_model_field="{}" source_record_identifier="{}" ' \
            'source_text="{}" source_language="{}" translated_text="{}" translated_text_language="{}">'.format(
                translation.source_model_name, translation.source_model_field, translation.source_record_identifier,
                translation.source_text, translation.source_language, translation.translated_text,
                translation.translated_text_language)

        assert expected_str == translation.__str__()
        assert expected_repr == translation.__repr__()


@mark.django_db
class TestSkillCategory(TestCase):
    """
    Tests for the ``SkillCategory`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the SkillCategory model.
        """
        skill_category = factories.SkillCategoryFactory()
        expected_str = '<SkillCategory id="{}" name="{}">'.format(skill_category.id, skill_category.name)
        expected_repr = expected_str

        assert expected_str == skill_category.__str__()
        assert expected_repr == skill_category.__repr__()


@mark.django_db
class TestRefreshProgramSkillConfig(TestCase):
    """
    Tests for the ``RefreshProgramSkillConfig`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the RefreshProgramSkillConfig model.
        """
        program_skill_config = factories.RefreshProgramSkillsConfigFactory()
        expected_str = '<RefreshProgramSkillsConfig arguments="{}">'.format(program_skill_config.arguments)
        expected_repr = '<RefreshProgramSkillsConfig id="{}">'.format(program_skill_config.id)

        assert expected_str == program_skill_config.__str__()
        assert expected_repr == program_skill_config.__repr__()


@mark.django_db
class TestRefreshCourseSkillConfig(TestCase):
    """
    Tests for the ``RefreshCourseSkillConfig`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the RefreshCourseSkillConfig model.
        """
        course_skill_config = factories.RefreshCourseSkillsConfigFactory()
        expected_str = '<RefreshCourseSkillsConfig arguments="{}">'.format(course_skill_config.arguments)
        expected_repr = '<RefreshCourseSkillsConfig id="{}">'.format(course_skill_config.id)

        assert expected_str == course_skill_config.__str__()
        assert expected_repr == course_skill_config.__repr__()


@mark.django_db
class TestJob(TestCase):
    """
    Tests for the ``Job`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the Job model.
        """
        job = factories.JobFactory()
        expected_str = '<Job title={}>'.format(job.name)
        expected_repr = '<Job id="{}" name="{}" external_id="{}" >'.format(job.id, job.name, job.external_id)

        assert expected_str == job.__str__()
        assert expected_repr == job.__repr__()


@mark.django_db
class TestSkillSubCategoryFactory(TestCase):
    """
    Tests for the ``SkillSubCategory`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the Job model.
        """
        skill_sub_category = factories.SkillSubCategoryFactory()
        expected_str = '<SkillSubCategory id="{}" name="{}" category="{}">'.format(
            skill_sub_category.id, skill_sub_category.name, skill_sub_category.category.name
        )
        expected_repr = '<SkillSubCategory id="{}" name="{}">'.format(skill_sub_category.id, skill_sub_category.name)

        assert expected_str == skill_sub_category.__str__()
        assert expected_repr == skill_sub_category.__repr__()


@mark.django_db
class TestSkillsQuiz(TestCase):
    """
    Tests for the ``SkillsQuiz`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the SkillsQuiz model.
        """
        skill_quiz = factories.SkillsQuizFactory()
        expected_str = '<SkillsQuiz id="{}" user="{}">'.format(
            skill_quiz.id, skill_quiz.username
        )
        expected_repr = '<SkillsQuiz id="{}" user="{}">'.format(skill_quiz.id, skill_quiz.username)

        assert expected_str == skill_quiz.__str__()
        assert expected_repr == skill_quiz.__repr__()


@mark.django_db
class TestIndustry(TestCase):
    """
    Tests for the ``Industry`` model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the SkillsQuiz model.
        """
        # We do need to create industry as it is pre-populated by the data migration.
        industry = Industry.objects.first()
        expected_str = '<Industry id="{}" name="{}">'.format(industry.id, industry.name)
        expected_repr = '<Industry id="{}" code="{}">'.format(industry.id, industry.code)

        assert expected_str == industry.__str__()
        assert expected_repr == industry.__repr__()
