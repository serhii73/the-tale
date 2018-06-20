
import smart_imports

smart_imports.all()

from the_tale.game.heroes.habilities import companions


class HabilitiesCompanionsTest(utils_testcase.TestCase):

    def setUp(self):
        super(HabilitiesCompanionsTest, self).setUp()
        game_logic.create_test_map()

        self.account = self.accounts_factory.create_account()
        self.storage = game_logic_storage.LogicStorage()
        self.storage.load_account_data(self.account)
        self.hero = self.storage.accounts_to_heroes[self.account.id]


    def test_walker(self):
        self.assertEqual(companions_abilities.WALKER().modify_attribute(relations.MODIFIERS.COMPANION_ABILITIES_LEVELS, {}),
                        {companions_abilities_relations.METATYPE.TRAVEL: 1})
        self.assertEqual(companions_abilities.WALKER().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_ABILITIES_LEVELS,)), {}), {})

        self.assertEqual(self.hero.companion_abilities_levels, {})
        self.hero.abilities.add(companions_abilities.WALKER.get_id(), 3)
        self.assertEqual(self.hero.companion_abilities_levels, {companions_abilities_relations.METATYPE.TRAVEL: 3})

    def test_comrade(self):
        self.assertEqual(companions_abilities.COMRADE().modify_attribute(relations.MODIFIERS.COMPANION_ABILITIES_LEVELS, {}),
                        {companions_abilities_relations.METATYPE.BATTLE: 1})
        self.assertEqual(companions_abilities.COMRADE().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_ABILITIES_LEVELS,)), {}), {})

        self.assertEqual(self.hero.companion_abilities_levels, {})
        self.hero.abilities.add(companions_abilities.COMRADE.get_id(), 3)
        self.assertEqual(self.hero.companion_abilities_levels, {companions_abilities_relations.METATYPE.BATTLE: 3})

    def test_improviser(self):
        self.assertEqual(companions_abilities.IMPROVISER().modify_attribute(relations.MODIFIERS.COMPANION_ABILITIES_LEVELS, {}),
                        {companions_abilities_relations.METATYPE.OTHER: 1})
        self.assertEqual(companions_abilities.IMPROVISER().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_ABILITIES_LEVELS,)), {}), {})

        self.assertEqual(self.hero.companion_abilities_levels, {})
        self.hero.abilities.add(companions_abilities.IMPROVISER.get_id(), 3)
        self.assertEqual(self.hero.companion_abilities_levels, {companions_abilities_relations.METATYPE.OTHER: 3})

    def test_economic(self):
        self.assertEqual(companions_abilities.ECONOMIC().modify_attribute(relations.MODIFIERS.COMPANION_ABILITIES_LEVELS, {}),
                        {companions_abilities_relations.METATYPE.MONEY: 1})
        self.assertEqual(companions_abilities.ECONOMIC().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_ABILITIES_LEVELS,)), {}), {})

        self.assertEqual(self.hero.companion_abilities_levels, {})
        self.hero.abilities.add(companions_abilities.ECONOMIC.get_id(), 3)
        self.assertEqual(self.hero.companion_abilities_levels, {companions_abilities_relations.METATYPE.MONEY: 3})

    def test_thoughtful(self):
        self.assertEqual(companions_abilities.THOUGHTFUL().modify_attribute(relations.MODIFIERS.COMPANION_MAX_HEALTH, 1.0), 1.1)
        self.assertEqual(companions_abilities.THOUGHTFUL().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_MAX_HEALTH,)), 1), 1)

        self.assertEqual(self.hero.companion_max_health_multiplier, 1)
        self.hero.abilities.add(companions_abilities.THOUGHTFUL.get_id(), 3)
        self.assertEqual(self.hero.companion_max_health_multiplier, 1.3)

    def test_coherence(self):
        self.assertEqual(companions_abilities.COHERENCE().modify_attribute(relations.MODIFIERS.COMPANION_MAX_COHERENCE, 0), 20)
        self.assertEqual(companions_abilities.COHERENCE().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_MAX_COHERENCE,)), 1), 1)

        self.assertEqual(self.hero.companion_max_coherence, 20) # coherence lvl 1 — default hero ability
        self.hero.abilities.add(companions_abilities.COHERENCE.get_id(), 3)
        self.assertEqual(self.hero.companion_max_coherence, 60)

    def test_healing(self):
        self.assertEqual(companions_abilities.HEALING().modify_attribute(relations.MODIFIERS.COMPANION_LIVING_HEAL, 0), 0.11574074074074076)
        self.assertEqual(companions_abilities.HEALING().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_LIVING_HEAL,)), 0), 0)

        companion_record = next(companions_storage.companions.enabled_companions())
        self.hero.set_companion(companions_logic.create_companion(companion_record))

        with mock.patch('the_tale.game.companions.objects.CompanionRecord.type', beings_relations.TYPE.ANIMAL):
            self.assertEqual(self.hero.companion_heal_probability, 0)
            self.hero.abilities.add(companions_abilities.HEALING.get_id(), 3)
            self.assertEqual(self.hero.companion_heal_probability, 0.3472222222222222)

    def test_mage_mechanincs(self):
        self.assertEqual(companions_abilities.MAGE_MECHANICS().modify_attribute(relations.MODIFIERS.COMPANION_CONSTRUCT_HEAL, 0), 0.11574074074074076)
        self.assertEqual(companions_abilities.MAGE_MECHANICS().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_CONSTRUCT_HEAL,)), 0), 0)

        companion_record = next(companions_storage.companions.enabled_companions())
        self.hero.set_companion(companions_logic.create_companion(companion_record))

        with mock.patch('the_tale.game.companions.objects.CompanionRecord.type', beings_relations.TYPE.MECHANICAL):
            self.assertEqual(self.hero.companion_heal_probability, 0)
            self.hero.abilities.add(companions_abilities.MAGE_MECHANICS.get_id(), 3)
            self.assertEqual(self.hero.companion_heal_probability, 0.3472222222222222)

    def test_witchcraft(self):
        self.assertEqual(companions_abilities.WITCHCRAFT().modify_attribute(relations.MODIFIERS.COMPANION_UNUSUAL_HEAL, 0), 0.11574074074074076)
        self.assertEqual(companions_abilities.WITCHCRAFT().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_UNUSUAL_HEAL,)), 0), 0)

        companion_record = next(companions_storage.companions.enabled_companions())
        self.hero.set_companion(companions_logic.create_companion(companion_record))

        with mock.patch('the_tale.game.companions.objects.CompanionRecord.type', beings_relations.TYPE.SUPERNATURAL):
            self.assertEqual(self.hero.companion_heal_probability, 0)
            self.hero.abilities.add(companions_abilities.WITCHCRAFT.get_id(), 3)
            self.assertEqual(self.hero.companion_heal_probability, 0.3472222222222222)

    def test_sociability(self):
        self.assertEqual(companions_abilities.SOCIABILITY().modify_attribute(relations.MODIFIERS.COMPANION_LIVING_COHERENCE_SPEED, 1), 1.2)
        self.assertEqual(companions_abilities.SOCIABILITY().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_LIVING_COHERENCE_SPEED,)), 1), 1)

        companion_record = next(companions_storage.companions.enabled_companions())
        self.hero.set_companion(companions_logic.create_companion(companion_record))

        with mock.patch('the_tale.game.companions.objects.CompanionRecord.type', beings_relations.TYPE.ANIMAL):
            self.assertEqual(self.hero.companion_coherence_speed, 1)
            self.hero.abilities.add(companions_abilities.SOCIABILITY.get_id(), 3)
            self.assertEqual(self.hero.companion_coherence_speed, 1.6)

    def test_service(self):
        self.assertEqual(companions_abilities.SERVICE().modify_attribute(relations.MODIFIERS.COMPANION_CONSTRUCT_COHERENCE_SPEED, 1), 1.2)
        self.assertEqual(companions_abilities.SERVICE().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_CONSTRUCT_COHERENCE_SPEED,)), 1), 1)

        companion_record = next(companions_storage.companions.enabled_companions())
        self.hero.set_companion(companions_logic.create_companion(companion_record))

        with mock.patch('the_tale.game.companions.objects.CompanionRecord.type', beings_relations.TYPE.MECHANICAL):
            self.assertEqual(self.hero.companion_coherence_speed, 1)
            self.hero.abilities.add(companions_abilities.SERVICE.get_id(), 3)
            self.assertEqual(self.hero.companion_coherence_speed, 1.6)

    def test_sacredness(self):
        self.assertEqual(companions_abilities.SACREDNESS().modify_attribute(relations.MODIFIERS.COMPANION_UNUSUAL_COHERENCE_SPEED, 1), 1.2)
        self.assertEqual(companions_abilities.SACREDNESS().modify_attribute(relations.MODIFIERS.random(exclude=(relations.MODIFIERS.COMPANION_UNUSUAL_COHERENCE_SPEED,)), 1), 1)

        companion_record = next(companions_storage.companions.enabled_companions())
        self.hero.set_companion(companions_logic.create_companion(companion_record))

        with mock.patch('the_tale.game.companions.objects.CompanionRecord.type', beings_relations.TYPE.SUPERNATURAL):
            self.assertEqual(self.hero.companion_coherence_speed, 1)
            self.hero.abilities.add(companions_abilities.SACREDNESS.get_id(), 3)
            self.assertEqual(self.hero.companion_coherence_speed, 1.6)
