"""
This module contains taxonomy related signals.
"""


from django.dispatch import Signal, receiver
from django.db.models.signals import post_save, pre_delete
from django_celery_beat.models import PeriodicTask
from taxonomy.models import SkillVerificationSchedule

UPDATE_COURSE_SKILLS = Signal()
UPDATE_PROGRAM_SKILLS = Signal()
UPDATE_XBLOCK_SKILLS = Signal()

# pylint: disable=unused-argument
@receiver(post_save, sender=SkillVerificationSchedule)
def create_or_update_related_task(
    sender, instance: SkillVerificationSchedule, *args, **kwargs
) -> None:
    """
    Create or update a `PeriodicTask` based on the `SkillVerificationSchedule`.
    """
    # Get the celery task by ID if exists or create an "empty" task
    celery_task = (
        PeriodicTask.objects.get(id=instance.celery_task.id)
        if instance.celery_task
        else PeriodicTask()
    )

    # Override the celery task arguments
    celery_task.name = instance.task.name
    celery_task.task = "taxonomy.tasks.check_for_skill_verification"
    celery_task.interval = instance.interval
    celery_task.save()

    # If the celery task was not set before, set it
    if not instance.celery_task:
        instance.celery_task = celery_task
        instance.save()


# pylint: disable=unused-argument
@receiver(pre_delete, sender=SkillVerificationSchedule)
def delete_related_task(
    sender, instance: SkillVerificationSchedule, *args, **kwargs
):
    """
    Delete the related celery task to not leave dangling references behind.
    """
    instance.celery_task.delete()
