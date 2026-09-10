function showToolbar()
{
// AddItem(id, text, hint, location, alternativeLocation);
// AddSubItem(idParent, text, hint, location);

	menu = new Menu();
	menu.addItem("webmasterid", "My Sites", "My Sites",  null, null);
	menu.addItem("newsid", "Kerala News", "Kerala News",  null, null);
        menu.addItem("musicid", "Favourites", "Favourites",  null, null);
	menu.addItem("searchengineid", "Search Engines", "Search Engines",  null, null);
	menu.addItem("miscid", "Miscellaneous", "Miscellaneous",  null, null);
	menu.addItem("emailid", "Contact", "Contact",  null, null);

	menu.addSubItem("webmasterid", "Kerala on the Net", "Kerala on the Net",  "http://www.123kerala.com/");
	menu.addSubItem("webmasterid", "Bollywood on the Net", "Bollywood on the Net",  "http://www.geocities.com/bollywud/");
	menu.addSubItem("webmasterid", "Malayalam Publications", "Malayalam Publications",  "http://www.123kerala.com/malpub.html");
        menu.addSubItem("webmasterid", "www.123kerala.com", "www.123kerala.com",  "http://www.123kerala.com/index.htm");
	menu.addSubItem("webmasterid", "Malayalee Homepages", "Malayalee Homepages",  "http://www.123kerala.com/malayaly.html");
	menu.addSubItem("webmasterid", "Tellicherry.com", "Tellicherry.com",  "http://www.tellicherry.com/");
	menu.addSubItem("webmasterid", "Abbassiya.com", "Abbassiya.com",  "http://www.abbassiya.com/");
        menu.addSubItem("webmasterid", "Chithram", "Chithram",  "http://www.123kerala.com/chithram/");

	menu.addSubItem("newsid", "Mathrubhumi", "Mathrubhumi",  "http://www.mathrubhumi.com");
	menu.addSubItem("newsid", "Malayala Manorama", "Malayala Manorama",  "http://www.malayalamanorama.com");
	menu.addSubItem("newsid", "Kerala Kaumudi", "Kaumudi",  "http://www.kaumudi.com");
	menu.addSubItem("newsid", "Deepika", "Deepika",  "http://www.deepika.com");
	menu.addSubItem("newsid", "Deshabhimani", "Deshabhimani",  "http://www.deshabhimani.com");
	menu.addSubItem("newsid", "Mangalam", "Mangalam",  "http://www.mangalam.net");

	menu.addSubItem("musicid", "Cricinfo", "Cricinfo",  "http://www-uk.cricket.org/");
	menu.addSubItem("musicid", "Rediff on the Net", "Rediff on the Net",  "http://www.rediff.com/");
	menu.addSubItem("musicid", "Samachar", "Samachar",  "http://www.samachar.com/");

	menu.addSubItem("searchengineid", "Yahoo", "Yahoo",  "http://www.yahoo.com/");
	menu.addSubItem("searchengineid", "Infoseek", "Infoseek",  "http://www.infoseek.com/");
	menu.addSubItem("searchengineid", "Excite", "Excite", "http://www.excite.com");
	menu.addSubItem("searchengineid", "HotBot", "HotBot",  "http://www.hotbot.com");

	menu.addSubItem("miscid", "Hitbox.com", "Hitbox.com",  "http://www.hitbox.com/");
	menu.addSubItem("miscid", "Cnet", "Cnet",  "http://www.cnet.com/");
	menu.addSubItem("miscid", "Andover.net", "Andover.net",  "http://www.andover.net/");
	menu.addSubItem("miscid", "RealAudio", "RealAudio",  "http://www.realaudio.com/");
	menu.addSubItem("miscid", "MP3.com", "MP3.com",  "http://www.mp3.com/");

	menu.addSubItem("emailid", "Contact", "Contact",  "mailto:sanjeev@123kerala.com");


	menu.showMenu();
}