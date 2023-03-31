// comment
/*
comment on severals lines
*/

to_ignore 'ns:c:1.0.0'

dependencies {
    // comment
    /*
    comment on severals lines
    */
    implementation 'ns_a:c_a:1.0.0'
    to_ignore instruction(include: ['*.jar'], dir: 'libs')
    to_ignore project(path: ':AccessibilityStatementLibrary')

    to_ignore('ns:c:0.0.0') {
        exclude group: 'ns', module: 'c'
        exclude group: 'ns', module: 'c'
    }

    implementation "ns_b:c_b:$version"

    def to_ignore = '4.8.0'
    api "ns_d:c_d:$version"

implementation 'ns_c:c_c:3.3.3'
}
// comment
/*
comment on severals lines
*/

to_ignore 'ns:c:1.0.0'


