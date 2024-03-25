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

# Version.............: 2.0.0
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
# Use SPDX short identifier as key, full name and URL of license text as values
LICENSES = {
    "Other": ["Other", "<to be completed>"], # If not listed bellow in a known exact SPDX short identifier

    "Apache-2.0": ["Apache 2.0 License", "https://opensource.org/license/apache-2-0"],
    "MIT": ["MIT License", "https://opensource.org/license/mit"],

    "0BSD": ["BSD Zero-Clause License", "https://opensource.org/license/0bsd"],
    "BSD-2-Clause": ["Free BSD License", "https://opensource.org/license/bsd-2-clause"],
    "BSD-3-Clause": ["BSD New License", "https://opensource.org/license/bsd-3-clause"],
    "BSD-3-Clause-No-Military-License": ["BSD 3-Clause No Military License", "https://spdx.org/licenses/BSD-3-Clause-No-Military-License.html"],
    "BSD-3-Clause-No-Nuclear-License": ["BSD 3-Clause No Nuclear License", "https://spdx.org/licenses/BSD-3-Clause-No-Nuclear-License.html"],
    "BSD-4-Clause": ["BSD Original License", "https://spdx.org/licenses/BSD-4-Clause.html"], # Or also "BSD Old"
    
    "EPL-2.0": ["Eclipse Public License 2.0", "https://opensource.org/license/epl-2.0"],
    "MPL-2.0": ["Mozilla Public License 2.0", "https://opensource.org/license/mpl-2-0"],
    "LGPL-2.0-only": ["GNU Library General Public License 2.0", "https://opensource.org/license/lgpl-2-0"],
    "LGPL-2.1": ["GNU Library General Public License 2.1", "https://opensource.org/license/lgpl-2-1"],
    "LGPL-3.0-only": ["GNU Library General Public License 3.0", "https://opensource.org/license/lgpl-3-0"],

    "GPL-2.0": ["GNU General Public License version 2", "https://opensource.org/license/gpl-2-0"],
    "GPL-3.0-only": ["GNU General Public License version 3", "https://opensource.org/license/gpl-3-0"],
    "AGPL-3.0-only": ["GNU Affero General Public License version 3", "https://opensource.org/license/agpl-v3"],
    
    "SSPL-1.0": ["Server Side Public License v1", "https://spdx.org/licenses/SSPL-1.0.html"],
    "BUSL-1.1": ["Business Source License 1.1", "https://spdx.org/licenses/BUSL-1.1.html"],
    "FSL-1.1-Apache-2.0": ["Functional Source License, Version 1.1, Apache 2.0 Future License", "https://fsl.software/"],
    "FSL-1.1-MIT": ["Functional Source License, Version 1.1, MIT Future License", "https://fsl.software/"],
    "RSALv2": ["Redis Source Available License 2.0", "https://redis.com/legal/rsalv2-agreement/"],

    "prosperity-2.0 ": ["Prosperity Public License 2.0", "https://github.com/licensezero/prosperity-public-license/blob/v2.0.0/LICENSE.mustache"],
    "Unlicense": ["The Unlicense License", "https://unlicense.org/"],
    "Hippocratic-2.1": ["Hippocratic License 2.1", "https://spdx.org/licenses/Hippocratic-2.1.html"]
}

LICENSES_NAMES = list(LICENSES)