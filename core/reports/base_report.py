class BaseReport:

    def __init__(self, master_file, folder, callback=None):

        self.master_file = master_file
        self.folder = folder
        self.callback = callback

    # -----------------------------------------------------

    def notify(self, message):

        if self.callback:
            self.callback(message)