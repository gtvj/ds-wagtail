export default function add_event(element, event, action) {
    $(element).on(event, action);
}
