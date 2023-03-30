# Keypirinha launcher (keypirinha.com)

import os
import re
from pathlib import Path

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
    ITEMCAT_RUN_1C = kp.ItemCategory.USER_BASE + 5
    ITEMCAT_IBASES_MANAGER = kp.ItemCategory.USER_BASE + 6
    ITEMCAT_IBASES_MANAGER_RUN = kp.ItemCategory.USER_BASE + 7

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
        self.set_catalog([
            self.create_item(
                category=self.ITEMCAT_RUN_1C,
                label='Run 1C',
                short_desc='Run 1C base from a valid server-base path',
                target='run_1c',
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.IGNORE),
            self.create_item(
                category=self.ITEMCAT_IBASES_MANAGER,
                label='ibases manager',
                short_desc='Manage 1C bases from local ibases.v8i file',
                target='ibases_manager',
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.IGNORE)])

    def on_suggest(self, user_input, items_chain):
        if not items_chain:
            return

        print('on_suggest')

        cur_item = items_chain[-1]
        cat = items_chain[-1].category()
        target = cur_item.target()

        if cat == self.ITEMCAT_RUN_1C:
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

        elif cat == self.ITEMCAT_IBASES_MANAGER:

            bases = self.get_bases_from_ibases_file()

            suggestions = []

            for base in bases:
                suggestions.append(self.create_item(
                    category=self.ITEMCAT_IBASES_MANAGER_RUN,
                    label=base['name'],
                    short_desc=base['path'],
                    target=base['path'],
                    args_hint=kp.ItemArgsHint.REQUIRED,
                    hit_hint=kp.ItemHitHint.IGNORE))

            self.set_suggestions(suggestions, kp.Match.FUZZY, kp.Sort.NONE)

        elif cat == self.ITEMCAT_IBASES_MANAGER_RUN:

            server_base_path = self.parse_server_base_path(target)
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

    def get_bases_from_ibases_file(self):
        
        appdata = os.getenv('appdata')
        
        ibases_file = Path(f"{appdata}/1C/1CEStart/ibases.v8i")
        
        if not ibases_file.exists():
            return []

        text = ibases_file.read_text(encoding='utf-8')

        bases = []

        for line in text.split('\n'):
            line = line.strip().replace('﻿', '')
            if not line:
                continue
            if line[0] == '[':
                bases.append({ 'name': line, 'path': '' })
            if 'Connect=' in line:
                bases[-1]['path'] = line.replace('Connect=', '')

        bases = [base for base in bases if base['path']]

        return bases
