// comment before
.package(to_ignore: "bad", to_ignore: "https://before")

dependencies: [
        // comment
        .package(name: "c_a", url: "https://c_a"),
        .package(name: "Contact",url: "git@to_ignore"),
        .package(name:"c_b", url:"https://c_b"),
],
to_ignore: [
        .package(name: "bad", url: "https://bad")
],
dependencies: ["to_ignore", "to_ignore"]
dependencies: [
    "to_ignore", "to_ignore"
]
// comment after
.package(to_ignore: "bad", to_ignore: "https://after")
