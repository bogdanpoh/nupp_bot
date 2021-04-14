import os
import constants
import tools

class FileManager(object):
    path_for_excel = os.path.join(constants.documents_directory, constants.excel_file)
    path_for_txt = os.path.join(constants.documents_directory, constants.txt_file)

    @staticmethod
    def if_not_exists_dir_make(path):
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def if_file_exists_remove(path):
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def download_file(bot, message, path):
        file_info = bot.get_file(message.document.file_id)
        type_file = str(file_info.file_path).split(".")[-1]
        downloaded_file = bot.download_file(file_info.file_path)
        full_path = "{}.{}".format(path, type_file)
        FileManager.if_file_exists_remove(full_path)
        tools.download_file(full_path, downloaded_file)
        return full_path
