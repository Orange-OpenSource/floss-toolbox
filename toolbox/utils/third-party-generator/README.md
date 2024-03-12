# Utils

# Generate THIRD-PARTY.md from user inputs

## Prerequisites

- Python 3.8

## Description

Sometimes as open source referent or developer, we need to define file listing third-party components.
This type of file must contain, for each component, its name, copyright, license (with URL pointing to its text) and also the version and the copyright owners.
It can be a bit boring and time-burning to fill each time the text or markdown file, that is the reason why this tool has been defined.

### Ask inputs from user

A first script will ask the user for details about the components he or she wants to add in the final THIRD-PARTY file.
To do that:
```shell
python3.8 third-party-prompt.py
```

This Python script will first check if some previous file still exists, i.e. if previous data can be reused (because the operation was paused before).
If the file exists, the script will prompt the user to keep or get rid of it (default).
Once the script completes, a local CSV file must appear or be updated (named *components.csv.result*).

### Generate the THIRD-PARTY file

Then once some CSV file exists, defined thanks to the previous script or for example given by someone else who already made a list, the other script can be used
so as to iterate on each component and build the final Markdown file.

```shell
# --file: the path to the CSV file containing the details
# --delimiter: to define how to split each row fields. Do not forget to escape it if ';'
python3.8 third-party-generator.py --file components.csv.result --delimiter \;
```

### About the CSV file

The CSV file produced by the script *third-party-prompt.py* or processed by *third-party-generator.py* must follow the format above:

```csv
name;repository;licenseName;copyright;version
```

Meaning:
- ";" symbol as delimiter
- name: the name of the component
- repository: the hyperlink to the repository to get the sources for the readers
- licenseName: the name of the license in SPDX short-identifier (cf *licenses.py*)
- copyright: the copyright owners
- version: the verison of the component


For example, with the CSV file bellow
```csv
SwiftUI-Flow;https://github.com/tevelee/SwiftUI-Flow;MIT;Copyright (c) 2023 Laszlo Teveli;1.2.0
BottomSheet;https://github.com/lucaszischka/BottomSheet;MIT;Copyright (c) 2021-2022 Lucas Zischka;3.1.1
DeclarationAccessibility;https://github.com/Orange-OpenSource/accessibility-statement-lib-ios;Apache-2.0;Copyright (c) 2021-2023 Orange SA;1.2.0
```

the produced Markdown (called *THIRD-PARTY.md.result*) will be:
```markdown
\# Third Party Softwares

This document contains the list of Third Party Softwares along with the license information.

Third Party Software may impose additional restrictions and it is the user's responsibility to ensure that they have met the licensing
requirements of the relevant license of the Third Party Software they are using.

\## SwiftUI-Flow

Version 1.2.0

Copyright Copyright (c) 2023 Laszlo Teveli

**SwiftUI-Flow** is distributed under the terms and conditions of the [MIT License](https://opensource.org/license/mit).
You may download the source code on the [following website](https://github.com/tevelee/SwiftUI-Flow).


\## BottomSheet

Version 3.1.1

Copyright Copyright (c) 2021-2022 Lucas Zischka

**BottomSheet** is distributed under the terms and conditions of the [MIT License](https://opensource.org/license/mit).
You may download the source code on the [following website](https://github.com/lucaszischka/BottomSheet).


\## DeclarationAccessibility

Version 1.2.0

Copyright Copyright (c) 2021-2023 Orange SA

**DeclarationAccessibility** is distributed under the terms and conditions of the [Apache-2.0 License](https://opensource.org/license/apache-2-0).
You may download the source code on the [following website](https://github.com/Orange-OpenSource/accessibility-statement-lib-ios).
```

### About the licenses.py file

There is plenty of licenses and also a lot of standards. It can be a pain or time-consuming to let the user write the license in use for a component,
then find the URL pointing to the license text and write it. In fact, such details are still known so we can let the user choose within list items.
The *licenses.py* file lists main licenses we can meet during audits. Each entry in this dictionary has a license name in SPDX short-identifier format and the URL pointing to the license text. Thus these details will be added in the THIRD-PARTY file.
