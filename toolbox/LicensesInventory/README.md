# Licenses Inventory

Table of Contents
=================		
   * [Licenses inventory](#licenses-inventory)
      * [Disclaimer](#disclaimer)
      * [Developer notice](#developer-notice)
      * [What the tool does](#what-the-tool-does)
      * [Prerequisites](#prerequisites)
      * [Fill the configuration file](#fill-the-configuration-file)
      * [Run the tool](#run-the-tool)
      * [Run the tests](#run-the-tests)
      * [Limits](#limits)
      * [Scenarios](#scenarios)
      * [Example of use](#example-of-use)
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

The tool searches a license for each dependency found in the files to treat.

## Disclaimer

*This is quite experimental feature, with results which must be verified by a human.*
*You must deal with platforms and APIs policies and fullfil them.*

*This is software is distributed on "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.*

*Such caveats are about versions of components (not checked) and version names (not sure they are related to the good components)*

**This is an experimental feature designed and implemented by a blind colleague, you must always keep in mind our [Code of Conduct](https://github.com/Orange-OpenSource/floss-toolbox/blob/dev/CODE_OF_CONDUCT.md) for any issues nor comments, and be benevolent and kind.
This is mandatory.**

## Developer notice

- Unit tests: in *tests/unittests*
- Integration tests: in *tests/integrationtests*
- To test the main: in *sources/test_main.py*
    with the data in *sources/data_to_test_main*

Do not delete the file 'to_add_this_folder_to_git.tmp' in:
    real_data/licenses*
    real_data/no_file

For integrationtest/test_3_print:
- you have to uncomment the first line in the test method to see the displays
- the test does not pass: it is normal, it tests the displaying after testing, you have to comment this line: the test will pass

After executing of the integration tests:
- delete the directories 'real_data/licenses*'
- execute the following commands:

```shell
    git checkout tests\integrationtests\real_data\licenses
    git checkout tests\integrationtests\real_data\licenses_with_errors
    git checkout tests\integrationtests\real_data\licenses_with_retry_after
```

## What the tool does

1. Read the file 'config.ini' ;
2. Read the files to treat ;
3. Extract the dependencies from these files ; 
4. Search in the web a license for each dependency ;
5. Save the licenses ;
6. Save the dependencies on error.

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
```ini
[dependencies]
# Where to find the package manager files above, must be defined, target must exist
path to parse = /absolute/path/to/project_to_test
# The name of the package manager file to process stored above, must be defined
the filenames = go.mod, build.gradle, build.gradle.kts, package.json
# For outputs, must be defined, target must exists
path to store the licenses = /absolute/path/to/project_to_test-licences
# Erros maangement if requests failed
number of authorized successive errors = 2
```

where:
- `path to parse` contains the dependencies manager files
- `the filenames` contains the names of the dependencies manager files to process
- `path to store the licenses` points to a folder containing the result files prefixed by "licenses_" if license has been found or "errors_"  if an error occured (e.g. requests limits in web site, etc)
- `number of authorized successive errors` is the number of succesive errors authorized before ignoring the next dependencies to treat

## Run the tool

```shell
python3 sources/main.py
```

For example, if you define some _Cargo.lock_ file to process in *the filenames* stored at *path to parse*, it will create in *path to store the licenses* a *Cargo_lock_ folder with some outputs (mainly HTML or JSON files) and a *licenses_Cargo.lock.txt* with the licenses of each component found.

## Run the tests
 
To run the tests (all must pass):

```shell
# Integration tests some user inputs
python3 -m pytest -s tests/integrationtests/*.py

# Unit tests 
python3 -m pytest tests/unittests/*.py
```

To run the unit tests, you must get the assets attached as artifacts to [the release you got](https://github.com/Orange-OpenSource/floss-toolbox/releases).
For integration tests, get the *real_data* folder in the *integrationtests* folder and move it to the same folder in your project.
For unit tests, get the *data* folder in the *unittests* folder and move it to the same folder in your project.

Then you will have to update the configuration values defined in all the _config_ files of the data sets.
Indeed, absolute paths are used, so you must look for any "🥜" and replace by the path fragments leading to the folders.

## Limits

The dependencies are always treated in the same order. The downloading can be aborted. For example, a website can limit the number of requests for a done duration. In this case, all the following dependencies will have the same error. For Gradle, we can limit the number of authorized errors to avoid to continue the unuseful downloadings.

## Scenarios

With no error:
- the dependency is saved in the file "licenses_platform.txt"
- the dependency is not saved in the file "errors_platform.txt"

On error:
- the dependency is not saved in the file "licenses_platform.txt"
- the dependency is saved in the file "errors_platform.txt"

## Example of use

The user executes the tools. If dependencies are on error, the tools displays, for each treated platform, the number of new dependencies to treat, the number of dependencies on error and the number of duplicated (dependencies on error which are in the new dependencies)/
The tools asks to the user to treat the dependencies on error or the new dependencies or to quit the program.

If they are only new dependencies, the tools does not display the number of dependencies.
If they are only dependencies on error, the tools does not display the number of dependencies.

So, we can search licenses for dependencies which have not been treated following an error during the downloading.

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