import os
import time
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'doc', 'docx'])

class FileStorage:
    def __init__(self, file, at = None):
        self.file = file
        self.folder = at

    def allowed_file(self):
        return '.' in self.file.filename and self.file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_file(self):
        if self.file and self.allowed_file():
            upload_folder = str(os.getenv('UPLOAD_PATH'))
            filename = secure_filename(self.file.filename)
            if(self.folder != None):
                localtime = time.localtime(time.time())
                year = localtime[0]
                month = localtime[1]
                month_day = localtime[2]
                file_time = str(year)+ "/" + str(month) + "/" + str(month_day)
                file_path = upload_folder + "/" + self.folder + "/" + file_time
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
            else:
                file_path = upload_folder

            self.file.save(os.path.join(file_path, filename))

            return (os.path.join(file_path, filename))

        else:
            return None







