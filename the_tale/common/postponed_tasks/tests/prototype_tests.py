# coding: utf-8
import time
import mock
import datetime

from common.utils.testcase import TestCase, CallCounter

from common.postponed_tasks.exceptions import PostponedTaskException
from common.postponed_tasks.prototypes import PostponedTaskPrototype, postponed_task, _INTERNAL_LOGICS
from common.postponed_tasks.models import PostponedTask, POSTPONED_TASK_STATE
from common.postponed_tasks.tests.helpers import FakePostponedInternalTask


class PrototypeTests(TestCase):

    def setUp(self):
        self.task = PostponedTaskPrototype.create(FakePostponedInternalTask())

    def test_internals_tasks_collection(self):
        self.assertEqual(_INTERNAL_LOGICS, {'fake-task': FakePostponedInternalTask})

    def test_internals_tasks_collection_duplicate_registration(self):

        class Fake2PostponedInternalTask(object):
            TYPE = 'fake-task'

        self.assertRaises(PostponedTaskException, postponed_task, Fake2PostponedInternalTask)


    def test_create(self):
        self.assertTrue(self.task.state.is_waiting)
        self.assertTrue(self.task.internal_state, FakePostponedInternalTask.INITIAL_STATE)
        self.assertEqual(self.task.internal_logic.TYPE, FakePostponedInternalTask.TYPE)
        self.assertTrue(PostponedTaskPrototype.check_if_used(FakePostponedInternalTask.TYPE, 777))

    def test_reset_all(self):
        task = PostponedTaskPrototype.create(FakePostponedInternalTask())
        task.state = POSTPONED_TASK_STATE.PROCESSED
        task.save()

        self.assertEqual(PostponedTask.objects.all().count(), 2)
        self.assertEqual(PostponedTask.objects.filter(state=POSTPONED_TASK_STATE.WAITING).count(), 1)
        self.assertEqual(PostponedTask.objects.filter(state=POSTPONED_TASK_STATE.PROCESSED).count(), 1)
        self.assertEqual(PostponedTask.objects.filter(state=POSTPONED_TASK_STATE.RESETED).count(), 0)

        PostponedTaskPrototype.reset_all()

        self.assertEqual(PostponedTask.objects.all().count(), 2)
        self.assertEqual(PostponedTask.objects.filter(state=POSTPONED_TASK_STATE.WAITING).count(), 0)
        self.assertEqual(PostponedTask.objects.filter(state=POSTPONED_TASK_STATE.PROCESSED).count(), 1)
        self.assertEqual(PostponedTask.objects.filter(state=POSTPONED_TASK_STATE.RESETED).count(), 1)


    def test_process_not_waiting_state(self):

        for state in POSTPONED_TASK_STATE.ALL:

            if state == POSTPONED_TASK_STATE.WAITING:
                continue

            self.task.state = state

            process_call_counter = CallCounter(return_value=True)

            with mock.patch.object(FakePostponedInternalTask, 'process', process_call_counter):
                self.task.process()

            self.assertEqual(process_call_counter.count, 0)
            self.assertEqual(self.task.state, state)

    def test_process_timeout(self):

        self.task.model.live_time = -1

        process_call_counter = CallCounter(return_value=True)

        with mock.patch.object(FakePostponedInternalTask, 'process', process_call_counter):
            self.task.process()

        self.assertEqual(process_call_counter.count, 0)
        self.assertTrue(self.task.state.is_timeout)


    def test_process_success(self):
        process_call_counter = CallCounter(return_value=True)

        with mock.patch.object(FakePostponedInternalTask, 'process', process_call_counter):
            self.task.process()

        self.assertEqual(process_call_counter.count, 1)
        self.assertTrue(self.task.state.is_processed)


    def test_process_internal_error(self):

        process_call_counter = CallCounter(return_value=False)

        with mock.patch.object(FakePostponedInternalTask, 'process', process_call_counter):
            self.task.process()

        self.assertEqual(process_call_counter.count, 1)
        self.assertTrue(self.task.state.is_error)


    def test_process_exception(self):

        def process_with_exception(self, *argv, **kwargs):
            raise Exception()

        with mock.patch.object(FakePostponedInternalTask, 'process', process_with_exception):
            self.task.process()

        self.assertTrue(self.task.state.is_exception)
        self.assertTrue(self.task.comment)
