function hide_program_elements(object, section, section_title) {
    if (object.innerText === section_title) {
        console.log("Setting section")
        object.innerText = section
    } else {
        console.log("Setting section_title")
        object.innerText = section_title
    }
}
