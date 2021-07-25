# GoogleMeetAutomatedTool

Made by Hullumeelne

This program lets you schedule Google Meetings, you can set:
- time to join Meeting
- join via link or a Saved Meeting
- time to leave Meeting
- leave if participants are below a certain number
- auto-fill fields in browser with your provided Google account details

You can Save Meetings, where you provide a title for the Meeting and a link to the Meeting. 
This means you don't need to insert the same links again every time if your Meetings links are temporary.
Then when scheduling your next Meetings, you can just select the saved Meeting from Saved Meetings.

With Scheduled Meetings window you can set multiple Meetings in row to be joined and left automatically.
When all the Meetings are finished, you will be shown a final report and status of every meeting (e.g. if the Meeting was joined successfully).
If you're a student, you can theoretically schedule all of the Meetings, depending on your teachers, and be away from your computer.

Program also automatically mutes and disables the camera when joining the Meeting.

Note:
- some Google accounts won't be able to login to Google from the Chrome driver. School maintained Google accounts can
- auto-fill can only be used with personal Google accounts
- leave and join time are both required
- don't use your computer while the program is trying to join Meetins, because it can interrupt the script 
  (although just a quick window switch from the user won't do any damage)
- set your computer to not go to sleep and to not black out the screen when running this tool
- currently available languages are english and estonian
- there are two "Start Meeting" buttons in the app. One is to start Scheduled Meetings and the other in the main window is to start a simpler single Meeting.

If downloading my program files from here (Github), you need to provide a downloaded Chrome driver file, named as "chromedriver.exe" and place it in the same folder with python scripts.
(https://chromedriver.chromium.org/downloads)
