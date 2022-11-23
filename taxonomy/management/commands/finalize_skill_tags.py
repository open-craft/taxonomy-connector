# -*- coding: utf-8 -*-
"""
Management command for finalizing the skill tags based on number of votes.
"""

import logging

from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from taxonomy.constants import MIN_VOTES_FOR_SKILLS, RATIO_THRESHOLD_FOR_SKILLS
from taxonomy.models import XBlockSkillData

LOGGER = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Command to check if skill tags are verified based on votes.

    Example usage:
        $ ./manage.py finalize_skill_tags
    """
    help = 'Checks the votes on tags to verify it'

    def handle(self, *args, **options):
        """
        Entry point for management command execution.
        """
        LOGGER.info('Starting skills verification task')
        unverified_skills = XBlockSkillData.objects.filter(verified=False)
        for xblock_skill in unverified_skills:
            has_valid_votes = bool(xblock_skill.relevant_count > MIN_VOTES_FOR_SKILLS)
            total_count = int(xblock_skill.relavant_count + xblock_skill.irrelevant_count)
            count_ratio = float(xblock_skill.relevant_count / total_count)
            crosses_ratio_threshold = bool(count_ratio > RATIO_THRESHOLD_FOR_SKILLS)
            if has_valid_votes and crosses_ratio_threshold:
                xblock_skill.verified = True
                xblock_skill.save()
                LOGGER.info('[%s] skill has been verified', xblock_skill.skill.name)
        LOGGER.info('Skills verification task is completed')
