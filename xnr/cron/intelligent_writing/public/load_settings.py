#-*-coding=utf-8-*-

import default_settings
import settings as over_settings


def iter_default_settings():
    """Return the default settings as an iterator of (name, value) tuples
       参数需要大写
    """
    for name in dir(default_settings):
        if name.isupper():
            yield name, getattr(default_settings, name)


def iter_settings():
    """Return the settings as an iterator of (name, value) tuples
       参数需要大写
    """
    for name in dir(over_settings):
        if name.isupper():
            yield name, getattr(over_settings, name)


def overidden_settings(settings=over_settings):
    """Return a dict of the settings that have been overridden"""
    for name, defvalue in iter_default_settings():
        if name in settings:
            value = settings[name]

        if not isinstance(defvalue, dict) and value != defvalue:
            yield name, value


def load_settings(settings=None):
    """load settings
       settings: dict, 需要覆盖的参数
    """
    over = dict()
    if not settings:
        # 不指定settings，则从settings.py加载配置
        for name, defvalue in iter_settings():
            over[name] = defvalue
    else:
        # 指定dict类型的settings进行覆盖
        over = settings

    defaults = dict()
    for name, defvalue in iter_default_settings():
        defaults[name] = defvalue

    defaults.update(over)
    return defaults


if __name__=='__main__':
    settings = load_settings()
    print settings

