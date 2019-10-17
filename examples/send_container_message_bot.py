import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, FormClosed, FormSubmitted, CustomContainer, Indent, \
    FlexOptions, Image, FileMetadata, Text, Divider
from pyAitu.utils.strings import UPLOADED_FILES


API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dispatcher.message_handler()
async def handle(message: Message):
    """
    Layers of containers:
    Main Container <- Parent Container <- Child Container
    """

    # Child Component
    child_contact_number_text = Text(
        content_id="text_id",
        title="+7 (727) 332-77-22",
        options=Options(
            text_size="H3",
            text_style="bold",
            indent_outer=Indent(left=12, top=4, right=12, bottom=12),
            text_color="#A9ADB1"
        )
    )

    # Child Component
    child_contact_title_text = Text(
        content_id="text_id",
        title="Контактный телефон:",
        options=Options(
            text_size="H4",
            indent_outer=Indent(left=12, top=2, right=12),
            text_color="#A9ADB1"
        )
    )

    # Child Component
    child_divider = Divider(
        content_id="divider_id",
        options=Options(
            indent_outer=Indent(left=12, top=14, right=12)
        )
    )

    # Child Component
    child_subtitle_text = Text(
        content_id="text_id",
        title="eubank.kz",
        options=Options(
            text_size="H4",
            alignment="right",
            indent_outer=Indent(left=12, top=2, right=12),
            text_color="#0075EB"
        ),
        # form_action=FormAction(action="open_url",
        #                        data_template="https://eubank.kz")
    )

    # Child Component
    child_title_text = Text(
        content_id="text_cat_id",
        title="Евразийский банк",
        options=Options(
            text_size="H3",
            text_style="bold",
            indent_outer=Indent(left=12, top=12, right=12),
        )
    )

    # Child Component
    file = await bot.upload_file("images/cat.jpg")
    child_image = Image(
        content_id="image_id",
        options=Options(width=37, height=6,
                        flex_options=FlexOptions(align_self="center")),
        file_metadata=FileMetadata(
            file_id=file.get(UPLOADED_FILES)[0]["fileId"],
            file_type="image",
            file_name=file.get(UPLOADED_FILES)[0]["fileName"]
        )
    )

    # Child Container
    child_custom_container = CustomContainer(
        content_id="child_id_1",
        options=Options(width=62, height=16,
                        flex_options=FlexOptions(flex_direction="column", align_items="center"),
                        background_color="#2B296D"),
        content=[child_image]
    )

    # Parent Container
    parent_custom_container = CustomContainer(
        content_id="parent_id",
        options=Options(width=62, flex_options=FlexOptions(flex_direction="column", align_items="start")),
        content=[child_custom_container, child_title_text, child_subtitle_text, child_divider, child_contact_title_text,
                 child_contact_number_text]
    )

    # Main Container
    main_custom_container = CustomContainer(
        content_id="main_id",
        options=Options(indent_outer=Indent(left=16, right=16, top=8, bottom=8), background="card"),
        content=[parent_custom_container]
    )

    content = [main_custom_container, main_custom_container, main_custom_container]

    await bot.send_container_message(message.chat.id, content=content)


@dispatcher.form_submitted_handler()
async def handle_submission(submitted_form: FormSubmitted):
    await bot.send_message(
        submitted_form.chat.id,
        f"Oh, it seems I have received text from you, look:\n\"{submitted_form.metadata}\""
    )


@dispatcher.form_closed_handler()
async def handle_form_closing(closed_form: FormClosed):
    await bot.send_message(closed_form.chat.id, "Form is closed")


if __name__ == '__main__':
    executor.start_polling(dispatcher)
