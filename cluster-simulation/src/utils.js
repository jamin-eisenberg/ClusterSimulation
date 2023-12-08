export function patch_to(url, val) {
    const requestOptions = {
        method: 'PATCH',
    };
    if (val === undefined) {
        fetch(url, requestOptions)
            .then(response => console.log(response))
    } else {
        fetch(url + '/' + val, requestOptions)
            .then(response => console.log(response))
    }
}