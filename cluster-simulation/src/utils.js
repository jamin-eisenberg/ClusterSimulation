export function patchTo(url, val) {
    const requestOptions = {
        method: 'PATCH',
    };
    if (val === undefined) {
        fetch(url, requestOptions)
            .then(response => console.log(response))
    } else {
        if (isNaN(val)) {
            fetch(url + '/0', requestOptions).then(console.log)
        }
        else {
            fetch(url + '/' + val, requestOptions)
                .then(response => console.log(response))
        }
    }
}

export async function getState(url) {
    const requestOptions = {
        method: 'GET',
    };
    return fetch(url + 'state', requestOptions)
}