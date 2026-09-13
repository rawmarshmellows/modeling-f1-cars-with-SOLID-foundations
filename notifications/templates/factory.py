from notifications.templates.html_template_v1 import HtmlTemplate_v1
from notifications.templates.plain_text_template_v1 import PlainTextTemplate_v1
from notifications.templates.rich_card_template_v1 import RichCardTemplate_v1


class TemplateFactory:
    @staticmethod
    def create_plain_text_template_v1():
        return PlainTextTemplate_v1()

    @staticmethod
    def create_html_template_v1():
        return HtmlTemplate_v1()

    @staticmethod
    def create_rich_card_template_v1():
        return RichCardTemplate_v1()
