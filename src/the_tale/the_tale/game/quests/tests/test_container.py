
import smart_imports

smart_imports.all()


class ContainerTests(utils_testcase.TestCase):

    def setUp(self):
        super(ContainerTests, self).setUp()
        game_logic.create_test_map()

        account = self.accounts_factory.create_account(is_fast=True)

        self.storage = game_logic_storage.LogicStorage()
        self.storage.load_account_data(account.id)
        self.hero = self.storage.accounts_to_heroes[account.id]

        self.container = container.QuestsContainer()
        self.container.hero = self.hero

    def test_add_interfered_person(self):
        self.assertFalse(self.container.is_person_interfered(1))
        self.container.add_interfered_person(1)
        self.assertTrue(self.container.is_person_interfered(1))

    def test_sync_interfered_persons(self):
        self.container.interfered_persons[1] = time.time() - conf.settings.INTERFERED_PERSONS_LIVE_TIME
        self.container.interfered_persons[2] = time.time()
        self.container.interfered_persons[3] = time.time() - conf.settings.INTERFERED_PERSONS_LIVE_TIME + 1

        self.assertFalse(self.container.is_person_interfered(1))
        self.assertTrue(self.container.is_person_interfered(2))
        self.assertTrue(self.container.is_person_interfered(3))

        self.container.sync_interfered_persons()

        self.assertFalse(self.container.is_person_interfered(1))
        self.assertTrue(self.container.is_person_interfered(2))
        self.assertTrue(self.container.is_person_interfered(3))

    def test_excluded_quests__no_history(self):
        self.assertEqual(self.container.history, {})
        self.assertEqual(self.container.excluded_quests(3), [])

    def test_excluded_quests(self):
        self.assertEqual(self.container.history, {})

        self.container.update_history('q_1', 5)
        self.container.update_history('q_2', 4)
        self.container.update_history('q_3', 3)
        self.container.update_history('q_4', 2)
        self.container.update_history('q_5', 1)
        self.container.update_history('q_6', 0)

        self.assertEqual(self.container.excluded_quests(0), [])
        self.assertEqual(set(self.container.excluded_quests(1)), set(['q_1']))
        self.assertEqual(set(self.container.excluded_quests(3)), set(['q_1', 'q_2', 'q_3']))
        self.assertEqual(set(self.container.excluded_quests(7)), set(['q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6']))

    def test_push_quest(self):
        with mock.patch('the_tale.game.quests.container.QuestsContainer.mark_updated') as mark_updated:
            with mock.patch('the_tale.game.actions.container.ActionsContainer.request_replane') as request_replane:
                self.container.push_quest('QUEST')

        self.assertEqual(mark_updated.call_count, 1)

        self.assertEqual(request_replane.call_count, 1)

        with mock.patch('the_tale.game.quests.container.QuestsContainer.mark_updated') as mark_updated:
            with mock.patch('the_tale.game.actions.container.ActionsContainer.request_replane') as request_replane:
                self.container.pop_quest()

        self.assertEqual(mark_updated.call_count, 1)

        self.assertEqual(request_replane.call_count, 1)

    def test_mark_updated(self):
        self.container._ui_info = 'fake ui info'

        self.container.mark_updated()

        self.assertEqual(self.container._ui_info, None)

    def test_ui_info(self):

        self.assertEqual(self.container._ui_info, None)

        with mock.patch('the_tale.game.quests.container.QuestsContainer._get_ui_info', mock.Mock(return_value='fake ui info')) as get_ui_info:
            self.container.ui_info(self.hero)

        self.assertEqual(get_ui_info.call_count, 1)

        self.assertEqual(self.container._ui_info, 'fake ui info')

        with mock.patch('the_tale.game.quests.container.QuestsContainer._get_ui_info', mock.Mock(return_value='fake ui info 2')) as get_ui_info:
            self.container.ui_info(self.hero)

        self.assertEqual(get_ui_info.call_count, 0)

        self.assertEqual(self.container._ui_info, 'fake ui info')
