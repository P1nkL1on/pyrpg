print('Hello, world!')

# tick is functions of game logic
# hero is functions related to one hero
# party is functions related to the party

VERBOSE_LEVEL_NONE = 0
VERBOSE_LEVEL_GLOBAL = 1
VERBOSE_LEVEL_PARTY = 2
VERBOSE_LEVEL_HERO = 3

class Hero:
	name = 'name'

	# TODO: make as summ of items
	con = 3
	hunger = 0
	morale = 10

	# TODO: make as summ of items
	food = 2

	count_passed_long_roads = 0
	count_passed_short_roads = 0

	_count_passed_short_roads_for_hunger = 0
	_votes_for_share_food = False
	_votes_for_stop_and_find_food = False
	_food_opionion_multiplier = 1


def hero_suffer_penalties_long_road(hero: Hero):
	do_add_hunger = True

	hero.count_passed_long_roads += 1

	if do_add_hunger:
		hero_add_hunger(hero, 1)


def hero_suffer_penalties_short_road(hero: Hero):
	do_add_hunger = True

	hero.count_passed_short_roads += 1

	if do_add_hunger:
		count_short_roads = hero._count_passed_short_roads_for_hunger + 1
		count_short_roads_to_add_1_hunger = hero.con
		hero._count_passed_short_roads_for_hunger = count_short_roads % count_short_roads_to_add_1_hunger
		
		hero_add_hunger(hero, count_short_roads // count_short_roads_to_add_1_hunger)


def hero_add_hunger(hero: Hero, x: int):
	if x == 0:
		return

	assert x > 0
	hero.hunger += x

	if VERBOSE_LEVEL >= VERBOSE_LEVEL_HERO:
		print(f"{hero.name} gains +{x} hunger")


def hero_remove_morale(hero: Hero, x: int):
	if x == 0:
		return

	assert x > 0
	hero.morale -= x

	if VERBOSE_LEVEL >= VERBOSE_LEVEL_HERO:
		print(f"{hero.name} loses {x} morale")


def hero_priority_share_food(hero: Hero):
	return -hero.con


def tick_hero_hunger(hero: Hero):
	hero._votes_for_stop_and_find_food = False
	hero._votes_for_share_food = False

	if hero.hunger == 0:
		return

	if hero.food >= hero.hunger:
		if VERBOSE_LEVEL >= VERBOSE_LEVEL_HERO:
			print(f"{hero.name} eats {hero.hunger} food, {hero.food - hero.hunger} left")

		hero.food -= hero.hunger
		hero.hunger = 0
		return

	if hero.food > 0:
		if VERBOSE_LEVEL >= VERBOSE_LEVEL_HERO:
			print(f"{hero.name} eats last {hero.food} food, but that's not enougth")
		hero.hunger -= hero.food
		hero.food = 0

	hero_remove_morale(hero, 1)
	hero._votes_for_share_food = True

	morale_threshold_to_ask_food = 5
	if hero.morale < morale_threshold_to_ask_food:
		hero._votes_for_stop_and_find_food = True



def tick_party_hunger(heroes):
	for hero in heroes:
		tick_hero_hunger(hero)

	if party_votes_for_share_food(heroes):
		party_share_food(heroes)

	if party_votes_for_stop_and_find_food(heroes):
		assert False, 'Implement!'
		pass


# TODO: add tests
def party_summ(heroes, what_to_summ):
	summ = 0
	for hero in heroes:
		assert isinstance(hero, Hero)
		element = what_to_summ(hero)

		assert isinstance(element, (int, float))
		summ += int(element)

	return summ


# TODO: add tests
def party_votes(heroes, is_voting): 
	return party_summ(heroes, lambda x: is_voting(x)) >= len(heroes) / 2


def party_votes_for_share_food(heroes):
	return party_votes(heroes, lambda x: x._votes_for_share_food)


def party_votes_for_stop_and_find_food(heroes):
	return party_votes(heroes, lambda x: x._votes_for_stop_and_find_food)


def party_share_food(heroes):
	# TODO: add a check for already food shared normally
	# 	    to not share it every turn when struggling
	count_food = party_summ(heroes, lambda x: x.food)
	count_party = len(heroes)
	if VERBOSE_LEVEL >= VERBOSE_LEVEL_PARTY:
		print(f"party has {count_food} food for {count_party} members")
	
	# TODO: check if it changes input var heroes order
	heroes = sorted(heroes, key = lambda x: hero_priority_share_food(x))

	if count_food > count_party:
		count_food_to_each = count_food // count_party
		count_food = count_food % count_party
		for hero in heroes:
			hero.food += count_food_to_each

		if VERBOSE_LEVEL >= VERBOSE_LEVEL_PARTY:
			print(f"each party member gains {count_food_to_each} food")

	if VERBOSE_LEVEL >= VERBOSE_LEVEL_PARTY and count_food > 0:
		x = count_food
		for hero in heroes:	
			if x > 0:
				print(f"{hero.name} gains 1 extra food")
				x -= 1

	for hero in heroes:
		if count_food > 0:
			hero.food += 1	
			count_food -= 1


	if VERBOSE_LEVEL >= VERBOSE_LEVEL_PARTY:
		names = ", ".join(map(lambda x: x.name, heroes))
		print(f"party {names} shares food")


h1: Hero = Hero()
h2: Hero = Hero()
h3: Hero = Hero()

h1.name = 'Alex'
h2.name = 'Brann'
h3.name = 'Cassie'
h1.food = 10

party = [h1, h2, h3]

VERBOSE_LEVEL = VERBOSE_LEVEL_PARTY

for i in range(200):
	print(f"turn {i + 1}")

	for hero in party:
		hero_suffer_penalties_short_road(hero)

	tick_party_hunger(party)
	pass

