# Keypirinha launcher (keypirinha.com)

import re

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

class run_1c(kp.Plugin):
    """
    Quick run 1C base from server-base path plugin
    """

    ITEMCAT_RUN_ENTERPRISE = kp.ItemCategory.USER_BASE + 1
    ITEMCAT_RUN_ENTERPRISE_MANAGED = kp.ItemCategory.USER_BASE + 2
    ITEMCAT_RUN_ENTERPRISE_ORDINARY = kp.ItemCategory.USER_BASE + 3
    ITEMCAT_RUN_CONFIG = kp.ItemCategory.USER_BASE + 4

    def __init__(self):
        super().__init__()

    def on_start(self):
        settings = self.load_settings()
        self.starter_path = settings.get('starter_path', 'main')
        self.icon_path = f'res://{self.package_full_name()}/1c.ico'

        self.set_default_icon(self.load_icon(self.icon_path))

        self.set_actions(self.ITEMCAT_RUN_ENTERPRISE, [
            self.create_action(
                name='managed',
                label='Run in Managed mode'),
            self.create_action(
                name='ordinary',
                label='Run in Ordinary mode')
        ])

    def on_catalog(self):
        self.set_catalog([self.create_item(
            category=kp.ItemCategory.KEYWORD,
            label='Run 1C',
            short_desc='Run 1C base from a valid server-base path',
            target='run_1c',
            args_hint=kp.ItemArgsHint.REQUIRED,
            hit_hint=kp.ItemHitHint.IGNORE)])

    def on_suggest(self, user_input, items_chain):
        if not items_chain or items_chain[-1].category() != kp.ItemCategory.KEYWORD:
            return

        server_base_path = self.parse_server_base_path(user_input)
        if not server_base_path:
            return
        [server_name, base_name] = server_base_path
        valid_base_path = f'{server_name}/{base_name}'

        suggestions = []
        
        suggestions.append(self.create_item(
            category=self.ITEMCAT_RUN_ENTERPRISE,
            label='Run Enterprise',
            short_desc=f'[{valid_base_path}]',
            target=valid_base_path,
            args_hint=kp.ItemArgsHint.FORBIDDEN,
            hit_hint=kp.ItemHitHint.IGNORE))

        suggestions.append(self.create_item(
            category=self.ITEMCAT_RUN_CONFIG,
            label='Run Config',
            short_desc=f'[{valid_base_path}]',
            target=valid_base_path,
            args_hint=kp.ItemArgsHint.FORBIDDEN,
            hit_hint=kp.ItemHitHint.IGNORE))

        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)

    def on_execute(self, item, action):
        if item and item.category() == self.ITEMCAT_RUN_ENTERPRISE:
            if not action:
                self.run_base(item.target())
            elif action.name() == 'managed':
                self.run_base(item.target(), 'managed')
            elif action.name() == 'ordinary':
                self.run_base(item.target(), 'ordinary')

        elif item and item.category() == self.ITEMCAT_RUN_CONFIG:
            self.run_base(item.target(), 'config')

    def parse_server_base_path(self, base_path):
        r = re.search('"(.+)".+"(.+)"', base_path)

        if r == None:
            return

        groups = r.groups()

        if groups:
            return groups

    def run_base(self, valid_base_path, launch_mode=None):
        app_type = 'ENTERPRISE'
        enterprise_mode = ''

        if launch_mode == 'config':
            app_type = 'CONFIG'
        elif launch_mode == 'managed':
            enterprise_mode = '/RunModeManagedApplication'
        elif launch_mode == 'ordinary':
            enterprise_mode = '/RunModeOrdinaryApplication'

        exe_path = f'\"{self.starter_path}\"'
        args_text = f'{app_type} /S {valid_base_path} {enterprise_mode}'
        kpu.shell_execute(exe_path, args_text)
