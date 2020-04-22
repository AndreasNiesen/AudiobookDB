import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sys

mysql_host = ''  # 'localhost' or IP (f.e. '192.168.123.21')
mysql_port = 3306
mysql_user = ''
mysql_pw = ''
mysql_db = ''

class mainWindow():
	def __init__(self, parent, dbConnection, dbCursor):
		self.parent = parent
		self.parent.title("Create Entry")
		self.parent.geometry("1310x670")
		self.parent.resizable(0, 0)

		self.dbConnection = dbConnection
		self.dbCursor = dbCursor

		self.forbidden_chars = ["\\", "'", '"'] #blacklist chars problematic for mysql query if necessary

		self.authorTitle = tk.StringVar()
		self.authorFirstName = tk.StringVar()
		self.authorMidNames = tk.StringVar()
		self.authorLastName = tk.StringVar()
		self.authorBDayDate = tk.StringVar()
		self.authorDeathDate = tk.StringVar()
		self.authorAlias = tk.StringVar()
		self.authorInfoLink = tk.StringVar()
		self.authorsListDict = []

		self.audiobookName = tk.StringVar()
		self.audiobookReleaseOriginal = tk.StringVar()
		self.audiobookReleaseGer = tk.StringVar()
		self.audiobookReleaseAudio = tk.StringVar()
		self.audiobookIsRoman = tk.IntVar()
		self.audiobookIsRoman.set(1)
		self.audiobookIsShortened = tk.IntVar()
		self.audiobookIsShortened.set(0)
		self.audiobookIsBox = tk.IntVar()
		self.audiobookIsBox.set(0)
		self.audiobookBoxName = tk.StringVar()
		self.audiobookIsMp3CD = tk.IntVar()
		self.audiobookIsMp3CD.set(0)
		self.audiobookIsPcOnly = tk.IntVar()
		self.audiobookIsPcOnly.set(0)
		self.audiobookGenre = tk.StringVar()
		self.audiobookAmountCDs = tk.StringVar()
		self.audiobookRuntime = tk.StringVar()

		self.reader_roleComments = tk.StringVar()
		self.reader_roleVATitle = tk.StringVar()
		self.reader_roleVAFirstName = tk.StringVar()
		self.reader_roleVAMidName = tk.StringVar()
		self.reader_roleVALastName = tk.StringVar()
		self.reader_roleRoleTitle = tk.StringVar()
		self.reader_roleRoleFirstName = tk.StringVar()
		self.reader_roleRoleMidName = tk.StringVar()
		self.reader_roleRoleLastName = tk.StringVar()
		self.reader_roleIsMain = tk.IntVar()
		self.reader_roleIsMain.set(0)
		self.reader_roleIsHelper = tk.IntVar()
		self.reader_roleIsHelper.set(0)
		self.reader_roleVAvsRole = tk.IntVar()
		self.reader_roleVAvsRole.set(0)
		#self.showVARolePairText
		self.VARoleListDict = []

		self.remainderAltName = tk.StringVar()
		self.remainderAltYear = tk.StringVar()
		self.remainderAltComment = tk.StringVar()
		#self.remainderSynopsisText
		#self.remainderCommentsText
		#self.remainderAltText
		self.altListDict = []

		#=================================================================================================

		self.authorLabel = tk.Label(self.parent, text="Autor:", anchor="nw", font="Arial, 14")
		self.authorLabel.place(x=30, y=20)
		self.borderAuthorLabel = tk.Label(self.parent, text="", relief="groove", height=36, width=40)
		self.borderAuthorLabel.place(x=30, y=55)

		self.authorTitleLabel = tk.Label(self.parent, text="Titel:", anchor="nw", font="Arial, 10")
		self.authorTitleLabel.place(x=40, y=75)
		self.authorTitleEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.authorTitle, width=16, relief="sunken")
		self.authorTitleEntry.place(x=47, y=105)
		self.authorTitleEntry.bind("<Key>", self.limitInputAll)

		self.authorFirstNameLabel = tk.Label(self.parent, text="Vorname:", anchor="nw", font="Arial, 10")
		self.authorFirstNameLabel.place(x=160, y=75)
		self.authorFirstNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.authorFirstName, width=18, relief="sunken")
		self.authorFirstNameEntry.place(x=167, y=105)
		self.authorFirstNameEntry.bind("<Key>", self.limitInputAll)

		self.authorMidNamesLabel = tk.Label(self.parent, text="Mittlere Namen:", anchor="nw", font="Arial, 10")
		self.authorMidNamesLabel.place(x=40, y=140)
		self.authorMidNamesEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.authorMidNames, width=35, relief="sunken")
		self.authorMidNamesEntry.place(x=47, y=170)
		self.authorMidNamesEntry.bind("<Key>", self.limitInputAll)

		self.authorLastNameLabel = tk.Label(self.parent, text="Nachname:", anchor="nw", font="Arial, 10")
		self.authorLastNameLabel.place(x=40, y=205)
		self.authorLastNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.authorLastName, width=35, relief="sunken")
		self.authorLastNameEntry.place(x=47, y=235)
		self.authorLastNameEntry.bind("<Key>", self.limitInputAll)

		self.authorBDayDateLabel = tk.Label(self.parent, text="Geburtsdatum:", anchor="nw", font="Arial, 10")
		self.authorBDayDateLabel.place(x=40, y=270)
		self.authorBDayDateEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.authorBDayDate, width=16, relief="sunken")
		self.authorBDayDateEntry.bind("<Key>", self.limitInputDate)
		self.authorBDayDateEntry.place(x=47, y=300)

		self.authorDeathDateLabel = tk.Label(self.parent, text="Todesdatum:", anchor="nw", font="Arial, 10")
		self.authorDeathDateLabel.place(x=160, y=270)
		self.authorDeathDateEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.authorDeathDate, width=18, relief="sunken")
		self.authorDeathDateEntry.bind("<Key>", self.limitInputDate)
		self.authorDeathDateEntry.place(x=167, y=300)

		self.authorAliasLabel = tk.Label(self.parent, text="Alias:", anchor="nw", font="Arial, 10")
		self.authorAliasLabel.place(x=40, y=335)
		self.authorAliasEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.authorAlias, width=35, relief="sunken")
		self.authorAliasEntry.place(x=47, y=365)
		self.authorAliasEntry.bind("<Key>", self.limitInputAll)

		self.authorInfoLabel = tk.Label(self.parent, text="Info Link:", anchor="nw", font="Arial, 10")
		self.authorInfoLabel.place(x=40, y=400)
		self.authorInfoEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.authorInfoLink, width=35, relief="sunken")
		self.authorInfoEntry.place(x=47, y=430)
		self.authorInfoEntry.bind("<Key>", self.limitInputAll)

		self.authorAddAuthorButton = tk.Button(self.parent, text="Weit.\nAutor", font="Arial, 10", width=5, height=6, justify="right", command=self.addAuthor)
		self.authorAddAuthorButton.place(x=40, y=470)

		self.authorAuthorsText = tk.Text(self.parent, font="Arial, 10", width=25, height=8, relief="sunken", state="disabled")
		self.authorAuthorsText.place(x=95, y=460)
		self.yscrollAuthorsSBar = tk.Scrollbar(self.parent, takefocus=0, orient="vertical", command=self.authorAuthorsText.yview)
		self.authorAuthorsText.config(yscrollcommand=self.yscrollAuthorsSBar.set)
		self.yscrollAuthorsSBar.place(x=274, y=460, height=132)

		#=================================================================================================

		self.audiobookLabel = tk.Label(self.parent, text="Hörbuch:", anchor="nw", font="Arial, 14")
		self.audiobookLabel.place(x=350, y=20)
		self.borderAudiobookLabel = tk.Label(self.parent, text="", relief="groove", height=36, width=40)
		self.borderAudiobookLabel.place(x=350, y=55)

		self.audiobookNameLabel = tk.Label(self.parent, text="Name:", anchor="nw", font="Arial, 10")
		self.audiobookNameLabel.place(x=360, y=75)
		self.audiobookNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.audiobookName, width=35, relief="sunken")
		self.audiobookNameEntry.place(x=367, y=105)
		self.audiobookNameEntry.bind("<Key>", self.limitInputAll)

		self.audiobookReleaseOriginalLabel = tk.Label(self.parent, text="Erschienen (Original):", anchor="nw", font="Arial, 10")
		self.audiobookReleaseOriginalLabel.place(x=360, y=140)
		self.audiobookReleaseOriginalEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.audiobookReleaseOriginal, width=35, relief="sunken")
		self.audiobookReleaseOriginalEntry.bind("<Key>", self.limitInputDate)
		self.audiobookReleaseOriginalEntry.place(x=367, y=170)

		self.audiobookReleaseGerLabel = tk.Label(self.parent, text="Erschienen (Deutschland):", anchor="nw", font="Arial, 10")
		self.audiobookReleaseGerLabel.place(x=360, y=205)
		self.audiobookReleaseGerEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.audiobookReleaseGer, width=35, relief="sunken")
		self.audiobookReleaseGerEntry.bind("<Key>", self.limitInputDate)
		self.audiobookReleaseGerEntry.place(x=367, y=235)

		self.audiobookReleaseAudioLabel = tk.Label(self.parent, text="Erschienen (Audiobuch):", anchor="nw", font="Arial, 10")
		self.audiobookReleaseAudioLabel.place(x=360, y=270)
		self.audiobookReleaseAudioEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.audiobookReleaseAudio, width=35, relief="sunken")
		self.audiobookReleaseAudioEntry.bind("<Key>", self.limitInputDate)
		self.audiobookReleaseAudioEntry.place(x=367, y=300)

		self.audiobookIsRomanRButton = tk.Radiobutton(self.parent, text="Roman", variable=self.audiobookIsRoman, value=1, font="Arial, 10")
		self.audiobookIsShortRButton = tk.Radiobutton(self.parent, text="KurzG", variable=self.audiobookIsRoman, value=0, font="Arial, 10")
		self.audiobookIsRomanRButton.place(x=360, y=335)
		self.audiobookIsShortRButton.place(x=360, y=355)
		self.audiobookIsShortenedChButton = tk.Checkbutton(self.parent, text="Gekürzt", variable=self.audiobookIsShortened, onvalue=1, offvalue=0, font="Arial, 10")
		self.audiobookIsBoxChButton = tk.Checkbutton(self.parent, text="Boxset", variable=self.audiobookIsBox, onvalue=1, offvalue=0, font="Arial, 10", command=self.changeBoxNameState)
		self.audiobookIsShortenedChButton.place(x=450, y=335)
		self.audiobookIsBoxChButton.place(x=450, y=355)
		self.audiobookIsMp3CDChButton = tk.Checkbutton(self.parent, text="Mp3 CD", variable=self.audiobookIsMp3CD, onvalue=1, offvalue=0, font="Arial, 10")
		self.audiobookIsPcOnlyChButton = tk.Checkbutton(self.parent, text="Nur PC", variable=self.audiobookIsPcOnly, onvalue=1, offvalue=0, font="Arial, 10")
		self.audiobookIsMp3CDChButton.place(x=540, y=335)
		self.audiobookIsPcOnlyChButton.place(x=540, y=355)

		self.audiobookBoxNameLabel = tk.Label(self.parent, text="Box:", anchor="nw", font="Arial, 10")
		self.audiobookBoxNameLabel.place(x=360, y=385)
		self.audiobookBoxNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.audiobookBoxName, width=35, relief="sunken", state="disabled")
		self.audiobookBoxNameEntry.place(x=367, y=415)
		self.audiobookBoxNameEntry.bind("<Key>", self.limitInputAll)

		self.audiobookGenreLabel = tk.Label(self.parent, text="Genre:", anchor="nw", font="Arial, 10")
		self.audiobookGenreLabel.place(x=360, y=450)
		self.audiobookGenreEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.audiobookGenre, width=35, relief="sunken")
		self.audiobookGenreEntry.place(x=367, y=480)
		self.audiobookGenreEntry.bind("<Key>", self.limitInputAll)

		self.audiobookAmountCDsLabel = tk.Label(self.parent, text="Anzahl CDs:", anchor="nw", font="Arial, 10")
		self.audiobookAmountCDsLabel.place(x=360, y=515)
		self.audiobookRuntimeLabel = tk.Label(self.parent, text="Laufzeit:", anchor="nw", font="Arial, 10")
		self.audiobookRuntimeLabel.place(x=480, y=515)
		self.audiobookAmountCDsEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.audiobookAmountCDs, width=10, relief="sunken", justify="right")
		self.audiobookAmountCDsEntry.bind("<Key>", self.limitInputDigits)
		self.audiobookAmountCDsEntry.place(x=367, y=545)
		self.audiobookRuntimeEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.audiobookRuntime, width=10, relief="sunken", justify="right")
		self.audiobookRuntimeEntry.bind("<Key>", self.limitInputTime)
		self.audiobookRuntimeEntry.place(x=487, y=545)

		#=================================================================================================

		self.reader_roleLabel = tk.Label(self.parent, text="Leser und Rollen:", anchor="nw", font="Arial, 14")
		self.reader_roleLabel.place(x=670, y=20)
		self.borderReader_roleLabel = tk.Label(self.parent, text="", relief="groove", height=36, width=40)
		self.borderReader_roleLabel.place(x=670, y=55)

		self.borderAudiobookLabel = tk.Label(self.parent, text="", relief="groove", height=1, width=20)
		self.borderAudiobookLabel.place(x=680, y=85)
		self.borderAudioplayLabel = tk.Label(self.parent, text="", relief="groove", height=1, width=12)
		self.borderAudioplayLabel.place(x=850, y=85)

		self.reader_roleBookLabel = tk.Label(self.parent, text="Hörbuch", anchor="nw", font="Arial, 10")
		self.reader_roleBookLabel.place(x=724, y=68)
		self.reader_rolePlayLabel = tk.Label(self.parent, text="Hörspiel", anchor="nw", font="Arial, 10")
		self.reader_rolePlayLabel.place(x=868, y=68)

		self.reader_roleVARButton = tk.Radiobutton(self.parent, text="Leser\t\t", font="Arial, 10", variable=self.reader_roleVAvsRole, value=0, command=self.changeVARoleState)
		self.reader_roleRoleRButton = tk.Radiobutton(self.parent, text="Rolle", font="Arial, 10", variable=self.reader_roleVAvsRole, value=1, command=self.changeVARoleState)
		self.reader_roleVARoleRButton = tk.Radiobutton(self.parent, text="Leser/Rolle", font="Arial, 10", variable=self.reader_roleVAvsRole, value=2, command=self.changeVARoleState)
		self.reader_roleVARButton.place(x=680 ,y=90)
		self.reader_roleRoleRButton.place(x=770 ,y=90)
		self.reader_roleVARoleRButton.place(x=850 ,y=90)

		self.reader_roleVATitleLabel = tk.Label(self.parent, text="Leser Titel:", anchor="nw", font="Arial, 10")
		self.reader_roleVATitleLabel.place(x=680, y=120)
		self.reader_roleVATitleEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.reader_roleVATitle, width=16, relief="sunken")
		self.reader_roleVATitleEntry.place(x=687, y=150)
		self.reader_roleVATitleEntry.bind("<Key>", self.limitInputAll)

		self.reader_roleVAFirstNameLabel = tk.Label(self.parent, text="Leser Vorname:", anchor="nw", font="Arial, 10")
		self.reader_roleVAFirstNameLabel.place(x=680, y=185)
		self.reader_roleVAFirstNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.reader_roleVAFirstName, width=16, relief="sunken")
		self.reader_roleVAFirstNameEntry.place(x=687, y=215)
		self.reader_roleVAFirstNameEntry.bind("<Key>", self.limitInputAll)

		self.reader_roleVAMidNameLabel = tk.Label(self.parent, text="Leser Mit. Namen:", anchor="nw", font="Arial, 10")
		self.reader_roleVAMidNameLabel.place(x=680, y=250)
		self.reader_roleVAMidNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.reader_roleVAMidName, width=16, relief="sunken")
		self.reader_roleVAMidNameEntry.place(x=687, y=280)
		self.reader_roleVAMidNameEntry.bind("<Key>", self.limitInputAll)

		self.reader_roleVALastNameLabel = tk.Label(self.parent, text="Leser Nachname:", anchor="nw", font="Arial, 10")
		self.reader_roleVALastNameLabel.place(x=680, y=315)
		self.reader_roleVALastNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.reader_roleVALastName, width=16, relief="sunken")
		self.reader_roleVALastNameEntry.place(x=687, y=345)
		self.reader_roleVALastNameEntry.bind("<Key>", self.limitInputAll)

		self.reader_roleRoleTitleLabel = tk.Label(self.parent, text="Rolle Job/Title:", anchor="nw", font="Arial, 10")
		self.reader_roleRoleTitleLabel.place(x=800, y=120)
		self.reader_roleRoleTitleEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.reader_roleRoleTitle, width=16, relief="sunken", state="disabled")
		self.reader_roleRoleTitleEntry.place(x=807, y=150)
		self.reader_roleRoleTitleEntry.bind("<Key>", self.limitInputAll)

		self.reader_roleRoleFirstNameLabel = tk.Label(self.parent, text="Rolle Vorname:", anchor="nw", font="Arial, 10")
		self.reader_roleRoleFirstNameLabel.place(x=800, y=185)
		self.reader_roleRoleFirstNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.reader_roleRoleFirstName, width=16, relief="sunken", state="disabled")
		self.reader_roleRoleFirstNameEntry.place(x=807, y=215)
		self.reader_roleRoleFirstNameEntry.bind("<Key>", self.limitInputAll)

		self.reader_roleRoleMidNameLabel = tk.Label(self.parent, text="Rolle Mit. Namen:", anchor="nw", font="Arial, 10")
		self.reader_roleRoleMidNameLabel.place(x=800, y=250)
		self.reader_roleRoleMidNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.reader_roleRoleMidName, width=16, relief="sunken", state="disabled")
		self.reader_roleRoleMidNameEntry.place(x=807, y=280)
		self.reader_roleRoleMidNameEntry.bind("<Key>", self.limitInputAll)

		self.reader_roleRoleLastNameLabel = tk.Label(self.parent, text="Rolle Nachname:", anchor="nw", font="Arial, 10")
		self.reader_roleRoleLastNameLabel.place(x=800, y=315)
		self.reader_roleRoleLastNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.reader_roleRoleLastName, width=16, relief="sunken", state="disabled")
		self.reader_roleRoleLastNameEntry.place(x=807, y=345)
		self.reader_roleRoleLastNameEntry.bind("<Key>", self.limitInputAll)

		self.reader_roleIsMainChButton = tk.Checkbutton(self.parent, text="Hauptperson", variable=self.reader_roleIsMain, onvalue=1, offvalue=0, font="Arial, 10", command=self.uncheckIsHelper, state="disabled")
		self.reader_roleIsHelperChButton = tk.Checkbutton(self.parent, text="Weiterer Charakter", variable=self.reader_roleIsHelper, onvalue=1, offvalue=0, font="Arial, 10", command=self.uncheckIsMain, state="disabled")
		self.reader_roleIsMainChButton.place(x=807, y=382)
		self.reader_roleIsHelperChButton.place(x=807, y=405)

		self.reader_roleAddRoleButton = tk.Button(self.parent, justify="center", text="Leser\nHinzufügen", width=16, height=2, command=self.addRoleVAPair)
		self.reader_roleAddRoleButton.place(x=680, y=385)

		self.showVARolePairText = tk.Text(self.parent, font="Arial, 10", width=32, height=9, state="disabled", padx=3, pady=2)
		self.showVARolePairText.place(x=682, y=440)
		self.yscrollVARolePairSBar = tk.Scrollbar(self.parent, orient="vertical", takefocus=0, command=self.showVARolePairText.yview)
		self.showVARolePairText.config(yscrollcommand=self.yscrollVARolePairSBar.set)
		self.yscrollVARolePairSBar.place(x=914, y=440, height=150)

	#=====================================================================================================

		self.remainderLabel = tk.Label(self.parent, text="Weiteres:", anchor="nw", font="Arial, 14")
		self.remainderLabel.place(x=990, y=20)
		self.borderRemainderLabel = tk.Label(self.parent, text="", relief="groove", height=36, width=40)
		self.borderRemainderLabel.place(x=990, y=55)

		self.remainderSynopsisLabel = tk.Label(self.parent, text="Zusammenfassung:", anchor="nw", font="Arial, 10")
		self.remainderSynopsisLabel.place(x=1000, y=65)
		self.remainderSynopsisText = tk.Text(self.parent, font="Arial, 10", width=32, height=7, relief="sunken", padx=3, pady=2)
		self.remainderSynopsisText.place(x=1007, y=95)
		self.yscrollSynopsisSBar = tk.Scrollbar(self.parent, orient="vertical", takefocus=0, command=self.remainderSynopsisText.yview)
		self.remainderSynopsisText.config(yscrollcommand=self.yscrollSynopsisSBar.set)
		self.yscrollSynopsisSBar.place(x=1239, y=95, height=118)
		self.remainderSynopsisText.bind("<Key>", self.limitTextBox)

		self.remainderCommentsLabel = tk.Label(self.parent, text="Kommentare:", anchor="nw", font="Arial, 10")
		self.remainderCommentsLabel.place(x=1000, y=225)
		self.remainderCommentsText = tk.Text(self.parent, font="Arial, 10", width=32, height=7, relief="sunken", padx=3, pady=2)
		self.remainderCommentsText.place(x=1007, y=255)
		self.yscrollCommentsSBar = tk.Scrollbar(self.parent, orient="vertical", takefocus=0, command=self.remainderCommentsText.yview)
		self.remainderCommentsText.config(yscrollcommand=self.yscrollCommentsSBar.set)
		self.yscrollCommentsSBar.place(x=1239, y=255, height=118)
		self.remainderCommentsText.bind("<Key>", self.limitTextBox)

		self.remainderAltNameLabel = tk.Label(self.parent, text="Alt. Name:", anchor="nw", font="Arial, 10")
		self.remainderAltNameLabel.place(x=1000, y=385)
		self.remainderAltNameEntry = tk.Entry(self.parent, font="Arial, 10", textvariable=self.remainderAltName, width=16, relief="sunken")
		self.remainderAltNameEntry.place(x=1007, y=415)
		self.remainderAltNameEntry.bind("<Key>", self.limitInputAll)

		self.remainderAltYearLabel = tk.Label(self.parent, text="Alt. Jahr:", anchor="nw", font="Arial, 10")
		self.remainderAltYearLabel.place(x=1120, y=385)
		self.remainderAltYearEntry = tk.Entry(self.parent, font="Arial, 10", relief="sunken", textvariable=self.remainderAltYear, width=18)
		self.remainderAltYearEntry.place(x=1127, y=415)
		self.remainderAltYearEntry.bind("<Key>", self.limitInputDigits)

		self.remainderAltCommentLabel = tk.Label(self.parent, text="Alt. Bemerkung:", anchor="nw", font="Arial, 10")
		self.remainderAltCommentLabel.place(x=1000, y=445)
		self.remainderAltCommentEntry = tk.Entry(self.parent, font="Arial, 10", relief="sunken", width=35, textvariable=self.remainderAltComment)
		self.remainderAltCommentEntry.place(x=1007, y=475)
		self.remainderAltCommentEntry.bind("<Key>", self.limitInputAll)

		self.remainderAddAltButton = tk.Button(self.parent, justify="center", font="Arial, 10", text="Weit.\nAlt.", height=3, width=5, command=self.addAltInfos)
		self.remainderAddAltButton.place(x=1000, y=517)

		self.remainderAltText = tk.Text(self.parent, font="Arial, 10", width=25, height=5, relief="sunken", padx=3, pady=2, state="disabled")
		self.remainderAltText.place(x=1055, y=505)
		self.yscrollAltSBar = tk.Scrollbar(self.parent, orient="vertical", takefocus=0, command=self.remainderAltText.yview)
		self.remainderAltText.config(yscrollcommand=self.yscrollAltSBar.set)
		self.yscrollAltSBar.place(x=1238, y=505, height=86)

	#=====================================================================================================

		self.addToDBButton = tk.Button(self.parent, justify="center", font="Arial, 10", text="Zur Datenbank\nHinzufügen", height=2, width=15, command=self.checkAllEntries)
		self.addToDBButton.place(x=590, y=615)

	#=====================================================================================================

	def dateFormatter(self, inp_date):
		#- . / : \
		if("-" in inp_date):
			buff = inp_date.split("-")
			#input will be day month year
			#mysql wants is year month date
			return(f"{buff[2]}-{buff[1]}-{buff[0]}")
		elif("." in inp_date):
			buff = inp_date.split(".")
			return(f"{buff[2]}-{buff[1]}-{buff[0]}")
		elif("/" in inp_date):
			buff = inp_date.split("/")
			return(f"{buff[2]}-{buff[1]}-{buff[0]}")
		elif(":" in inp_date):
			buff = inp_date.split(":")
			return(f"{buff[2]}-{buff[1]}-{buff[0]}")
		elif("\\" in inp_date):
			buff = inp_date.split("\\")
			return(f"{buff[2]}-{buff[1]}-{buff[0]}")
		else:
			if(len(inp_date) != 4):
				messagebox.showerror(title="ERROR!", message=f"Datum falsch!\n'{inp_date}'")
			return(f"{inp_date}-01-01")

	def timeFormatter(self, inp_time):
		#inp_time should be "HH:MM"
		#or "HH.MM" or everything in minutes
		#for mysql make it "HH:MM:SS"
		if(":" in inp_time):
			inp_time += ":00"
			return(inp_time)
		if("." in inp_time):
			inp_time.replace(".", ":")
			inp_time += ":00"
			return(inp_time)
		if("." not in inp_time and ":" not in inp_time):
			hour = str(int(int(inp_time)/60))
			minutes = (int(inp_time)%60)
			return(f"{hour}:{minutes}:00")

	def logError(self, error_msg):
		with open("ErrorLog.txt", "a+") as f:
			f.write(error_msg)
			f.close()
		messagebox.showerror(title="Error!", message="Fehler wurde im ErrorLog vermerkt.\nBitte den zuständigen Nerd kontaktieren!")

	def exeQuery(self, query, commit=False):
		error_msg = ""
		try:
			self.dbCursor.execute(query)
			if(commit):
				self.dbConnection.commit()
		except:
			error_msg = " ".join(str(msg) for msg in sys.exc_info())
			error_msg += "\n"
			self.logError(error_msg)

	def checkAllEntries(self):
		sql_query = ""
		ret_vals = []
		author_ids = []
		audiobook_id = 0
		va_roles_ids = {}

		#=====================================================================================================
		
		if(not self.authorsListDict):
			messagebox.showerror(title="No Authors!", message="Bisher wurde kein\nAutor hinzugefügt.")
			return False
		for auth_dict in self.authorsListDict:
			ret_vals = []
			sql_query = "SELECT author_id FROM author WHERE name_first='"
			sql_query += auth_dict["First"] if "First" in auth_dict.keys() else ""
			sql_query += "' AND name_mid='"
			sql_query += auth_dict["Mid"] if "Mid" in auth_dict.keys() else ""
			sql_query += "' AND name_last='"
			sql_query += auth_dict["Last"] if "Last" in auth_dict.keys() else ""
			sql_query += "'"
			self.exeQuery(sql_query, False)
			for vals in self.dbCursor:
				ret_vals.append(vals)
			if not ret_vals:
				sql_query = "INSERT INTO author (title, name_first, name_mid, name_last, date_birth, date_death, alias, info_link) VALUES ("
				sql_query += "'" + auth_dict["Title"] + "', " if "Title" in auth_dict.keys() else "'', "
				sql_query += "'" + auth_dict["First"] + "', " if "First" in auth_dict.keys() else "'', "
				sql_query += "'" + auth_dict["Mid"] + "', " if "Mid" in auth_dict.keys() else "'', "
				sql_query += "'" + auth_dict["Last"] + "', " if "Last" in auth_dict.keys() else "'', "
				sql_query += "'" + self.dateFormatter(auth_dict["BDay"]) + "', " if "BDay" in auth_dict.keys() else "'0001-01-01', "
				sql_query += "'" + self.dateFormatter(auth_dict["DDate"]) + "', " if "DDate" in auth_dict.keys() else "'0001-01-01', "
				sql_query += "'" + auth_dict["Alias"] + "', " if "Alias" in auth_dict.keys() else "'', "
				sql_query += "'" + auth_dict["Nfo"] + "')" if "Nfo" in auth_dict.keys() else "'')"
				self.exeQuery(sql_query, True)

				sql_query = "SELECT LAST_INSERT_ID()"
				self.exeQuery(sql_query, False)
				for vals in self.dbCursor:
					ret_vals.append(vals)
			author_ids.append(int(ret_vals[0][0]))
		
		#=====================================================================================================

		ret_vals = []
		sql_query = "INSERT INTO audiobooks (name, release_original, release_germany, release_audio, synopsis, isRoman, isShortened, isInBox, boxName, isMp3CD, isPCOnly, amountCDs, genre, comments, runtime) VALUES ("
		sql_query += "'" + self.audiobookName.get() + "', "
		sql_query += "'" + self.dateFormatter(self.audiobookReleaseOriginal.get()) + "', " if self.audiobookReleaseOriginal.get() != "" else "NULL, "
		sql_query += "'" + self.dateFormatter(self.audiobookReleaseGer.get()) + "', " if self.audiobookReleaseGer.get() != "" else "NULL, "
		sql_query += "'" + self.dateFormatter(self.audiobookReleaseAudio.get()) + "', " if self.audiobookReleaseAudio.get() != "" else "NULL, "
		sql_query += "'" + self.remainderSynopsisText.get("1.0", tk.END) + "', "
		sql_query += "TRUE, " if self.audiobookIsRoman.get()==1 else "FALSE, "
		sql_query += "TRUE, " if self.audiobookIsShortened.get()==1 else "FALSE, "
		sql_query += "TRUE, " if self.audiobookIsBox.get()==1 else "FALSE, "
		sql_query += "'" + self.audiobookBoxName.get() + "', "
		sql_query += "TRUE, " if self.audiobookIsMp3CD.get()==1 else "FALSE, "
		sql_query += "TRUE, " if self.audiobookIsPcOnly.get()==1 else "FALSE, "
		sql_query += "'" + self.audiobookAmountCDs.get() + "', "
		sql_query += "'" + self.audiobookGenre.get() + "', "
		sql_query += "'" + self.remainderCommentsText.get("1.0", tk.END) + "', "
		sql_query += "'" + self.timeFormatter(self.audiobookRuntime.get()) + "')"
		self.exeQuery(sql_query, True)

		sql_query = "SELECT LAST_INSERT_ID()"
		self.exeQuery(sql_query, False)
		for vals in self.dbCursor:
			ret_vals.append(vals)
		audiobook_id = int(ret_vals[0][0])

		#=====================================================================================================

		if(not self.VARoleListDict):
			messagebox.showerror(title="No VA/Role!", message="Bisher wurden weder\nLeser noch Rolle hinzugefügt.")
			return False
		buff = " ".join(key for key in self.VARoleListDict[0].keys()) #trusting user might end up bad
		if("VA" in buff and "Role" in buff):
			for vaRole_dict in self.VARoleListDict:
				# Check if VA already exists, otherwise add VA
				va_id = 0
				ret_vals = []
				sql_query = "SELECT voice_id FROM voice_artists WHERE name_first='"
				sql_query += vaRole_dict["VAFirst"] if "VAFirst" in vaRole_dict.keys() else ""
				sql_query += "' AND name_mid='"
				sql_query += vaRole_dict["VAMid"] if "VAMid" in vaRole_dict.keys() else ""
				sql_query += "' AND name_last='"
				sql_query += vaRole_dict["VALast"] if "VALast" in vaRole_dict.keys() else ""
				sql_query += "'"
				self.exeQuery(sql_query, False)
				for vals in self.dbCursor:
					ret_vals.append(vals)
				if(not ret_vals):
					sql_query = "INSERT INTO voice_artists (title, name_first, name_mid, name_last) VALUES ("
					sql_query += "'" + vaRole_dict["VATitle"] + "', " if "VATitle" in vaRole_dict.keys() else "'', "
					sql_query += "'" + vaRole_dict["VAFirst"] + "', " if "VAFirst" in vaRole_dict.keys() else "'', "
					sql_query += "'" + vaRole_dict["VAMid"] + "', " if "VAMid" in vaRole_dict.keys() else "'', "
					sql_query += "'" + vaRole_dict["VALast"] + "')" if "VALast" in vaRole_dict.keys() else "'')"
					self.exeQuery(sql_query, True)

					sql_query = "SELECT LAST_INSERT_ID()"
					self.exeQuery(sql_query, False)
					for vals in self.dbCursor:
						ret_vals.append(vals)
				va_id = int(ret_vals[0][0])
				# same actions for role
				ret_vals = []
				sql_query = "SELECT role_id FROM roles WHERE name_first='"
				sql_query += vaRole_dict["RoleFirst"] if "RoleFirst" in vaRole_dict.keys() else ""
				sql_query += "' AND name_mid='"
				sql_query += vaRole_dict["RoleMid"] if "RoleMid" in vaRole_dict.keys() else ""
				sql_query += "' AND name_last='"
				sql_query += vaRole_dict["RoleLast"] if "RoleLast" in vaRole_dict.keys() else ""
				sql_query += "'"
				self.exeQuery(sql_query, False)
				for vals in self.dbCursor:
					ret_vals.append(vals)
				if(not ret_vals):
					sql_query = "INSERT INTO roles (job, name_first, name_mid, name_last) VALUES ("
					sql_query += "'" + vaRole_dict["RoleTitle"] + "', " if "RoleTitle" in vaRole_dict.keys() else "'', "
					sql_query += "'" + vaRole_dict["RoleFirst"] + "', " if "RoleFirst" in vaRole_dict.keys() else "'', "
					sql_query += "'" + vaRole_dict["RoleMid"] + "', " if "RoleMid" in vaRole_dict.keys() else "'', "
					sql_query += "'" + vaRole_dict["RoleLast"] + "')" if "RoleLast" in vaRole_dict.keys() else "'')"
					self.exeQuery(sql_query, True)

					sql_query = "SELECT LAST_INSERT_ID()"
					self.exeQuery(sql_query, False)
					for vals in self.dbCursor:
						ret_vals.append(vals)
				if(va_id not in va_roles_ids.keys()):
					va_roles_ids[va_id] = {}
				va_roles_ids[va_id][int(ret_vals[0][0])] = vaRole_dict["RoleRelevance"] if "RoleRelevance" in vaRole_dict.keys() else "none" #va_roles_ids = {va_id:{role_id: RoleRelevance}
		
		else:
			va_ids = []
			role_ids = {}
			for sub_dict in self.VARoleListDict:
				buff = " ".join(key for key in sub_dict.keys())
				if("VA" in buff and "Role" not in buff):
					ret_vals = []
					sql_query = "SELECT voice_id FROM voice_artists WHERE name_first='"
					sql_query += sub_dict["VAFirst"] if "VAFirst" in sub_dict.keys() else ""
					sql_query += "' AND name_mid='"
					sql_query += sub_dict["VAMid"] if "VAMid" in sub_dict.keys() else ""
					sql_query += "' AND name_last='"
					sql_query += sub_dict["VALast"] if "VALast" in sub_dict.keys() else ""
					sql_query += "'"
					self.exeQuery(sql_query, False)
					for vals in self.dbCursor:
						ret_vals.append(vals)
					if(not ret_vals):
						sql_query = "INSERT INTO voice_artists (title, name_first, name_mid, name_last) VALUES ("
						sql_query += "'" + sub_dict["VATitle"] + "', " if "VATitle" in sub_dict.keys() else "'', "
						sql_query += "'" + sub_dict["VAFirst"] + "', " if "VAFirst" in sub_dict.keys() else "'', "
						sql_query += "'" + sub_dict["VAMid"] + "', " if "VAMid" in sub_dict.keys() else "'', "
						sql_query += "'" + sub_dict["VALast"] + "')" if "VALast" in sub_dict.keys() else "'')"
						self.exeQuery(sql_query, True)
	
						sql_query = "SELECT LAST_INSERT_ID()"
						self.exeQuery(sql_query, False)
						for vals in self.dbCursor:
							ret_vals.append(vals)
					va_ids.append(int(ret_vals[0][0]))
				elif("VA" not in buff and "Role" in buff):
					ret_vals = []
					sql_query = "SELECT role_id FROM roles WHERE name_first='"
					sql_query += sub_dict["RoleFirst"] if "RoleFirst" in sub_dict.keys() else ""
					sql_query += "' AND name_mid='"
					sql_query += sub_dict["RoleMid"] if "RoleMid" in sub_dict.keys() else ""
					sql_query += "' AND name_last='"
					sql_query += sub_dict["RoleLast"] if "RoleLast" in sub_dict.keys() else ""
					sql_query += "'"
					self.exeQuery(sql_query, False)
					for vals in self.dbCursor:
						ret_vals.append(vals)
					if(not ret_vals):
						sql_query = "INSERT INTO roles (job, name_first, name_mid, name_last) VALUES ("
						sql_query += "'" + sub_dict["RoleTitle"] + "', " if "RoleTitle" in sub_dict.keys() else "'', "
						sql_query += "'" + sub_dict["RoleFirst"] + "', " if "RoleFirst" in sub_dict.keys() else "'', "
						sql_query += "'" + sub_dict["RoleMid"] + "', " if "RoleMid" in sub_dict.keys() else "'', "
						sql_query += "'" + sub_dict["RoleLast"] + "')" if "RoleLast" in sub_dict.keys() else "'')"
						self.exeQuery(sql_query, True)
	
						sql_query = "SELECT LAST_INSERT_ID()"
						self.exeQuery(sql_query, False)
						for vals in self.dbCursor:
							ret_vals.append(vals)
					role_ids[int(ret_vals[0][0])] = sub_dict["RoleRelevance"] if "RoleRelevance" in sub_dict.keys() else "none"
				else:
					messagebox.showerror(title="ANDI BESCHEIDGEBEN", message="fehler in der logik!\nfinger weg von der tastatur und andi bescheid geben")
					return False
			if (not role_ids):
				role_ids[1] = "none"
			for va in va_ids:
				va_roles_ids[va] = role_ids

		#=====================================================================================================
		
		if(self.altListDict):
			for alt_dict in self.altListDict:
				sql_query = "INSERT INTO alternative_names (audiobook_id, alt_name, year_changed, comments) VALUES ("
				sql_query += str(audiobook_id) + ", '" + alt_dict["Name"] + "', "
				sql_query += "'" + alt_dict["Year"] +"-01-01" + "', " if "Year" in alt_dict.keys() else "NULL, "
				sql_query += "'" + alt_dict["Comment"] + "')" if "Comment" in alt_dict.keys() else "NULL)"
				self.exeQuery(sql_query, True)

		#=====================================================================================================

		for auth_id in author_ids:
			sql_query = "INSERT INTO author_book (author_id, audiobook_id) VALUES ("
			sql_query += str(auth_id) + ", "
			sql_query += str(audiobook_id) + ")"
			self.exeQuery(sql_query, True)

		#=====================================================================================================

		for va_key in va_roles_ids.keys():
			for role_key in va_roles_ids[va_key].keys():
				sql_query = "INSERT INTO va_book (audiobook_id, role_id, voice_id, isPrimary, isSecondary) VALUES ("
				sql_query += str(audiobook_id) + ", "
				sql_query += str(role_key) + ", "
				sql_query += str(va_key) + ", "
				if(va_roles_ids[va_key][role_key] == "Main"):
					sql_query += "TRUE, FALSE)"
				elif(va_roles_ids[va_key][role_key] == "Help"):
					sql_query += "FALSE, TRUE)"
				else:
					sql_query += "FALSE, FALSE)"
				self.exeQuery(sql_query, True)

		#=====================================================================================================
		# clean up
		self.cleanAuthor()
		self.cleanVA()
		self.cleanRole()
		self.cleanAudiobook()
		self.authorAuthorsText.config(state="normal")
		self.authorAuthorsText.delete("1.0", tk.END)
		self.authorAuthorsText.config(state="disabled")
		self.showVARolePairText.config(state="normal")
		self.showVARolePairText.delete("1.0", tk.END)
		self.showVARolePairText.config(state="disabled")
		self.remainderSynopsisText.delete("1.0", tk.END)
		self.remainderCommentsText.delete("1.0", tk.END)
		self.remainderAltText.config(state="normal")
		self.remainderAltText.delete("1.0", tk.END)
		self.remainderAltText.config(state="disabled")
		self.authorsListDict = []
		self.VARoleListDict = []
		self.altListDict = []

	def cleanAuthor(self):
		self.authorTitle.set("")
		self.authorFirstName.set("")
		self.authorMidNames.set("")
		self.authorLastName.set("")
		self.authorBDayDate.set("")
		self.authorDeathDate.set("")
		self.authorAlias.set("")
		self.authorInfoLink.set("")

	def cleanAudiobook(self):
		self.audiobookName.set("")
		self.audiobookReleaseOriginal.set("")
		self.audiobookReleaseGer.set("")
		self.audiobookReleaseAudio.set("")
		self.audiobookBoxName.set("")
		self.audiobookGenre.set("")
		self.audiobookAmountCDs.set("")
		self.audiobookRuntime.set("")
		self.audiobookIsMp3CD.set(0)
		self.audiobookIsPcOnly.set(0)
		self.audiobookIsRoman.set(1)
		self.audiobookIsShortened.set(0)
		self.audiobookIsBox.set(0)
		self.audiobookBoxNameEntry.config(state="disabled")

	def cleanVA(self):
		self.reader_roleVATitle.set("")
		self.reader_roleVAFirstName.set("")
		self.reader_roleVAMidName.set("")
		self.reader_roleVALastName.set("")

	def cleanRole(self):
		self.reader_roleRoleTitle.set("")
		self.reader_roleRoleFirstName.set("")
		self.reader_roleRoleMidName.set("")
		self.reader_roleRoleLastName.set("")

	def addAuthor(self):
		self.authorAuthorsText.config(state="normal")
		strbuff = self.authorAuthorsText.get("1.0", tk.END)
		authbuff = ""
		infosDict = {}

		if(strbuff[-1] == "\n"):
			strbuff = strbuff[:-1]
		if(self.authorTitle.get() != ""):
			authbuff += self.authorTitle.get() + "; "
			infosDict["Title"] = self.authorTitle.get()
		if(self.authorFirstName.get() != ""):
			authbuff += self.authorFirstName.get() + "; "
			infosDict["First"] = self.authorFirstName.get()
		if(self.authorMidNames.get() != ""):
			authbuff += self.authorMidNames.get() + "; "
			infosDict["Mid"] = self.authorMidNames.get()
		if(self.authorLastName.get() != ""):
			authbuff += self.authorLastName.get() + "; "
			infosDict["Last"] = self.authorLastName.get()
		if(self.authorBDayDate.get() != ""):
			authbuff += self.authorBDayDate.get() + "; "
			infosDict["BDay"] = self.authorBDayDate.get()
		if(self.authorDeathDate.get() != ""):
			authbuff += self.authorDeathDate.get() + "; "
			infosDict["DDate"] = self.authorDeathDate.get()
		if(self.authorAlias.get() != ""):
			authbuff += self.authorAlias.get() + "; "
			infosDict["Alias"] = self.authorAlias.get()
		if(self.authorInfoLink.get() != ""):
			authbuff += self.authorInfoLink.get() + "; "
			infosDict["Nfo"] = self.authorInfoLink.get()

		if(authbuff != ""):
			if("First" not in infosDict.keys() and "Last" not in infosDict.keys()):
				messagebox.showerror(title="Autor Unvollständig!", message="Autor muss mindestens\nVor- oder Nachname\nhaben.")
				return False
			self.authorsListDict.append(infosDict)
			self.cleanAuthor()
			if(strbuff == ""):
				strbuff += authbuff
			else:
				strbuff += "\n" + authbuff
		self.authorAuthorsText.delete("1.0", tk.END)
		self.authorAuthorsText.insert("1.0", strbuff)
		self.authorAuthorsText.config(state="disabled")

	def addAltInfos(self):
		self.remainderAltText.config(state="normal")
		strbuff = self.remainderAltText.get("1.0", tk.END)
		infosDict = {}

		if(strbuff == "\n"):
			strbuff = ""
		if(self.remainderAltName.get() == ""):
			messagebox.showerror(title="Error!", message="Alt. Name muss einen Wert enthalten.")
			return False
		else:
			strbuff += f"{self.remainderAltName.get()}; "
			infosDict["Name"] = self.remainderAltName.get()
			self.remainderAltName.set("")
		if(self.remainderAltYear.get() != ""):
			strbuff += f"{self.remainderAltYear.get()}; "
			infosDict["Year"] = self.remainderAltYear.get()
			self.remainderAltYear.set("")
		if(self.remainderAltComment.get() != ""):
			strbuff += f"{self.remainderAltComment.get()}"
			infosDict["Comment"] = self.remainderAltComment.get()
			self.remainderAltComment.set("")

		self.altListDict.append(infosDict)
		self.remainderAltText.delete("1.0", tk.END)
		self.remainderAltText.insert("1.0", strbuff)
		self.remainderAltText.config(state="disabled")

	def uncheckIsMain(self):
		if(self.reader_roleIsHelper.get() == 1):
			self.reader_roleIsMain.set(0)

	def uncheckIsHelper(self):
		if(self.reader_roleIsMain.get() == 1):
			self.reader_roleIsHelper.set(0)

	def addRoleVAPair(self):
		self.showVARolePairText.config(state="normal")
		strbuff = self.showVARolePairText.get("1.0", tk.END)
		Rolebuff = ""
		VAbuff = ""
		infosDict = {}
		
		if(strbuff[-1] == "\n"):
			strbuff = strbuff[0:-1]
		if(self.reader_roleVATitle.get() != ""):
			VAbuff += self.reader_roleVATitle.get() + " "
			infosDict["VATitle"] = self.reader_roleVATitle.get()
		if(self.reader_roleVAFirstName.get() != ""):
			VAbuff += self.reader_roleVAFirstName.get() + " "
			infosDict["VAFirst"] = self.reader_roleVAFirstName.get()
		if(self.reader_roleVAMidName.get() != ""):
			VAbuff += self.reader_roleVAMidName.get() + " "
			infosDict["VAMid"] = self.reader_roleVAMidName.get()
		if(self.reader_roleVALastName.get() != ""):
			VAbuff += self.reader_roleVALastName.get() + " "
			infosDict["VALast"] = self.reader_roleVALastName.get()
		if(self.reader_roleRoleTitle.get() != ""):
			Rolebuff += self.reader_roleRoleTitle.get() + " "
			infosDict["RoleTitle"] = self.reader_roleRoleTitle.get()
		if(self.reader_roleRoleFirstName.get() != ""):
			Rolebuff += self.reader_roleRoleFirstName.get() + " "
			infosDict["RoleFirst"] = self.reader_roleRoleFirstName.get()
		if(self.reader_roleRoleMidName.get() != ""):
			Rolebuff += self.reader_roleRoleMidName.get() + " "
			infosDict["RoleMid"] = self.reader_roleRoleMidName.get()
		if(self.reader_roleRoleLastName.get() != ""):
			Rolebuff += " " + self.reader_roleRoleLastName.get()
			infosDict["RoleLast"] = self.reader_roleRoleLastName.get()
		if(self.reader_roleIsMain.get() == 1 and self.reader_roleVAvsRole.get() > 0):
			infosDict["RoleRelevance"] = "Main"
		if(self.reader_roleIsHelper.get() == 1 and self.reader_roleVAvsRole.get() > 0):
			infosDict["RoleRelevance"] = "Help"

		self.cleanRole()
		self.cleanVA()
		if(Rolebuff == "" and VAbuff == ""):
			messagebox.showerror(title="VA-Role Unvollständig", message="Rolle und/oder Leser müssen müssen\nmindestens einen Wert enthalten.")
			return False
		self.VARoleListDict.append(infosDict)
		if(strbuff != "" and (Rolebuff != "" or VAbuff != "")):
			strbuff += "\n"
		strbuff += VAbuff
		if(self.reader_roleVAvsRole.get() >= 1 and Rolebuff != ""):
			strbuff += "-> " + Rolebuff
			if(self.reader_roleIsMain.get() == 1):
				strbuff += " !H!"
				self.reader_roleIsMain.set(0)
			if(self.reader_roleIsHelper.get() == 1):
				strbuff += " !W!"
				self.reader_roleIsHelper.set(0)

		self.showVARolePairText.delete("1.0", tk.END)
		self.showVARolePairText.insert("1.0", strbuff)
		self.showVARolePairText.config(state="disabled")

	def changeBoxNameState(self):
		if(self.audiobookIsBox.get() == 1):
			self.audiobookBoxNameEntry.config(state="normal")
		elif(self.audiobookIsBox.get() == 0):
			self.audiobookBoxName.set("")
			self.audiobookBoxNameEntry.config(state="disabled")

	def changeVAState(self, new_state):
		self.reader_roleVATitleEntry.config(state=new_state)
		self.reader_roleVAFirstNameEntry.config(state=new_state)
		self.reader_roleVAMidNameEntry.config(state=new_state)
		self.reader_roleVALastNameEntry.config(state=new_state)

	def changeRoleState(self, new_state):
		self.reader_roleRoleTitleEntry.config(state=new_state)
		self.reader_roleRoleFirstNameEntry.config(state=new_state)
		self.reader_roleRoleMidNameEntry.config(state=new_state)
		self.reader_roleRoleLastNameEntry.config(state=new_state)
		self.reader_roleIsMainChButton.config(state=new_state)
		self.reader_roleIsHelperChButton.config(state=new_state)

	def changeVARoleState(self):
		if(self.reader_roleVAvsRole.get() == 0):
			self.changeRoleState("disabled")
			self.cleanRole()
			self.changeVAState("normal")
			self.reader_roleAddRoleButton.config(text="Leser\nHinzufügen")
		elif(self.reader_roleVAvsRole.get() == 1):
			self.changeRoleState("normal")
			self.cleanVA()
			self.changeVAState("disabled")
			self.reader_roleAddRoleButton.config(text="Rolle\nHinzufügen")
		elif(self.reader_roleVAvsRole.get() == 2):
			self.changeRoleState("normal")
			self.changeVAState("normal")
			self.reader_roleAddRoleButton.config(text="Leser->Rolle\nHinzufügen")


	def limitInputAll(self, event_key):
		if(event_key.char in self.forbidden_chars):
			return "break"
		else:
			return True

	def limitTextBox(self, event):
		if(event.char in self.forbidden_chars):
			return "break"
		if(event.keysym == 'Tab'):
			event.widget.tk_focusNext().focus()
			return "break"
		else:
			return True

	def limitInputDate(self, event_key):
		allowed_keysym = ['BackSpace', 'Tab', 'Return', 'KP_Enter', 'minus', 'period', 'slash', 'colon', 'Left', 'Right', 'Delete']
		if(event_key.char in self.forbidden_chars):
			return "break"
		elif(event_key.char.isdigit() or event_key.keysym in allowed_keysym):
			return True
		else:
			return "break"

	def limitInputTime(self, event_key):
		allowed_keysym = ['BackSpace', 'Tab', 'Return',  'KP_Enter', 'period', 'colon', 'Left', 'Right', 'Delete']
		if(event_key.char in self.forbidden_chars):
			return "break"
		elif(event_key.char.isdigit() or event_key.keysym in allowed_keysym):
			return True
		else:
			return "break"

	def limitInputDigits(self, event_key):
		allowed_keysym = ['BackSpace', 'Tab', 'Return',  'KP_Enter', 'Left', 'Right', 'Delete']
		if(event_key.char in self.forbidden_chars):
			return "break"
		elif(event_key.char.isdigit() or event_key.keysym in allowed_keysym):
			return True
		else:
			return "break"

if(__name__ == "__main__"):
	print("Connecting to Database...")
	try:
		dbConnection = mysql.connector.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_pw, database=mysql_db)
	except:
		print(" ".join(str(msg) for msg in sys.exc_info()))
		messagebox.showerror(title="ERROR!", message="Konnte nicht mit Datenbank verbinden.\nFehlermeldung steht in der Konsole.")
		sys.exit(0)
	print("Connection established!")
	dbCursor = dbConnection.cursor()
	root = tk.Tk()
	mainWnd = mainWindow(root, dbConnection, dbCursor)
	root.mainloop()
	dbCursor.close()
	dbConnection.close()