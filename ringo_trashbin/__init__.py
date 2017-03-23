import logging
from pyramid.i18n import TranslationStringFactory
from ringo.lib.i18n import translators
from ringo_trashbin import views

log = logging.getLogger(__name__)


def includeme(config):
    """Registers a new modul for ringo.

    :config: Dictionary with configuration of the new modul

    """
    translators.append(TranslationStringFactory('ringo_trashbin'))
    config.add_translation_dirs('ringo_trashbin:locale/')
