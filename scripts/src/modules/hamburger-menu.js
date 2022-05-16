import debounce from "./debounce.js";

export default function () {
    let $headerMenu = document.querySelector('[data-id="site-menu"]');
    let $headerMenuList = document.querySelector('[data-id="site-menu-list"]');
    let $headerElementsToHide = document.querySelectorAll(
        '[data-isSearch="false"]'
    );
    let $searchListItem = document.querySelector("#site-menu-search");
    let $globalSearchButton = document.querySelector("#gs-show-hide");
    if (!$headerMenu || !$headerMenuList || !$searchListItem) {
        return;
    }

    let isGlobalSearchFocused = function () {

        if(!$globalSearchButton) {
            return false;
        }

        // This has to be calculated outside of placeGlobalSearchAtIndex(), as I believe the debounce delay was causing an document.activeElement to be incorrect
        return $globalSearchButton.id === document.activeElement.id;
    };

    let placeGlobalSearchAtIndex = function (newIndex, isFocused) {
        if (newIndex === "end") {
            newIndex = $headerMenuList.childNodes.length - 1;
        }

        // Only move the element if it's in the wrong place
        if (
            $headerMenuList.childNodes[newIndex].id !== $searchListItem.id
        ) {
            $headerMenuList.insertBefore(
                $searchListItem,
                $headerMenuList.childNodes[newIndex]
            ); //IE11 compatible prepend

            isFocused ? $globalSearchButton.focus() : null;
        }
    };

    let $showHideListItem = document.createElement("li");
    $showHideListItem.classList.add("header__nav-list-item");
    $showHideListItem.setAttribute("data-id", "menu-show-hide-button");

    let $showHideButton = document.createElement("button");
    $showHideButton.innerHTML =
        '<span class="sr-only">Show or hide navigation menu</span>';
    $showHideButton.classList.add("header__show-hide-button");
    $showHideButton.setAttribute("aria-expanded", false);

    $showHideListItem.appendChild($showHideButton);

    $headerMenuList.insertBefore(
        $showHideListItem,
        $headerMenuList.childNodes[0]
    ); //IE11 compatible prepend

    if (window.innerWidth >= 768) {
        $showHideButton.hidden = "true";
    } else {
        // Move global search button to the 2nd DOM element, so that the CSS can work as intended.
        placeGlobalSearchAtIndex(1, isGlobalSearchFocused());
    }

    let ariaControls = "";
    for (let i = 0; i < $headerElementsToHide.length; i++) {
        let id = `menu-item-${i}`;
        $headerElementsToHide[i].id = id;
        ariaControls += ` ${id}`;
        if (window.innerWidth < 768) {
            $headerElementsToHide[i].hidden = "true";
        }
    }

    $showHideButton.setAttribute("aria-controls", ariaControls);

    $showHideButton.addEventListener("click", function () {
        let ariaExpandedBoolean =
            $showHideButton.getAttribute("aria-expanded") === "true";
        $showHideButton.setAttribute("aria-expanded", !ariaExpandedBoolean);

        for (let i = 0; i < $headerElementsToHide.length; i++) {
            $headerElementsToHide[i].hidden = !$headerElementsToHide[i].hidden;
        }
    });

    let setMenuItemsHidden = function (hidden) {
        for (let i = 0; i < $headerElementsToHide.length; i++) {
            $headerElementsToHide[i].hidden = hidden;
        }
    };

    window.addEventListener(
        "resize",
        debounce(() => {
            let ariaExpanded = $showHideButton.getAttribute("aria-expanded");

            if (window.innerWidth < 768) {
                $showHideButton.hidden = false;

                if (ariaExpanded === "false") {
                    setMenuItemsHidden(true);
                } else {
                    setMenuItemsHidden(false);
                }

                placeGlobalSearchAtIndex(1, isGlobalSearchFocused());
            } else {
                // Hide button on desktop, but keep menu items visible
                $showHideButton.hidden = true;
                setMenuItemsHidden(false);
                placeGlobalSearchAtIndex("end", isGlobalSearchFocused());
            }
        }, 200)
    );
}
