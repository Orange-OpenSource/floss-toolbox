# Licenses Inventory

Table of Contents
=================		
   * [Licenses inventory](#licenses-inventory)			
      * [Disclaimer](#disclaimer)			
      * [Prerequisites](#prerequisites)			
      * [Fill the configuration file](#fill-the-configuration-file)			
      * [Run the tool](#run-the-tool)
      * [Run the tests](#run-the-tests)
      * [Managed platforms and environments](#managed-platforms)
         * [Go with go.mod](#go-language)
         * [Gradle with build.gradle(.kts)](#gradle-environment)
         * [Rust with Cargo.lock](#rust-environment)		 
         * [JavaScript / Node.js with package.json](#javascript--nodejs-environment)
         * [Swift with Package.swift](#swift--spm-environment)
         * [Dart / Flutter with pubspec.yaml](#dart--flutter-environment)		 		 		 
      * [Notes](#notes)

# Licenses inventory

_Keywords: #licenses #SPM #Gradle #Maven #NPMJS #package #Cocoapods #pubspec #gomod #Cargo #crates_

## Disclaimer

*This is quite experimental feature, with results which must be verified by a human.*
*You must deal with platforms and APIs policies and fullfil them.*

*This is software is distributed on "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.*

*Such caveats are about versions of components (not checked) and version names (not sure they are related to the good components)*

## Prerequisites

- _Python_ version **3.7**
- _Python_ modules like _requests_, _xmltodict_, _pytests_ and _beautiful soup_

```shell
pip install -r requirements.txt
```

This project expects to have the third-party elements above available and already added in your system.
None of them have been modified nor distributed.
It could be seen as a [composition](https://www.gnu.org/licenses/gpl-faq.html#MereAggregation) of components (except maybe for _pytests_), you can get licenses details in THIRD-PARTY.txt and licenses folder.

For integration tests, you must download the archive assets attaches in this current release, extract the ZIP folder you got called *toolbox/LicensesInventory/tests/integrationtests/data* and place the *data* folder in _tests/integrationtests_ folder. Otherwise tests won't work and dry-run script will fail!

To check preconditions, run:

```shell
bash dry-run.sh
```

## Fill the configuration file

Before to use the tools, the file 'config.ini' is at the root of the project, you have to personalize this file.

For example:
```text
[dependencies]
# Where to find the package manager file above
path to parse = /absolute/path/to/project_to_test
# The name of the package manager file to process store above
the filenames = go.mod
# For outputs
path to store the licenses = /absolute/path/to/project_to_test-licences
```

where:
- `path to parse` contains the dependencies manager files
- `the filenames` contains the names of the dependencies manager files to process
- `path to store the licenses` points to a folder containing the result files

## Run the tool

```shell
python3 sources/main.py
```

## Run the tests
 
To run integration tests:

```shell
 python3 -m pytest tests/integrationtests/*.py
```

## Managed platforms

### Go language

`go.mod` files are managed.
Depending to the `go.mod` definitions implementation, some cases can be applied:

1. **github.com** will be requested if dependency starts by _github.com_
2. **pkg.go.dev** will be requested for other cases

For example:

```text
module ...

go 1.15

require (
	emperror.dev/errors v0.4.2                                          // <--- Request pkg.go.dev
	github.com/antihax/optional v1.0.0                                  // <--- Request github.com
	golang.org/x/tools v0.0.0-20201014231627-1610a49f37af // indirect   // <--- Not managed
	k8s.io/api v0.20.2                                                  // <--- Request pkg.go.dev
	sigs.k8s.io/controller-runtime v0.7.2                               // <--- Request pkg.go.dev
)
```

### Gradle environment

`build.gradle` and `build.gradle.kts` files are managed.
Some platforms are requested like _Maven Central_ (**search.maven.org**) and _GitHub_ (through **api.github.com**).

**Warning: unstable feature with maybe _Maven Central_ troubles, missing results sometimes*

Managed (tested) keywords are: 
```groovy
    implementation 'ns_d:c_d:4.4.4'
    compile 'ns_e:c_e:5.5.5'
    api 'ns_f:c_f:6.6.6'
    testImplementation 'ns_g:c_g:7.7.7'
    androidTestImplementation 'ns_h:c_h:8.8.8'
    annotationProcessor 'ns_i:c_i:9.9.9'
    compileOnly 'ns_j:c_j:10.10.10'
```

But the following are not managed yet:
```groovy
    implementation('...') {
        exclude module: '...'
    }

    androidTestImplementation('...') {
        exclude group: '...', module: '...'
    }
```

### Rust environment

`Cargo.lock` files are also managed.
_Crates_ (**crates.io**) platform will be requested for each dependency found.

### JavaScript / Node.js environment

`package.json` files can be parsed too.
The platform **npmjs.org**_** wll be requested for each dependency found.

### Swift / SPM environment

If you use _Swift Package Manager_, you can parse `Package.swift` file.
The tool will extract the dependency URLs and request some forges, e.g. **_**github.com**.

### Dart / Flutter environment

The `pubspec.yaml` files can also be processed.
For each dependency found, the **pub.dev**_** platform will be requested.

### CocoaPods case

The `Podfile` files can also be processed and the **cocoapods.org** website will be used.

## Notes

The tool downloads a file for each dependency it found in the dependency manager file.
These files containing the licenses are in directory like 'licenses/sub_folder', where 'sub_folder' is created for each platform: Gradle, Rust, etc.

A file 'licenses.txt' is created in the folder 'licenses'. 
This file contains the list of the licenses for each dependency.
To personalize this folder, use 'config.ini'.

Beware of your proxys or public IP address to not be blocked by such platforms, and avoid flooding them.
