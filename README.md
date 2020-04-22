# AudiobookDB
  Interactions with AudiobookDB mysql database.

Database for my Dads audiobooks.<br>
As he is german and his english isn't the best, most of the output is in german.<br>
English might be added later on.. but it's rather unlikely.<br>
<br>
Dividing the whole project in two different scripts is mostly for security reasons:<br>
audiobookDB_addEntries has a user that's allowed to freely add, modify and delete anything within the database.<br>
audiobookDB_readEntries (to be created) has a user that's only allowed to read entries.<br>
<br>
Database contains Author, (Audio)Book, Reader and Role Information<br>
and looks something along the lines of:<br>
![](Images/SQLDB.png)
♪ represents primary keys<br>
Red lines are foreign key connections/constraints<br>
It's not quite the final Database, but should give a proper idea.