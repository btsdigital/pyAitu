from ...utils.strings import SHOW_SHARE_CONTACT_BUTTON, SHOW_RECORD_AUDIO_BUTTON, SHOW_GALLERY_BUTTON, \
    SHOW_CAMERA_BUTTON, REPLY_KEYBOARD, QUICK_BUTTON_COMMANDS, FORM_MESSAGE


class UiState:
    def __init__(self,
                 show_camera_button=True,
                 show_share_contact_button=True,
                 show_record_audio_button=True,
                 show_gallery_button=True,
                 can_write_text=False,
                 reply_keyboard: list = None,
                 quick_button_commands: list = None,
                 form_message: dict = None
                 ):
        self.show_camera_button = show_camera_button
        self.show_share_contact_button = show_share_contact_button
        self.show_record_audio_button = show_record_audio_button
        self.show_gallery_button = show_gallery_button
        self.can_write_text = can_write_text
        self.form_message = form_message
        self.reply_keyboard = []
        self.quick_button_commands = []

        if reply_keyboard:
            for command in reply_keyboard:
                self.reply_keyboard.append(command.to_dict())

        if quick_button_commands:
            for command in quick_button_commands:
                self.quick_button_commands.append(command.to_dict())

    def to_dict(self):
        return self.remove_empty_keyboard({
            SHOW_CAMERA_BUTTON: self.show_camera_button,
            SHOW_GALLERY_BUTTON: self.show_gallery_button,
            SHOW_RECORD_AUDIO_BUTTON: self.show_record_audio_button,
            SHOW_SHARE_CONTACT_BUTTON: self.show_share_contact_button,
            REPLY_KEYBOARD: self.reply_keyboard,
            QUICK_BUTTON_COMMANDS: self.quick_button_commands,
            FORM_MESSAGE: self.form_message
        })

    def remove_empty_keyboard(self, command: dict):
        if not command.get(REPLY_KEYBOARD):
            command.pop(REPLY_KEYBOARD)
        if not command.get(QUICK_BUTTON_COMMANDS):
            command.pop(QUICK_BUTTON_COMMANDS)
        return command
