/**
 * Redirects the user to a specified endpoint.
 * @param {string} endpoint_name - The name of the endpoint to navigate to.
 */
function action(endpoint_name) {
    window.location.replace('/' + endpoint_name); // Replaces the current page with the specified endpoint.
}

/**
 * Redirects the user to the '/demo' endpoint.
 * @param {string} code - (Unused parameter) This parameter is not used in the function.
 */
function redirect_to_demo(code) {
    window.location.replace('/demo'); // Replaces the current page with the '/demo' endpoint.
}
