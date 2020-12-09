import os, pymysql
import datetime
from addons.textbook.model.textbook import Textbook
from addons.image.model.image import Image
from common.models.course import Course
from common.models.textbook_course import Textbook_Course



def handle_raw_tables():
    Textbook.create_table()
    Course.create_table()
    Textbook_Course.create_table()
    fp = "C:/Users/yz391/Desktop/book_cover"

    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           db='texbook',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute('''
            SELECT distinct course_name,course_ID,instructor,subject from book
        ''')
    course_res = cursor.fetchall()
    for e in course_res:
        Course.insert(
            course_ID=e["course_ID"],
            course_name=e["course_name"],
            instructor=e["instructor"],
            subject=e["subject"]
        ).execute()

    dir_path = os.listdir(fp)
    for name in dir_path:
        with open(fp + "/" + name, "rb") as p:
            image_content = p.read()
        Image.insert(
            owner_email="public",
            image_format="jpg",
            type="bookcover:" + name.split(".")[0],
            content=image_content,
            dateAdded=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ).execute()

    query = '''
                select * from book
        '''
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    for e in res:

        title = e["book_title"]
        des = e["book_description"].split(';')
        ISBN = des[0].split(":")
        if len(ISBN) > 1:
            ISBN = ISBN[1].split(".")[0].strip(" ")
        else:
            ISBN = ISBN[0].split(".")[0].strip(" ")
        try:
            author = des[1].split(":")[1].strip(" ")
        except:
            author = "NULL"
        try:
            edition = des[2].split(":")[1].strip(" ")
        except:
            edition = "NULL"
        try:
            publisher = des[3].split(":")[1].strip(" ")
        except:
            publisher = "NULL"

        query = Image.select().where(Image.type == "bookcover:" + ISBN)
        if query.exists():
            image_id = query.get().id
            Textbook.insert(
                ISBN=ISBN,
                title=title,
                author=author,
                edition=edition,
                publisher=publisher,
                price=e["book_price"],
                book_format=e["book_format"],
                cover_image_id=image_id
            ).execute()
        else:
            Textbook.insert(
                ISBN=ISBN,
                title=title,
                author=author,
                edition=edition,
                publisher=publisher,
                price=e["book_price"],
                book_format=e["book_format"],
            ).execute()

    for e in res:
        course_id = Course.select().where(Course.course_ID == e["course_ID"]).get().id
        textbook_id = Textbook.select().where(Textbook.title == e["book_title"]).get().id
        Textbook_Course.insert(
            course_id=course_id,
            textbook_id=textbook_id
        ).execute()




def insert_images():
    fp = "C:/Users/yz391/Desktop/collected_covers"
    dir_path = os.listdir(fp)
    for name in dir_path:
        with open(fp + "/" + name, "rb") as p:
            image_content = p.read()

        if "-" not in name:
            name = name[:3]+"-"+name[3:]

        name = name.split(".")[0]

        query = Image.select(Image.id).where(Image.type.contains(name))
        if not query.exists():
            Image.insert(
                owner_email="public",
                image_format="jpg",
                type="bookcover:"+name,
                content=image_content,
                dateAdded=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ).execute()


def textbook_reference():
    textbook_list = Textbook.select()

    for book in textbook_list:
        if book.cover_image_id is None:
            ISBN = book.ISBN.replace("-rent","").replace(" Author","").replace("-Web","")
            query = Image.select().where(Image.type.contains(ISBN))
            if query.exists():
                book_cover_image=query.get()
                Textbook.update(ISBN=ISBN,cover_image_id=book_cover_image.id).where(Textbook.id == book.id).execute()
            else:
                print(ISBN)


if __name__ == "__main__":
    # textbook_reference()
    from addons.image.model.image import Image
    with open("C:/Users/yz391/Desktop/matthew-feeney-Nwkh-n6l25w-unsplash.jpg","rb") as fp:
        f = fp.read()
    Image.update(
        content=f).where(Image.id==2151).execute()














