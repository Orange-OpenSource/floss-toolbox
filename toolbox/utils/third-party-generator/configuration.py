#!/usr/bin/python3
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) Orange SA
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license,
# the text of which is available at https://opensource.org/license/apache-2-0
# or see the "LICENSE.txt" file for more details.
#
# Authors: See CONTRIBUTORS.txt
# Software description: A toolbox of scripts to help work of forges admins and open source referents

# Version.............: 1.3.0
# Since...............: 12/03/2024
# Description.........: Just to list managed licenses and share values between scripts

# Some configuration
# ------------------

DEFAULT_PROMPT_RESULT_FILE = "components.csv.result"
DEFAULT_PROMPT_RESULT_FILE_DELIMITER = ";"
DEFAULT_AVOID_FIELD_SYMBOL = "?"

# Licenses to manage
# ------------------

# Please refer to https://opensource.org/licenses or https://spdx.org/licenses/
# Use SPDX short identifier as key, URL of license text as value
LICENSES = {
    "Other": "<to be completed>",                                   # If not listed bellow in this exact SPDX short identifier
    "MIT": "https://opensource.org/license/mit",                    # MIT
    "0BSD": "https://opensource.org/license/0bsd",                  # Zero-Clause BSD
    "BSD-2-Clause": "https://opensource.org/license/bsd-2-clause",  # FreeBSD / BSD 2-Clause
    "BSD-3-Clause": "https://opensource.org/license/bsd-3-clause",  # New BSD / BSD 3-Claise
    "BSD-4-Clause": "https://spdx.org/licenses/BSD-4-Clause.html",  # Original BSD / Old BSD / BSD 4-Clause
    "Apache-2.0": "https://opensource.org/license/apache-2-0",      # Apache 2.0
    "MPL-2.0": "https://opensource.org/license/mpl-2-0",            # Mozilla Public License 2.0
    "EPL-2.0": "https://opensource.org/license/epl-2.0",            # Eclipse Public License 2.0
    "LGPL-2.0-only": "https://opensource.org/license/lgpl-2-0",     # GNU Library General Public License 2.0
    "LGPL-2.1": "https://opensource.org/license/lgpl-2-1",          # GNU Library General Public License 2.1
    "LGPL-3.0-only": "https://opensource.org/license/lgpl-3-0",     # GNU Library General Public License 3.0
    "GPL-2.0": "https://opensource.org/license/gpl-2-0",            # GNU General Public License version 2
    "GPL-3.0-only": "https://opensource.org/license/gpl-3-0",       # GNU General Public License version 3
    "AGPL-3.0-only": "https://opensource.org/license/agpl-v3",      # GNU Affero General Public License version 3
    "SSPL-1.0": "https://spdx.org/licenses/SSPL-1.0.html",          # Service Side Public License v1
    "BUSL-1.1": "https://spdx.org/licenses/BUSL-1.1.html",          # Business Source License 1.1
    "FSL-1.1-Apache-2.0": "https://fsl.software/",                  # Functional Source License, Version 1.1, Apache 2.0 Future License
    "FSL-1.1-MIT": "https://fsl.software/",                         # Functional Source License, Version 1.1, MIT Future License
    "RSALv2": "https://redis.com/legal/rsalv2-agreement/",          # Redis Source Available License 2.0
    "prosperity-2.0 ": "https://github.com/licensezero/prosperity-public-license/blob/v2.0.0/LICENSE.mustache", # Prosperity Public License 2.0
    "Unlicense": "https://unlicense.org/",                          # The Unlicense
    "Hippocratic-2.1": "https://spdx.org/licenses/Hippocratic-2.1.html", # Hippocratice License 2.1
    "BSD-3-Clause-No-Military-License": "https://spdx.org/licenses/BSD-3-Clause-No-Military-License.html", # BSD 3-Clause No Military License
    "BSD-3-Clause-No-Nuclear-License": "https://spdx.org/licenses/BSD-3-Clause-No-Nuclear-License.html" # BSD 3-Clause No Nuclear License
}
LICENSES_NAMES = list(LICENSES)