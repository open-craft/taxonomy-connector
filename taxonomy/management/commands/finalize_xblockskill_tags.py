# -*- coding: utf-8 -*-
"""
Management command for finalizing the xblockskill tags based on number of votes.
"""

import logging

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.translation import gettext as _

from taxonomy.constants import MIN_VOTES_FOR_SKILLS, RATIO_THRESHOLD_FOR_SKILLS
from taxonomy.exceptions import InvalidCommandOptionsError
from taxonomy.models import XBlockSkillData

LOGGER = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Command to check if xblockskill tags are verified based on votes.
    
    The tags are marked as verified when it's verified count is
    above the minimum votes, and the ratio of verified count to
    the total count is above the ratio threshold. Both the
    minimum votes and ratio threshold values are configurable.

    Example usage:
        $ ./manage.py finalize_xblockskill_tags
    """
    help = 'Checks the votes on xblockskill tags to verify it'

    def add_arguments(self, parser):
        """
        Add arguments to the command parser
        """
        parser.add_argument(
            '--min-votes',
            help=_('Minimum number of votes required for verification'),
        )
        parser.add_argument(
            '--ratio-threshold',
            help=_('Ratio of min votes to total votes for verification'),
        )

    def handle(self, *args, **options):
        """
        Entry point for management command execution.
        """
        LOGGER.info('Starting xblockskill tags verification task')

        if not (options['min_votes'] or MIN_VOTES_FOR_SKILLS):
            raise InvalidCommandOptionsError('Either configure MIN_VOTES_FOR_SKILLS in settings \
                or pass with arg --min-votes')
        
        if not (options['ratio_threshold'] or RATIO_THRESHOLD_FOR_SKILLS):
            raise InvalidCommandOptionsError('Either configure RATIO_THRESHOLD_FOR_SKILLS in settings \
                or pass with arg --ratio-threshold')
        
        with transaction.atomic():
            unverified_skills = XBlockSkillData.objects.filter(verified=False)

            for xblock_skill in unverified_skills:
                min_votes = options['min_votes'] if options.get('min_votes', None) else MIN_VOTES_FOR_SKILLS
                ratio_threshold = options['ratio_threshold'] if options.get('ratio_threshold', None) else RATIO_THRESHOLD_FOR_SKILLS
                has_min_votes = bool(xblock_skill.verified_count > min_votes)
                total_count = int(xblock_skill.verified_count + xblock_skill.ignored_count)
                count_ratio = float(xblock_skill.verified_count / total_count)
                crosses_ratio_threshold = bool(count_ratio > ratio_threshold)
                if has_min_votes and crosses_ratio_threshold:
                    xblock_skill.verified = True
                    xblock_skill.save()
                    LOGGER.info(
                        '[%s] skill tag for the xblock [%s] has been verified',
                        xblock_skill.skill.name,
                        xblock_skill.xblock.usage_key
                    )
        LOGGER.info('Xblockskill tags verification task is completed')
