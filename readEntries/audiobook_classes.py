import datetime

class Author():
	def __init__(self, sql_response):
		if len(sql_response) != 9:
			raise sql_response_error("sql_response enthält nicht genug Einträge um diese Author-Instantz zu füllen.")
		self.id = sql_response[0]
		self.name_array = sql_response[1:5] #name_array = [title, first_name, mid_names, last_name]
		self.birthday = sql_response[5]
		self.deathday = sql_response[6]
		self.aliases = sql_response[7]
		self.info_link = sql_response[8]
		self.books = [] #Book instance

	def __iter__(self):
		for book in self.books:
			yield book

	@property
	def full_name(self):
		return(" ".join(name_part for name_part in self.name_array if name_part))

	def get_age(self):
		"""
		returns days_alive as int and is_alive as bool
		days_alive 0, if birthday unknown
		"""
		if(self.birthday == datetime.date(1,1,1)): #0001-01-01 is a standin for unknown date in database
			if(self.deathday == datetime.date(1,1,1)):
				return(0, True)
			else:
				return(0, False)
		elif(self.deathday == datetime.date(1,1,1)):
			return((datetime.datetime.now().date() - self.birthday).days, True)
		else:
			return((self.deathday - self.birthday).days, False)

	def add_book(self, new_book):
		#new_book = instance of book-class
		for book in self.books:
			if (new_book.id == book.id):
				return(False, "Books ID already in Booklist")
		self.books.append(new_book)
		return(True, None)

	def add_books_list(self, new_books):
		#new_books = [Book]
		#skips already known books
		prev_known = 0
		for book in new_books:
			success, error = self.add_book(book)
			if not success:
				if error == "Books ID already in Booklist":
					prev_known += 1
				else:
					return(False, error)
		return(True, str(prev_known)) #str(prev_known) to keep return-types equal

class Book():
	def __init__(self, sql_response):
		if len(sql_response) != 16:
			raise sql_response_error("sql_response enthält nicht genug Einträge um diese Book-Instantz zu füllen.")
		self.id = sql_response[0]
		self.name = sql_response[1]
		self.release = {}
		self.release["original"] = sql_response[2]
		self.release["germany"] = sql_response[3]
		self.release["audiobook"] = sql_response[4]
		self.synopsis = sql_response[5]
		self.roman = sql_response[6] #True = roman, False = shortstory
		self.shortened = sql_response[7]
		self.boxset = sql_response[8]
		self.boxname = sql_response[9]
		self.mp3CD = sql_response[10]
		self.PConly = sql_response[11]
		self.amountCDs = sql_response[12]
		self.genre = sql_response[13]
		self.comments = sql_response[14]
		self.runtime = sql_response[15]
		self.authors = []
		self.altNames = {} # {altName: [altYear, altComment]}

	def __iter__(self):
		for author in self.authors:
			yield author

	def add_alternativeInfo(self, sql_response):
		self.altNames[sql_response[1]] = [sql_response[2], sql_response[3]]

	def add_author(self, new_author):
		for author in self.authors:
			if author.full_name == new_author.full_name:
				return(False, "Author already in Authorlist")
		self.authors.append(new_author)
		return(True, None)

	def add_authors_list(self, authors_list):
		prev_known = 0
		for author in authors_list:
			success, error = self.add_author(author)
			if not success:
				if error == "Author already in Authorlist":
					prev_known += 1
				else:
					return(False, error)
		return(True, str(prev_known))


#TODO:
#	VAs
#	Roles