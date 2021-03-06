# -*- coding: utf-8 -*-
#
# Copyright © 2012 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from weblate.trans.management.commands import UnitCommand
from weblate.trans.models import Unit
from weblate.lang.models import Language
from weblate.trans.search import FULLTEXT_INDEX, create_source_index, create_target_index
from optparse import make_option

class Command(UnitCommand):
    help = 'rebuilds index for fulltext search'
    option_list = UnitCommand.option_list + (
        make_option('--clean',
            action='store_true',
            dest='clean',
            default=False,
            help='removes also all words from database'),
        )

    def handle(self, *args, **options):
        languages = Language.objects.all()
        if options['clean']:
            create_source_index()
            for lang in languages:
                create_target_index(lang = lang.code)

        base = self.get_units(*args, **options)

        if base.count() == 0:
            return

        with FULLTEXT_INDEX.source_writer(buffered = False) as writer:
            for unit in base.values('checksum', 'source', 'context').iterator():
                Unit.objects.add_to_source_index(
                    unit['checksum'],
                    unit['source'],
                    unit['context'],
                    writer)

        for lang in languages:
            with FULLTEXT_INDEX.target_writer(lang = lang.code, buffered = False) as writer:
                for unit in base.filter(translation__language =
                    lang).exclude(target = '').values('checksum', 'target').iterator():
                    Unit.objects.add_to_target_index(
                        unit['checksum'],
                        unit['target'],
                        writer)

