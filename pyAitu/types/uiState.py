from ..utils.strings import SHOW_SHARE_CONTACT_BUTTON,\
    SHOW_RECORD_AUDIO_BUTTON, SHOW_GALLERY_BUTTON, SHOW_CAMERA_BUTTON


class UiState:
    def __init__(self,
                 show_camera_button=True,
                 show_share_contact_button=True,
                 show_record_audio_button=True,
                 show_gallery_button=True):
        self.show_camera_button = show_camera_button
        self.show_share_contact_button = show_share_contact_button
        self.show_record_audio_button = show_record_audio_button
        self.show_gallery_button = show_gallery_button

    def get_default_ui_state(self):
        return {
            SHOW_CAMERA_BUTTON: self.show_camera_button,
            SHOW_GALLERY_BUTTON: self.show_gallery_button,
            SHOW_RECORD_AUDIO_BUTTON: self.show_record_audio_button,
            SHOW_SHARE_CONTACT_BUTTON: self.show_share_contact_button
        }
