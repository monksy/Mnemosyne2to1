
__author__ = "steven"
__website__= "http://theexceptioncatcher.com"
__date__ = "$Feb 13, 2011$"


from xml.dom.minidom import Document
from pysqlite2 import dbapi2 as sqlite

#create database connection
conn = sqlite.connect("default.db")
cur = conn.cursor()

cur.execute("select name from tags")


xmlDoc = Document()
allNodes = xmlDoc.createElement("mnemosyne")
allNodes.setAttribute("core_version", "1")
allNodes.setAttribute("time_of_start", "1215720000")
xmlDoc.appendChild(allNodes)

#Categories
for cat in cur:
    item = xmlDoc.createElement("category")

    item.setAttribute("active", str("1"))
    incat = xmlDoc.createElement("name");
    incat.appendChild(xmlDoc.createTextNode(str(cat[0])))
    item.appendChild(incat)
    allNodes.appendChild(item)

#TODO Items
#<item id="74b1b599" gr="2" e="2.500" ac_rp="2" rt_rp="0" lps="0" ac_rp_l="2" rt_rp_l="0" l_rp="32" n_rp="33">
# <cat><th-en></cat>
# <Q>???</Q>
# <A>shadow; reflection; image</A>
#</item>
#
#

cur.execute("""
SELECT tags.name, cards.id, grade, easiness, acq_reps, ret_reps, lapses, acq_reps_since_lapse,  ret_reps_since_lapse, last_rep, next_rep , ques.value AS q, ans.value AS a
    FROM cards
    join  tags_for_card on cards._id = tags_for_card._card_id
     join  tags on tags_for_card._tag_id = tags._id
     JOIN data_for_fact AS ques  ON cards._fact_id=ques._fact_id AND ques.key='q'
    JOIN data_for_fact AS ans
      ON cards._fact_id=ans._fact_id AND ans.key='a'
    WHERE cards.fact_view_id='2::1'
  UNION
  SELECT tags.name, cards.id, grade, easiness, acq_reps, ret_reps, lapses, acq_reps_since_lapse,  ret_reps_since_lapse, last_rep, next_rep , ans.value AS q, ques.value AS a
  FROM cards
   join  tags_for_card on cards._id = tags_for_card._card_id
     join  tags on tags_for_card._tag_id = tags._id
     JOIN data_for_fact AS ans ON cards._fact_id=ans._fact_id AND ans.key='a'
    JOIN data_for_fact AS ques ON cards._fact_id=ques._fact_id AND ques.key='q'
   WHERE cards.fact_view_id='2::2'
""")

for itm in cur:
    item = xmlDoc.createElement("item")
    item.setAttribute("id", unicode(itm[1]))
    item.setAttribute("gr", str(itm[2]))
    item.setAttribute("e", str(itm[3]))
    item.setAttribute("ac_rp", str(itm[4]))
    item.setAttribute("rt_rp", str(itm[5]))
    item.setAttribute("lps", str(itm[6]))
    item.setAttribute("ac_rp_l", str(itm[7]))
    item.setAttribute("rt_rp_l", str(itm[8]))
    item.setAttribute("l_rp", str(itm[9]))
    item.setAttribute("n_rp", str(itm[10]))

    cat = xmlDoc.createElement("cat")
    cat.appendChild(xmlDoc.createTextNode(str(itm[0])))
    item.appendChild(cat)

    qu = xmlDoc.createElement("Q")
    qu.appendChild(xmlDoc.createTextNode(itm[11]))
    item.appendChild(qu)

    an = xmlDoc.createElement("A")
    an.appendChild(xmlDoc.createTextNode(itm[12]))
    item.appendChild(an)

    allNodes.appendChild(item)


print xmlDoc.toprettyxml(encoding="utf-8")
