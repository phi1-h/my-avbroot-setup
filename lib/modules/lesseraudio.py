# SPDX-FileCopyrightText: 2024-2025 Andrew Gunnerson
# SPDX-License-Identifier: GPL-3.0-only

from collections.abc import Iterable
import logging
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import override
import zipfile

from lib import modules
from lib.filesystem import CpioFs, ExtFs
from lib.modules import Module, ModuleRequirements


logger = logging.getLogger(__name__)


class LesserAudioModule(Module):
    def __init__(self, zip: Path, sig: Path) -> None:
        super().__init__()

        self.zip: Path = zip
        self.abi: str = modules.host_android_abi()

    @override
    def requirements(self) -> ModuleRequirements:
        return ModuleRequirements(
            boot_images=set(),
            ext_images={'system'},
            selinux_patching=False,
        )

    @override
    def inject(
        self,
        boot_fs: dict[str, CpioFs],
        ext_fs: dict[str, ExtFs],
        sepolicies: Iterable[Path],
    ) -> None:
        logger.info(f'Injecting Lesser Audio: {self.zip}')

        system_fs = ext_fs['system']
        with zipfile.ZipFile(self.zip, 'r') as z:
            for path in z.namelist():
                if not path.endswith('.apk') and not path.endswith('.xml'):
                    continue
                modules.zip_extract(z, path, system_fs)
