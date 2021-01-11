# SEP_mod_mapping

When I was planning for my exchange semester, I naturally wanted to know which university I could map the most modules to, and also which universities offered the modules I was interested in taking.
I also wanted to know which of my modules could be mapped overseas at all, and which I would simply have to take in NUS.

As a Business Analytics (BZA) student in the NUS School of Computing, the modules that count toward my major are quite domain-specific.
Coupled with the fact that business analytics is a relatively new field, and is rarely offered as a degree at the undergraduate level, 
I was unsure if going on an exchange was even feasible for me. I decided to write some code to help me plan.

On my faculty website (NUS School of Computing), there was information on all the pre-approved module mappings. For example, NUS' `CS3244 Machine Learning` could be mapped to Georgetown's `COSC288 Introduction to Machine Learning`. 
This information was listed in tables, where each university had a table listing the Computing modules that could be mapped to that particular university.
With the sheer number of universities and modules available, I wanted a way to collate all this information, perhaps in a csv format or something similar, so that the information was displayed neatly and easy to manage.

At the time, I had not heard of BeautifulSoup or any other HTML web sraping libraries out there. 
Me being me, I jumped into doing things the stupid way, without doing any background research. 
I opened "Inspect" on my browser and looked at the HTML code on the faculty website, picking out the patterns that appeared in each table, such as:
`<tr>`, `<ul>` etc. The original html is saved as a `.txt` file - `overseasmods.txt`.

With this knowledge, I built a very basic (or should I say primitive), but also highly specific, highly un-scalable web scraper.
I also did some aggregation to display universities by the number of mappable modules they offered.

Since not all School of Computing modules are part of my curriculum (Bachelor of Science in Business Analytics), 
I also had to differentiate between modules that would count towards my major, and those that were targeted at CS/IS/InfoSec students.
+ `BZAmods.csv` is the full list of modules that fall under the BZA curriculum.
+ `BZAmodcodes.csv` is the module codes of all modules in the BZA curriculum, scraped from `BZAmods.csv`

It is obvious that modules and universities have a many-to-many relationship. That is, a university can offer multiple modules that can be mapped to NUS modules, 
while an NUS module may have multiple universities offering its mapped equivalent. `modsmap.py` processes the information both ways, 
tracking the modules offered by every university as well as the all the universities that offer a particular module. Its output consists of 
+ `mods_by_n_unis_offering.csv` which displays each BZA module by the number of universities that offer it, as well as
+ `overseasunis.csv` which displays each overseas university and the number and list of mappable BZA modules.

In `overlaps.py`, I compared the list of modules that appeared on the website to the list in `BZAmodcodes.csv`.
It outputs the following: 
+ `overlaps.csv` which shows the modules that can be mapped overseas on an exchange programme, and those that can't.

Imagine my chagrin when several months after cobbling this together I found out that NUS has a portal where you can export 
all the module mappings into a nicely formatted `.csv` file...
