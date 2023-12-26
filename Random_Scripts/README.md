# What is <I>this</I> now?
This is a collection of utility scripts. Most of these will be <b>batch</b> files for use on windows machines. 

## backupCreation.bat and backupRestore.bat

These are scripts to create and restore backups of MS Office Template folder.\
Primary purpose of these backups is to backup <I>Autocorrect</I> entries from <b>MS Word</b>, for safe-keeping and also transfer to other systems.
Sometimes, these entries get corrupted and messed up, which necessitated the creation of these scripts.\
[backupCreation.bat](backupcreation.bat) copies the current contents of <I>'Templates'</I> to a folder named "USG Backup [current system date]", which it creates in the same folder the script is present in.\
[backupRestore.bat](backuprestore.bat) copies the contents of the latest backup (from the same folder as the script) to the location of <I>'Templates'</I> folder on the computer.

 

