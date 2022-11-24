export default function remove_mobile_tracking() {
    const Stories_body = document.querySelector(".stories-container__main");
    const section_headings = document.querySelectorAll(".section-separator__heading");

    Array.prototype.forEach.call(section_headings, item => {
        item.removeAttribute("data-component-name");
        item.removeAttribute("data-link-type");
        item.removeAttribute("data-position");
        item.removeAttribute("data-link");
    });

    Stories_body.removeEventListener("click", e => {
        mobile_section_tracking(e);
    })
}
