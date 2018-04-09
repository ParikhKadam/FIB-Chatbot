#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- general imports --#
import json
import random


class Item_generator(object):

	"""This class allows random generation of items (such as teachers)

		Parameters:
			data(:obj:`list` or :obj:`str`): list of items or path to get the file with
				the data
			num_items(:obj:`int`): limit of items that the generator can generate

		Attributes:
			num_items(:obj:`int`): limit of items that the generator can generate
			items(:obj:`list`): list of the items that can be generated
	"""
	def __init__(self, data, num_items = 9999, name = False):
		self.name = name
		if isinstance(data, list):
			d_size = len(data)
			self.num_items = min(num_items, d_size)
			self.items = data[:self.num_items]
		else:
			d_size = len(open(data,'r').readlines())
			self.num_items = min(num_items, d_size)
			self.items = open(data,'r').readlines()[:self.num_items]
	"""
		Returns a random element of the item list
	"""
	def get_random(self):
		i_idx = random.randint(0, self.num_items-1)
		shorten = random.randint(0,100) <= 50;
		if shorten and self.name:
			length = random.randint(1, 2)
			return ' '.join(self.items[i_idx].split(' ')[0:length])
		return self.items[i_idx]


class Data_generator(object):

	"""This class allows random generation of data (for instance, questions)

		Parameters:
			i_g(:class:`Item_generator`): Item generator for the data (items)
			s_g(:class:`Item_generator`): Item generator for the sentences (not items)
			type_(:type:`str`): can either be 'teacher' or 'subject', defines the type of item used
			intent(:type:`str`): defines the intent of the sentence to be generated

		Attributes:
			num_items(:obj:`int`): limit of items that the generator can generate
			items(:obj:`list`): list of the items that can be generated
	"""
	def __init__(self, i_g, s_g, type_, intent):
		self.i_g = i_g
		self.s_g = s_g
		self.type = type_
		self.intent = intent

	"""
		Parameters:
			num_examples(:obj:`int`): defines the amount of examples to be generated

		This function returns a list (of size num_examples) of random generated examples
	"""
	def get_examples(self, num_examples):
		examples = []
		for i in range(num_examples):
			examples.append(self.get_random_element())
		return examples

	"""
		This function returns a random sentence generated with both generators
	"""
	def get_random_element(self):
		entity = self.i_g.get_random().lower().rstrip()
		sentence = self.s_g.get_random()
		offset_ini = 0
		for char in sentence:
			if char != "{":
				offset_ini += 1
			else: break
		offset_fi = offset_ini + len(entity)
		if self.type == 'teacher': entity_type = 'teacher_name'
		if self.type == 'subject': entity_type = 'subject_acronym'
		return {
			"text": sentence.format(entity),
			"intent": self.intent,
			"entities": [
				{
					'start': offset_ini,
					'end': offset_fi,
					'value': entity,
					'entity': entity_type,
				}
			]
		}


def main(amount = 250, language = 'es'):
	intros_teacher_mail = ["correo de {}", "cual es el correo de {}", "cual es el correo de {}?", "mail de {}", "cual es el mail de {}?"]
	intros_teacher_desk = ["cual es el despacho de {}?", "cual es el despacho de {}", "despacho de {}", "donde esta el despacho de {}?", "dónde está el despacho de {}"]
	intros_subject_free_spots = ['plazas libres en {}', 'plazas libres de {}', 'cuantas plazas libres quedan en {}?',
			'cuantos huecos hay en {}', 'plazas de {}', 'plazas en {}', "cuantas plazas libres hay en {}?",
			"plazas en {}", "cuantas plazas hay en {}"]
	intros_subject_schedule = ['horario de {}', "cual es el horario de {}?",
			"cuando tengo {}?", 'cuando tengo {}', "cuando hago {}?", "cuando hago {}",
			"a qué hora tengo {}?", "a que hora tengo {}"]
	intros_subject_clasroom = ['en que clase hago {}?', "en que clase tengo {}",
			'donde hago {}', "clase de {}", 'cual es la clase de {}?',
			"aula de {}", "en que aula tengo {}"]
	intros_subject_teacher_mail = ["correo del profesor de {}", "cual es el correo del profe de {}", "mail del profe de {}", "cual es el mail del profe de {}"]
	intros_subject_teacher_office = ["despacho del profesor de {}", "cual es el despacho del profe de {}", "donde esta el despacho del profesor de {}"]
	intros_subject_teacher_name = ["nombre del profesor de {}", "nombre de la profesora de {}", "como se llama el profe de {}", "profesor de {}", "profe de {}", "quien es el profesor de {}",
	"quienes son los profesores de {}", "quien es el profesor de {}?", "quien es la profesora de {}"]

	if language == 'en':
		intros_teacher_mail = ["{}'s mail", "what is {}'s mail", "what is {}'s mail?", "mail of {}", "what's the mail of {}"]
		intros_teacher_desk = ["what's {}'s office?", "what's {}'s office", "{}'s office", "office of {}", "what's the office of {}"]
		intros_subject_free_spots = ['free spots in {}', 'how many free spots are in {}?',
				'how many free spots are in {}', 'spots left in {}', "how many free spots are there in {}",
				"free spots of {}", "{}'s free spots"]
		intros_subject_schedule = ['schedule of {}', "what's {}'s schedule?",
				"what's {}'s schedule", 'when do i have {}', "when do i do {}"]
		intros_subject_clasroom = ['in which class do i have {}?', "where do i do {}",
				'in which class do i have {}',"{}'s classroom", "where do i have {}",
				"classroom of {}", "class of {}"]
		intros_subject_teacher_mail = ["{}'s teacher's mail ", "what's the mail of {}'s teacher", "{}'s teacher mail", "what is the mail of {} teacher"]
		intros_subject_teacher_office = ["office of {}'s teacher'", "{}'s teacher office", "{} teacher office", "whats {} teacher office"]
		intros_subject_teacher_name = ["name of the teacher of {}", "{}'s teacher's name", "Who is the teacher of {}", "{}'s teacher"]

	elif language == 'ca':
		intros_teacher_mail = ["correu de {}", "correu del {}", "correu de la {}",
		"quin es el correu de {}", "quin es el correu del {}", "quin es el correu de la {}",
		"quin es el correu de {}?", "quin es el correu del {}?", "quin es el correu de la {}?",
		"quin es el mail de {}?", "quin es el mail del {}?", "quin es el mail de la {}?",
		"quin es el mail de {}", "quin es el mail del {}", "quin es el mail de la {}",
		"mail de {}", "mail del {}", "mail de la {}"]
		intros_teacher_desk = ["quin es el despatx de {}?", "quin es el despatx del {}?", "quin es el despatx de la {}?",
		"quin es el despatx de {}", "quin es el despatx del {}", "quin es el despatx de la {}",
		"despatx de {}", "despatx del {}", "despatx de la {}",
		"on esta el despatx de {}?","on esta el despatx del {}?", "on esta el despatx de la {}?",
		"on esta el despatx de {}","on es el despatx del {}", "on es el despatx de la {}",
		"on és el despatx de {}?","on es el despatx del {}?", "on és el despatx de la {}?"]
		intros_subject_free_spots = ['places lliures en {}', 'places lliures de {}', 'quantes places lliures queden a {}?',
				'quants espais hi ha a {}', 'places de {}', 'places a {}', "quantes places lliures hi ha a {}?",
				"plazas en {}", "cuantas plazas hay en {}"]
		intros_subject_schedule = ['horari de {}', "quin és l'horari de {}?",
				"quant tinc {}?", 'quan hi ha {}', "quan faig {}?", "quan tindré {}",
				"A quina hora tinc {}", "a quina hora faig {}?"]
		intros_subject_clasroom = ['a quina classe faig{}?', "a quina classe faig {}",
				'on tinc {}', "aula de {}", 'quina és la classe de {}?',
				"aula de {}", "a quina aula tinc {}?"]
		intros_subject_teacher_mail = ["correu del professor de {}", "correu de la professora de {}", "correu del profe de {}", "correu de la profe de {}",
		"quin és el correu del profe de {}", "quin és el correu de la profe de {}?", "quin és el correu del profe de {}", "quin és el correu de la profe de {}",
		"quin és el correu del professor de {}", "quin és el correu de la professora de {}",
		"mail del profe de {}", "mail de la profe de {}", "mail del professor de {}", "mail de la professora de {}",
		"quin es el mail del profe de {}", "quin es el mail de la profe de {}", "quin es el mail del profe de {}", "quin es el mail de la professora de {}?"]
		intros_subject_teacher_office = ["despatx del professor de {}", "despatx de la professora de {}", "despatx del profe de {}", "despatx de la profe de {}",
		"quin és el despatx del profe de {}", "quin és el despatx de la profe de {}",
		"quin és el despatx del professor de {}", "quin és el despatx de la professora de {}",
		"quin és el despatx del profe de {}?", "quin és el despatx de la profe de {}?",
		"quin és el despatx del professor de {}?", "quin és el despatx de la professora de {}?",
		"on és el despatx del profe de {}", "on és el despatx de la profe de {}",
		"on és el despatx del professor de {}", "on és el despatx de la professora de {}",
		"on és el despatx del profe de {}?", "on és el despatx de la profe de {}?",
		"on és el despatx del professor de {}?", "on és el despatx de la professora de {}?"]
		intros_subject_teacher_name = ["nom del profesor de {}", "nom de la professora de {}",
		 "com es diu el profe de {}?",  "com es diu la  profe de {}?", "com es diu el professor de {}?", "com es diu la professora de {}?",
		 "professor de {}", "professora de {}",
		 "profe de {}", "qui és el professor de {}", "qui és la professora de {}?", "qui és profe de {}"]


	regex_features = []
	entity_synonyms = []
	common_examples = []

	teacher_gen = Item_generator(data = "./Data/Professors.txt", name = True)
	subject_gen = Item_generator(data = "./Data/Subjects.txt")

	intro_mail_gen = Item_generator(data = intros_teacher_mail)
	intro_desk_gen = Item_generator(data = intros_teacher_desk)
	intro_spots_gen = Item_generator(data = intros_subject_free_spots)
	intro_schedule_gen = Item_generator(data = intros_subject_schedule)
	intro_classroom_gen = Item_generator(data = intros_subject_clasroom)
	intro_subject_teacher_mail_gen = Item_generator(data = intros_subject_teacher_mail)
	intro_subject_teacher_office_gen = Item_generator(data = intros_subject_teacher_office)
	intro_subject_teacher_name_gen = Item_generator(data = intros_subject_teacher_name)
	#intro_inform_teacher_gen = Item_generator(data = intros_inform_teacher)
	#intro_inform_subject_gen = Item_generator(data = intros_inform_subject)

	teacher_mail_gen = Data_generator(teacher_gen, intro_mail_gen, type_="teacher", intent="ask_teacher_mail")
	teacher_desk_gen = Data_generator(teacher_gen, intro_desk_gen, type_="teacher", intent="ask_teacher_office")
	subject_spots_gen = Data_generator(subject_gen, intro_spots_gen, type_="subject", intent="ask_free_spots")
	subject_schedule_gen = Data_generator(subject_gen, intro_schedule_gen, type_="subject", intent="ask_subject_schedule")
	subject_classroom_gen = Data_generator(subject_gen, intro_classroom_gen, type_="subject", intent="ask_subject_classroom")
	subject_teacher_mail_gen = Data_generator(subject_gen, intro_subject_teacher_mail_gen, type_ ="subject", intent = "ask_subject_teacher_mail")
	subject_teacher_office_gen = Data_generator(subject_gen, intro_subject_teacher_office_gen, type_ = "subject", intent = "ask_subject_teacher_office")
	subject_teacher_name_gen = Data_generator(subject_gen, intro_subject_teacher_name_gen, type_="subject", intent = "ask_subject_teacher_name")
	#inform_teacher_gen = Data_generator(teacher_gen, intro_inform_teacher_gen, type_="teacher", intent="inform")
	#inform_subject_gen = Data_generator(subject_gen, intro_inform_subject_gen, type_="subject", intent="inform")

	common_examples.extend( teacher_mail_gen.get_examples(amount) )
	common_examples.extend( teacher_desk_gen.get_examples(amount) )
	common_examples.extend( subject_spots_gen.get_examples(amount) )
	common_examples.extend( subject_schedule_gen.get_examples(amount) )
	common_examples.extend( subject_classroom_gen.get_examples(amount) )
	common_examples.extend( subject_teacher_mail_gen.get_examples(amount) )
	common_examples.extend( subject_teacher_office_gen.get_examples(amount) )
	common_examples.extend( subject_teacher_name_gen.get_examples(amount) )
	#common_examples.extend( inform_teacher_gen.get_examples(amount) )
	#common_examples.extend( inform_subject_gen.get_examples(amount) )

	file_path = './Data/Dataset_{}.json'.format(language)

	result = {"rasa_nlu_data": {
					"regex_features": regex_features,
					"entity_synonyms": entity_synonyms,
					"common_examples": common_examples}
			 }
	print ( "Size of the dataset: {}".format(len(common_examples)))
	json_ = str(json.dumps(result, indent=2))
	file = open(file_path,"w")
	file.write(json_)
	file.close()


if __name__ == "__main__":
	language = input("Qué idioma quieres generar? (es/ca/en/all)\n")
	if not (language == 'ca' or language == 'es' or language == 'en' or language == 'all'):
		language = None
	amount = input("How many examples for each type? ")
	if amount:
		if language == 'all':
			main(int(amount), 'ca')
			main(int(amount), 'es')
			main(int(amount), 'en')
		else:main(int(amount), language)
	else: main(language)