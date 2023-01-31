r'''
This is a simple wrapper around the MS TaskDialog API
See https://learn.microsoft.com/en-us/windows/win32/controls/task-dialogs for more information.

The workflow is like this

1. Import the module
2. Create a dialog instance
3. Call the create_page method for the first page.
3. Show the dialog

Minimal example:

    from taskdialog import Dialog
    from time import ctime

    class MinimalDialog(Dialog):

        def __init__(self):
            if sys.version_info[0] == 2:
                super(MinimalDialog, self).__init__()
            else:
                super().__init__()
            
            self.create_page(
                title = "MyTitle", 
                main_instruction = "Main instructions going here", 
                push_buttons = [
                    (1000, "Close this task", self.on_close)
                ], 
            )

            
        def on_close(self, id):
            return 0  # triggers closing


    m = MinimalDialog()
    m.show()
    print(m.checked_verification)


Slightly more enhanced example


    from taskdialog import Dialog
    from time import ctime

    class MyDialog(Dialog):

        def __init__(self):
            if sys.version_info[0] == 2:
                super(MyDialog, self).__init__()
            else:
                super().__init__()
            
            self.create_page(
                title = "MyTitle", 
                main_instruction = "Main instructions going here", 
                content = "{0}".format(ctime()),
                default_button = 1001,
                push_buttons = [
                    (1000, "Close this task", self.on_close), 
                    (1001, "Next", self.create_second_page)
                ], 
                default_radio_button = 2003,
                radio_buttons = [
                    (2000, "option &0", self.on_option),
                    (2001, "option 1", self.on_option2),
                    (2002, "option 2", self.on_option2),
                    (2003, "option &3", self.on_option),
                ],
                verification_text = "Verification requested !!",
                # expanded_information = "expanded_information !!",
                # expanded_control_text = "expanded_control_text !!",
                # collapsed_control_text = "collapsed_control_text !!",
                # footer = "footer !!",
                width = 400
            )

            
        def on_close(self, id):
            print("I'm closing")
            return 0  # triggers closing

        def create_third_page(self, id):
            self.use_command_links(True)
            self.use_hyper_links(True)
            self.create_page(
                content = "<a href=\"https://github.com/bruderstein/PythonScript/releases\">This is a link to the PS release page</a>",
                push_buttons = [
                    (1000, "Close this task", self.on_close), 
                ],
                radio_buttons = []
            )

        def create_second_page(self, id):
            self.use_command_links(False)
            self.create_page(
                title = "Changing title", 
                main_instruction = "forget what I said the last time", 
                content = "Now do this",
                push_buttons = [
                    (1000, "Close this task", self.on_close), 
                    (1001, "Go on", self.create_third_page), 
                ],
                radio_buttons = []
            )

        def on_option(self, id):
            print("Clicked on option button id", id)
            
        def on_option2(self, id):
            print("Triggered by option button id", id)


    m = MyDialog()
    m.show()
    print(m.checked_verification)
'''

__version__ = '0.1.0'
__all__ = ['Dialog']

from .taskdlg import Dialog