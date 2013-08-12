# coding: utf-8

from common.utils import testcase

from accounts.logic import register_user
from game.heroes.prototypes import HeroPrototype

from game.logic import create_test_map
from game.balance import constants as c

from game.heroes.habilities import nonbattle
from game.heroes.relations import ITEMS_OF_EXPENDITURE


class HabilitiesNonBattleTest(testcase.TestCase):

    def setUp(self):
        super(HabilitiesNonBattleTest, self).setUp()
        create_test_map()

        result, account_id, bundle_id = register_user('test_user')
        self.hero = HeroPrototype.get_by_account_id(account_id)

    def tearDown(self):
        pass

    def test_charisma(self):
        self.assertTrue(100 < nonbattle.CHARISMA().update_quest_reward(self.hero, 100))

    def test_hackster(self):
        self.assertTrue(100 > nonbattle.HUCKSTER().update_buy_price(self.hero, 100))
        self.assertTrue(100 < nonbattle.HUCKSTER().update_sell_price(self.hero, 100))

    def test_dandy(self):
        priorities = {record:record.priority for record in ITEMS_OF_EXPENDITURE._records}
        priorities = nonbattle.DANDY().update_items_of_expenditure_priorities(self.hero, priorities)

        self.assertEqual(ITEMS_OF_EXPENDITURE.INSTANT_HEAL.priority, priorities[ITEMS_OF_EXPENDITURE.INSTANT_HEAL])
        self.assertEqual(ITEMS_OF_EXPENDITURE.USELESS.priority, priorities[ITEMS_OF_EXPENDITURE.USELESS])
        self.assertEqual(ITEMS_OF_EXPENDITURE.IMPACT.priority, priorities[ITEMS_OF_EXPENDITURE.IMPACT])

        self.assertTrue(ITEMS_OF_EXPENDITURE.BUYING_ARTIFACT.priority < priorities[ITEMS_OF_EXPENDITURE.BUYING_ARTIFACT])
        self.assertTrue(ITEMS_OF_EXPENDITURE.SHARPENING_ARTIFACT.priority < priorities[ITEMS_OF_EXPENDITURE.SHARPENING_ARTIFACT])

    def test_businessman(self):
        self.assertFalse(any(self.hero.can_get_artifact_for_quest() for i in xrange(200)))
        self.hero.abilities.add(nonbattle.BUSINESSMAN.get_id())
        self.assertTrue(any(self.hero.can_get_artifact_for_quest() for i in xrange(200)))

    def test_picky(self):
        self.assertFalse(any(self.hero.can_buy_better_artifact() for i in xrange(200)))
        self.hero.abilities.add(nonbattle.PICKY.get_id())
        self.assertTrue(any(self.hero.can_buy_better_artifact() for i in xrange(200)))

    def test_ethereal_magnet(self):
        old_crit_chance = self.hero.might_crit_chance
        self.hero.abilities.add(nonbattle.ETHEREAL_MAGNET.get_id())
        self.assertTrue(self.hero.might_crit_chance > old_crit_chance)

    def test_wanderer(self):
        old_speed = self.hero.move_speed
        self.hero.abilities.add(nonbattle.WANDERER.get_id())
        self.assertTrue(self.hero.move_speed > old_speed)

    def test_gifted(self):
        self.hero.add_experience(10)
        experience_delta = self.hero.experience

        self.hero.abilities.add(nonbattle.GIFTED.get_id())
        self.hero.add_experience(10)

        self.assertTrue(self.hero.experience > experience_delta * 2)
