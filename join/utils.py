# join/utils.py

from .models import Subtask

def update_subtasks(instance, subtasks_data):
    """
    Updates the subtasks of a given Task instance.

    - Deletes subtasks that are no longer present
    - Updates existing subtasks
    - Creates new subtasks if no ID is provided

    Args:
        instance (Task): The task instance being updated.
        subtasks_data (list[dict]): A list of subtask data dictionaries.

    Returns:
        None
    """
    subtask_ids = [s['id'] for s in subtasks_data if 'id' in s]

    for subtask in instance.subtasks.all():
        if subtask.id not in subtask_ids:
            subtask.delete()

    for data in subtasks_data:
        subtask_id = data.get('id')
        if subtask_id:
            subtask = Subtask.objects.get(id=subtask_id, task=instance)
            subtask.value = data.get('value', subtask.value)
            subtask.edit = data.get('edit', subtask.edit)
            subtask.done = data.get('done', subtask.done)
            subtask.save()
        else:
            data.pop('task', None)
            Subtask.objects.create(task=instance, **data)
