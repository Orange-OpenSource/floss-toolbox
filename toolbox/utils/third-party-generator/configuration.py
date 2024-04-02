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

# Version.............: 3.0.0
# Since...............: 12/03/2024
# Description.........: Just to list managed licenses and share values between scripts

sys.path.append('../_')
from licenses import *

# Some configuration
# ------------------

DEFAULT_PROMPT_RESULT_FILE = "components.csv.result"
DEFAULT_PROMPT_RESULT_FILE_DELIMITER = ";"
DEFAULT_AVOID_FIELD_SYMBOL = "?"