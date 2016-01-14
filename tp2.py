import random
import sys

class Bag:

	BEST_VALUE = 0

	def __init__(self, content_max, content = []):
		self.__content_max = content_max
		self.__left_son = None
		self.__right_son = None
		self.__children = (self.__left_son, self.__right_son)
		self.__content = content

	def get_left_son(self):
		return self.__left_son

	def set_left_son(self, son):
		self.__left_son = son
		self.__children = (self.__left_son, self.__right_son)

	def get_right_son(self):
		return self.__right_son

	def set_right_son(self, son):

		self.__right_son = son
		self.__children = (self.__left_son, self.__right_son)

	def get_children(self):
		return self.__children

	def get_content_max(self):
		return self.__content_max

	def get_content(self):
		return self.__content

	def get_value(self):
		return sum([obj.get_value() for obj in self.__content])

	def __iter__(self):
		return self.__content.__iter__()


class Objet:

	def __init__(self, weight, value, ident, prop = 1):
		self.__weight = weight
		self.__value = value
		self.__ident = ident
		self.__prop = prop

	def get_weight(self):
		return self.__weight * self.__prop

	def get_value(self):
		return self.__value * self.__prop

	def get_ident(self):
		return self.__ident

	def set_prop(self, value):
		self.__prop = value

	def duplicate(self, prop = 1):
		return Objet(self.__weight, self.__value, self.__ident, prop)

	def __repr__(self):
		return "n°: " + str(self.__ident) + "\tmon poids: " + str(self.__weight) + "\tma valeur: " + str(self.__value) + "\tmon ratio:" + str(self.__value / self.__weight)

	def __lt__(self, other):
		ratio_self = self.__value / self.__weight
		ratio_other = other.get_value() / other.get_weight()
		return (ratio_self < ratio_other)


def initialize(filename):
	f = open(filename, 'r')
	line = f.readline()
	max_content = float(line)
	sac = Bag(max_content)
	maison = []
	line = f.readline()
	ident = 1
	while line != "":
		values = line.split()
		maison.append(Objet(float(values[0]), float(values[1]), ident))
		line = f.readline()
		ident += 1
	f.close()
	return (sorted(maison, reverse=True), sac)


def max_boundary(maison, weight_max, value):

	weight = 0
	i = 0
	while (weight <= weight_max and i < len(maison)):
		if  (weight_max - (weight + maison[i].get_weight()) > 0):
			weight += maison[i].get_weight()
			value += maison[i].get_value()
		elif (weight != weight_max):
			prop = ((weight_max - weight) / maison[i].get_weight())
			weight += maison[i].get_weight() * prop
			value += maison[i].get_value() * prop
		else:
			break
		i += 1

	return value

def walk(maison, sac):
	if len(maison) > 0:
		if (max_boundary(maison, sac.get_content_max(), sac.get_value()) > Bag.BEST_VALUE):

			sac.set_right_son(Bag(sac.get_content_max(), sac.get_content()))

			if sac.get_content_max() - maison[0].get_weight() >= 0:
				added_object = maison[0].duplicate()
				#sac.set_right_son(Bag(sac.get_content_max() - maison[0].get_weight(), sac.get_content() + [maison[0]]))
				sac.set_left_son(Bag(sac.get_content_max() - added_object.get_weight(), sac.get_content() + [added_object]))

			elif sac.get_content_max() > 0:
				proportion = sac.get_content_max() / maison[0].get_weight()
				added_object = maison[0].duplicate(proportion)
				sac.set_left_son(Bag(sac.get_content_max() - added_object.get_weight(), sac.get_content() + [added_object]))


		# yield sac
		# for child in sac.get_children():
		# 	if child is not None:
		# 		for obj in walk(maison[1:], child):
		# 			yield obj

		for child in sac.get_children():
			if child is not None:
				for obj in walk(maison[1:], child):
					yield obj
	else:
		if (sac.get_value() > Bag.BEST_VALUE):
			Bag.BEST_VALUE = sac.get_value()
			yield sac

def walk2(maison, sac):
	contenu = []
	if len(maison) > 0:
		if (max_boundary(maison, sac.get_content_max(), sac.get_value()) > Bag.BEST_VALUE):

			sac.set_right_son(Bag(sac.get_content_max(), sac.get_content()))

			print(max_boundary(maison, sac.get_content_max(), sac.get_value()), Bag.BEST_VALUE)

			if sac.get_content_max() - maison[0].get_weight() >= 0:
				added_object = maison[0].duplicate()
				sac.set_left_son(Bag(sac.get_content_max() - added_object.get_weight(), sac.get_content() + [added_object]))

			elif sac.get_content_max() > 0:
				proportion = sac.get_content_max() / maison[0].get_weight()
				added_object = maison[0].duplicate(proportion)
				sac.set_left_son(Bag(sac.get_content_max() - added_object.get_weight(), sac.get_content() + [added_object]))


		contenu.append(sac)
		for child in sac.get_children():
			if child is not None:
				for obj in walk2(maison[1:], child):
					contenu.append(obj)
	else:
		if (sac.get_value() > Bag.BEST_VALUE):
			Bag.BEST_VALUE = sac.get_value()
			contenu.append(sac)

	return contenu


if __name__ == "__main__":

	sys.setrecursionlimit(1005)
	maison, sac = initialize("test.txt")
	print("Poids max: " + str(sac.get_content_max()))
	for obj in maison:
		print(obj)

	for x in walk(maison, sac):
			print("Contenu max: " + str(x.get_content_max()) + "\t" + "Meilleure valeur: " + str(Bag.BEST_VALUE) + "\t" + "Valeur courante: " + str(x.get_value()) + "\t" + str([obj.get_ident() for obj in x]))

	# print(50.0)
	# for i in range(1000):
	# 	print(str(float(random.randint(1,10.0))) + " " + str(float(random.randint(1,41))))


