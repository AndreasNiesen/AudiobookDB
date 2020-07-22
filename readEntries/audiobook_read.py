import tkinter as tk
from tkinter import messagebox
import mysql.connector
import datetime
import sys
import os
import psutil
from audiobook_classes import Author, Book

mysql_nfo = {
	'host':'',
	'user':'',
	'passwd':'',
	'database':'',
}

class sql_response_error(Exception):
	pass


class mainWindow(tk.Tk):
	def __init__(self, dbCursor, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.title("Read/Search Entry")
		self.geometry("1310x670")
		self.resizable(0, 0)

		self.dbCursor = dbCursor
		self.authors = {} #author_id: Author-instance
		self.books = {} #book_id: Book-instance

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for frameClass in (InitialFrame, AuthorFrame):
			frameName = frameClass.__name__
			frame = frameClass(parent=container, controller=self)
			self.frames[frameName] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.showFrame("InitialFrame")

	def showFrame(self, frameName):
		frame = self.frames[frameName]
		frame.tkraise()

	def europifyDate(self, date):
		dateList = str(date).split("-") # [year, month, day]
		return(f"{dateList[2]:2}.{dateList[1]:2}.{dateList[0]:4}")

	def loadAuthor(self, author):
		sql_query = f"SELECT audiobook_id FROM author_book WHERE author_id='{author.id}'"
		self.dbCursor.execute(sql_query)
		book_ids = []					#
		for infos in self.dbCursor:		# cannot have multiple requests with the same cursor
			book_ids.append(infos[0])	#
		for ids in book_ids:
			audio_buff = self.findAudioByID(ids)
			author.add_book(audio_buff)

	def loadBook(self, book):
		sql_query = f"SELECT author_id FROM author_book WHERE audiobook_id='{book.id}'"
		self.dbCursor.execute(sql_query)
		auth_ids = []
		for infos in self.dbCursor:
			auth_ids.append(infos[0])
		for ids in auth_ids:
			auth_buff = self.findAuthorByID(ids)
			book.add_author(auth_buff)
		sql_query = f"SELECT * FROM alternative_names WHERE audiobook_id='{book.id}'"
		for altName in self.dbCursor:
			book.add_alternativeInfo(altName)

	def findAuthorByID(self, authorID):
		if authorID in self.authors.keys():
			return self.authors[authorID]
		
		sql_query = f"SELECT * FROM author WHERE author_id=\"{authorID}\""
		self.dbCursor.execute(sql_query)
		for infos in self.dbCursor:
			try:
				self.authors[infos[0]] = Author(infos)
			except sql_response_error:
				print(f"Error adding Authors\nlackluster sql_response: {infos}")
		self.loadAuthor(self.authors[authorID])
		return self.authors[authorID]

	def findAuthorByName(self, authorNameArr):
		auth_rets = []
		authorName = " ".join(namePart for namePart in authorNameArr if namePart)

		for authorID in self.authors.keys():
			print(f"{authorName} vs {self.authors[authorID].full_name}")
			if self.authors[authorID].full_name == authorName:
				auth_rets.append(self.authors[authorID])
		if len(auth_rets) > 0:
			return auth_rets
		
		sql_query = f"SELECT * FROM author WHERE title=\"{authorNameArr[0]}\" AND name_first=\"{authorNameArr[1]}\" AND name_mid=\"{authorNameArr[2]}\" AND name_last=\"{authorNameArr[3]}\""
		print(sql_query)
		self.dbCursor.execute(sql_query)
		for infos in self.dbCursor:
			try:
				self.authors[infos[0]] = Author(infos)
				auth_rets.append(self.authors[infos[0]])
			except sql_response_error:
				print(f"Error adding Authors\nlackluster sql_response: {infos}")
		for auth in auth_rets:
			self.loadAuthor(auth)
		return auth_rets

	def findAudioByID(self, bookID):
		if bookID in self.books.keys():
			return self.books[bookID]
		
		sql_query = f"SELECT * FROM audiobooks WHERE audiobook_id=\"{bookID}\""
		self.dbCursor.execute(sql_query)
		for infos in self.dbCursor:
			try:
				self.books[infos[0]] = Book(infos)
			except sql_response_error:
				print(f"Error adding Books\nlackluster sql_response: {infos}")
		self.loadBook(self.books[bookID])
		return self.books[bookID]

	def findAudioByName(self, bookName):
		book_rets = []
		
		for audioID in self.books.keys():
			if self.books[audioID].name == bookName:
				book_rets.append(self.books[audioID])	
		if len(book_rets) > 0:
			return book_rets

		sql_query = f"SELECT * FROM audiobooks WHERE name=\"{bookName}\""
		self.dbCursor.execute(sql_query)
		for infos in self.dbCursor:
			try:
				self.books[infos[0]] = Book(infos)
				book_rets.append(self.books[infos[0]])
			except sql_response_error:
				print(f"Error adding Books\nlackluster sql_response: {infos}")
		for audio in book_rets:
			self.loadBook(audio)
		return book_rets


class AuthorFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		self.controller = controller
		self.dbCursor = controller.dbCursor
		self.authors = controller.authors
		self.books = controller.books

		self.nameLabel = tk.Label(self, text="Name:", anchor="nw", font="Arial, 14")
		self.nameLabel.place(x=90, y=75)
		self.nameInfoLabel = tk.Label(self, text="", anchor="nw", font="Arial, 12")
		self.nameInfoLabel.place(x=115, y=105)

		self.birthdayLabel = tk.Label(self, text="Geburtstag:", anchor="nw", font="Arial, 14")
		self.birthdayLabel.place(x=90, y=140)
		self.birthdayInfoLabel = tk.Label(self, text="", anchor="nw", font="Arial, 12")
		self.birthdayInfoLabel.place(x=115, y=170)

		self.deathdayLabel = tk.Label(self, text="Todestag:", anchor="nw", font="Arial, 14")
		self.deathdayLabel.place(x=90, y=205)
		self.deathdayInfoLabel = tk.Label(self, text="", anchor="nw", font="Arial, 12")
		self.deathdayInfoLabel.place(x=115, y=235)

		self.ageLabel = tk.Label(self, text="Alter:", anchor="nw", font="Arial, 14")
		self.ageLabel.place(x=90, y=270)
		self.ageInfoLabel = tk.Label(self, text="", anchor="nw", font="Arial, 12")
		self.ageInfoLabel.place(x=115, y=300)

		self.aliasesLabel = tk.Label(self, text="Aliase:", anchor="nw", font="Arial, 14")
		self.aliasesLabel.place(x=90, y=335)
		self.aliasesInfoLabel = tk.Label(self, text="", anchor="nw", font="Arial, 12")
		self.aliasesInfoLabel.place(x=115, y=365)

		self.booksLB = tk.Listbox(self, font="Arial, 10", width=33, height=20, relief="sunken")
		self.booksLB.place(x=450, y=80)
		self.booksLBYSB = tk.Scrollbar(self, takefocus=0, orient="vertical", command=self.booksLB.yview)
		self.booksLB.config(yscrollcommand=self.booksLBYSB.set)
		self.booksLBYSB.place(x=684, y=79, height=344)
		self.booksLBXSB = tk.Scrollbar(self, takefocus=0, orient="horizontal", command=self.booksLB.xview)
		self.booksLB.config(xscrollcommand=self.booksLBXSB.set)
		self.booksLBXSB.place(x=450, y=423, width=250)

		#DEBUG:
		self.testReset = tk.Button(self, text="reset", width=20, height=5, command=self.clearWidgets)
		self.testReset.place(x=650, y=550)
		self.testRead = tk.Button(self, text="read", width=20, height=5, command=self.readcur)
		self.testRead.place(x=800, y=550)
		self.testSearch = tk.Button(self, text="suche", width=20, height=5, command=self.searchFunc)
		self.testSearch.place(x=350, y=550)

	def searchFunc(self):
		titleStr = tk.StringVar()
		firstStr = tk.StringVar()
		midStr = tk.StringVar()
		lastStr = tk.StringVar()

		def go_search():
			authorName = [titleStr.get().strip(), firstStr.get().strip(), midStr.get().strip(), lastStr.get().strip()]
			go_on = False
			for part in authorName:
				if part == "":
					continue
				go_on = True

			if go_on:
				auth_insts = self.controller.findAuthorByName(authorName)
				if len(auth_insts) == 0:
					messagebox.showerror(title="No Result!", message="Kein Autor mit entsprechendem Namen gefunden.")
					top.lift(aboveThis=mainWnd)
				elif len(auth_insts) == 1:
					self.displayInfos(auth_insts[0])
					top.destroy()
				else:
					#DEBUG:
					print(auth_insts)
					self.displayInfos(auth_insts[1])
					top.destroy()
			else:
				messagebox.showerror(title="?!", message="Keines der Namensfelder ist ausgefüllt.")
				top.lift(aboveThis=mainWnd)
		
		top = tk.Toplevel()
		top.geometry(f"+400+300")
		top.title("Suche..")
		
		title = tk.Label(top, text="Titel: ", anchor="nw", font="Arial, 12")
		title.grid(row=0, column=0)
		tentry = tk.Entry(top, textvariable=titleStr, width=16, relief="sunken", font="Arial, 12")
		tentry.grid(row=0, column=1)

		first = tk.Label(top, text="Vorname: ", anchor="nw", font="Arial, 12")
		first.grid(row=1, column=0)
		fentry = tk.Entry(top, textvariable=firstStr, width=16, relief="sunken", font="Arial, 12")
		fentry.grid(row=1, column=1)
		
		mid = tk.Label(top, text="Mittelname: ", anchor="nw", font="Arial, 12")
		mid.grid(row=2, column=0)
		mentry = tk.Entry(top, textvariable=midStr, width=16, relief="sunken", font="Arial, 12")
		mentry.grid(row=2, column=1)

		last = tk.Label(top, text="Nachname: ", anchor="nw", font="Arial, 12")
		last.grid(row=3, column=0)
		lentry = tk.Entry(top, textvariable=lastStr, width=16, relief="sunken", font="Arial, 12")
		lentry.grid(row=3, column=1)

		searchbutton = tk.Button(top, text="Suchen", command=go_search)
		searchbutton.grid(row=4, columnspan=2)

	#DEBUG:
	def readcur(self):
		index = self.booksLB.curselection()
		if len(index) > 0:
			print(self.booksLB.get(index[0]))
			audios = self.controller.findAudioByName(self.booksLB.get(index[0]))
			for audio in audios:
				print(f"\"{audio.name}\"-Autoren:")
				for auth in audio:
					print(f"  {auth.full_name}")

	def displayInfos(self, auth):
		self.nameInfoLabel.config(text=auth.full_name)
		self.birthdayInfoLabel.config(text=self.controller.europifyDate(auth.birthday))
		age, alive = auth.get_age()
		if alive:
			self.deathdayInfoLabel.config(text=self.controller.europifyDate(auth.deathday))
		else: 
			self.deathdayInfoLabel.config(text="Lebendig")
		self.ageInfoLabel.config(text=int(age/365.25))
		if auth.aliases != "":
			self.aliasesInfoLabel.config(text=auth.aliases)
		else:
			self.aliasesInfoLabel.config(text="Keine Aliase vorhanden.")

		self.booksLB.delete(0, tk.END)
		for book in auth:
			self.booksLB.insert(tk.END, book.name)

	def clearWidgets(self):
		self.nameInfoLabel.config(text="")
		self.birthdayInfoLabel.config(text="")
		self.deathdayInfoLabel.config(text="")
		self.ageInfoLabel.config(text="")
		self.aliasesInfoLabel.config(text="")
		self.booksLB.delete(0, tk.END)


class MainFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		raise NotImplementedError


class InitialFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.dbCursor = controller.dbCursor

		self.preloadButton = tk.Button(self, text="Preload DB", font="Arial, 10", width=20, height=5, justify="center", command=self.db_preload, state="normal")
		self.preloadButton.place(x=380, y=150)
		self.preloadButton.bind("<Button-3>", self.preloadToggleInfo)
		self.noloadButton = tk.Button(self, text="Live Interaction", font="Arial, 10", width=20, height=5, justify="center", command=lambda:self.controller.showFrame("AuthorFrame"), state="normal")
		self.noloadButton.place(x=730, y=150)
		self.noloadButton.bind("<Button-3>", self.noloadToggleInfo)

	def preloadToggleInfo(self, event):
		txt_buff = self.preloadButton["text"]
		if "\n" not in txt_buff:
			txt_buff += "\n--\nlangsames laden\nschneller zugriff"
		elif "\n" in txt_buff:
			txt_buff = txt_buff.split("\n")[0]
		self.preloadButton.config(text=txt_buff)

	def noloadToggleInfo(self, event):
		txt_buff = self.noloadButton["text"]
		if "\n" not in txt_buff:
			txt_buff += "\n--\nschnelles laden\nlangsamer zugriff"
		elif "\n" in txt_buff:
			txt_buff = txt_buff.split("\n")[0]
		self.noloadButton.config(text=txt_buff)

	def db_preload(self):
		print(f'\nRSS usage Pre: {psutil.Process(os.getpid()).memory_info().rss:,} Bytes\n')

		self.preloadButton.config(state="disabled")

		loadingLabel = tk.Label(self, text="LOADING DATABASE INTO MEMORY..", font="Arial, 20")
		loadingLabel.place(x=400, y=300)
		
		sql_query = "SELECT * FROM author"
		self.dbCursor.execute(sql_query)
		for infos in self.dbCursor:
			try:
				self.controller.authors[infos[0]] = Author(infos)
			except sql_response_error:
				print(f"Error adding Authors\nlackluster sql_response: {infos}")

		sql_query = "SELECT * FROM audiobooks"
		self.dbCursor.execute(sql_query)
		for infos in self.dbCursor:
			try:
				self.controller.books[infos[0]] = Book(infos)
			except sql_response_error:
				print(f"Error adding Books\nlackluster sql_response: {infos}")

		for author_id in self.controller.authors:
			sql_query = f"SELECT audiobook_id FROM author_book WHERE author_id='{author_id}'"
			self.dbCursor.execute(sql_query)
			for book_ids in self.dbCursor:
				book_id = book_ids[0]
				self.controller.authors[author_id].add_book(self.controller.books[book_id])
				self.controller.books[book_id].add_author(self.controller.authors[author_id])

		for audiobook_id in self.controller.books:
			sql_query = f"SELECT * FROM alternative_names WHERE audiobook_id='{audiobook_id}'"
			self.dbCursor.execute(sql_query)
			for altName in self.dbCursor:
				#altName = [audiobook_id, altName, altYear, altComment]
				self.controller.books[audiobook_id].add_alternativeInfo(altName)

		loadingLabel.destroy()
		print(f'\nRSS usage Post: {psutil.Process(os.getpid()).memory_info().rss:,} Bytes\n')
		self.controller.showFrame("AuthorFrame")


if(__name__ == "__main__"):
	print("Connecting to Database...")
	try:
		dbConnection = mysql.connector.connect(host=mysql_nfo['host'], user=mysql_nfo['user'], passwd=mysql_nfo['passwd'], database=mysql_nfo['database'])
	except:
		print(" ".join(str(msg) for msg in sys.exc_info()))
		messagebox.showerror(title="ERROR!", message="Konnte nicht mit Datenbank verbinden.\nFehlermeldung steht in der Konsole.")
		sys.exit(0)
	print("Connection established!")
	dbCursor = dbConnection.cursor()

	mainWnd = mainWindow(dbCursor=dbCursor)
	mainWnd.mainloop()
	
	dbCursor.close()
	dbConnection.close()