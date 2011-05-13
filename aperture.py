import sqlite3
import datetime
import re
import os

from Cheetah.Template import Template

OUTPUT_FOLDER = "output"
MASTERS_FOLDER = "/Volumes/MCP/Pictures/Aperture Library.aplibrary/Masters"

NON_ALPHANUM_REGEX = re.compile('[\W_]+')

def alphanum(name):
    return NON_ALPHANUM_REGEX.sub("", name)

class Folder(object):
    def __init__(self):
        super(Folder, self).__init__()

        self.uuid = ""
        self.name = ""
        self.parent_uuid = ""
        self.parent = None
        self.child_folders = []
        self.child_photos = []
    
    def __unicode__(self):
        return u"<Folder({0})>".format(self.name)
    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def stub_name(self):
        stub_components = [alphanum(self.name.lower())]
        
        parent = self.parent
        
        while parent and parent.parent:
            stub_components.append(alphanum(parent.name.lower()))
            parent = parent.parent
        
        stub_components.reverse()
        
        return "_".join(stub_components)

class Photo(object):
    def __init__(self):
        super(Photo, self).__init__()
        
        self.id = 0
        self.uuid = ""
        self.name = ""
        self.parent = None
        self.keywords = []
        self.date = None
        self.path = ""
        self.size = 0
    
    def __unicode__(self):
        return u"<Photo({0}) in {1}>".format(self.name, self.parent.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

class Keyword(object):
    def __init__(self):
        super(Keyword, self).__init__()
        
        self.id = 0
        self.uuid = ""
        self.name = ""
        self.children = []
    
    def __unicode__(self):
        return u"<Keyword({0})>".format(self.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

def load_folders(c):
    folders = {}
    
    c.execute("select * from RKFolder")
    
    for row in c:
        folder = Folder()
        
        folder.uuid = row[1]
        folder.name = row[3]
        folder.parent_uuid = row[4]
        
        folders[folder.uuid] = folder
    
    for folder in folders.values():
        if folder.parent_uuid:
            folder.parent = folders[folder.parent_uuid]
            folders[folder.parent_uuid].child_folders.append(folder)
    
    return folders

def print_folders(root, depth=0):
    print ("  " * depth) + root.name, len(root.child_photos)
    for folder in root.child_folders:
        print_folders(folder, depth + 1)

def load_photos(c, folders):
    photos = {}
    
    c.execute("select * from RKMaster")
    
    for row in c:
        photo = Photo()
        
        photo.id = row[0]
        photo.uuid = row[1]
        photo.name = row[2]
        photo.parent = folders[row[3]]
        photo.path = os.path.join(MASTERS_FOLDER, row[17])
        photo.size = row[18]
        
        if row[21]:
            photo.date = datetime.datetime.fromtimestamp(row[21] + 978307200)
        
        photos[photo.id] = photo
        photo.parent.child_photos.append(photo)
    
    return photos

def load_keywords(c):
    keywords = {}
    
    c.execute("select * from RKKeyword")
    
    for row in c:
        keyword = Keyword()
        keyword.id = row[0]
        keyword.uuid = row[1]
        keyword.name = row[2]
        
        keywords[keyword.id] = keyword
    
    return keywords

def apply_keywords(c, keywords, photos):
    c.execute("select * from RKKeywordForVersion")
    
    for row in c:
        if row[1] in photos:
            keywords[row[2]].children.append(photos[row[1]])
            photos[row[1]].keywords.append(keywords[row[2]])

def generate_folder_indices(folders):
    def generate_folder_index(folder):    
        templ = Template(file="folder_index.tmpl")
        templ.root_folder = folder
        
        out_file_name = os.path.join(OUTPUT_FOLDER, folder.stub_name() + ".html")
        out_file = open(out_file_name, "w")
        out_file.write(str(templ))
        out_file.close()
        
        print "Generated", out_file_name
    
    def recurse_folders(folder):
        generate_folder_index(folder)
        [recurse_folders(f) for f in folder.child_folders]
        
    recurse_folders(folders["AllProjectsItem"])

def main():
    conn = sqlite3.connect("Library.apdb")

    c = conn.cursor()

    folders = load_folders(c)
    keywords = load_keywords(c)
    photos = load_photos(c, folders)
    
    apply_keywords(c, keywords, photos)
    
    generate_folder_indices(folders)
    
    #for photo in photos.values():
    #    print photo, photo.date
    
    #print_folders(folders["AllProjectsItem"])
    
    #print sum([photo.size for photo in photos.values()])

if __name__ == '__main__':
    main()
    