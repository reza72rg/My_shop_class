'use strict';
{
    const inputTags = ['BUTTON', 'INPUT', 'SELECT', 'TEXTAREA'];
    const modelName = document.getElementById('django-admin-form-add-constants').dataset.modelName;
    if (modelName) {
        const form = document.getElementById(modelName + '_form');
        for (const element of form.elements) {
            // HTMLElement.offsetParent returns null when the element is not
            // rendered.
            if (inputTags.includes(element.tagName) && !element.disabled && element.offsetParent) {
                element.focus();
                break;
            }
        }
    }
}

$(document).ready(function(){
    $("#productimage_set-group .add-row").hide();
    $(".column-image_cropping_info").hide();
    $(".dynamic-productimage_set td.delete").css("float", "right");
})