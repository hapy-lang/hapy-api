require.config({ paths: { vs: '../static/node_modules/monaco-editor/min/vs' } });

// elements
var outputContainer = document.getElementById("output");
var pythonCodeContainer = document.getElementById("python_code");

require(['vs/editor/editor.main'], function() {

    monaco.languages.register({
        id: 'hapy'
    });
    monaco.languages.setMonarchTokensProvider('hapy', monarchSettings());

    // Define a new theme that constains only rules that match this language
    monaco.editor.defineTheme('myCoolTheme', {
        base: 'vs',
        inherit: false,
        rules: [
            { token: 'custom-info', foreground: '808080' },
            { token: 'custom-error', foreground: 'ff0000', fontStyle: 'bold' },
            { token: 'custom-notice', foreground: 'FFA500' },
            { token: 'custom-date', foreground: '008800' }
        ]
    });

    window.editor = monaco.editor.create(document.getElementById('container'), {
        value: getCode(),
        language: 'hapy'
    });

    // window.editor = monaco.editor.create(document.getElementById('container'), {
    //     value: getCode(),
    //     language: 'hapy'
    // });

    let select = document.getElementById("themeselect");
    let currentTheme = "vs";
    select.onchange = function() {
        currentTheme = select.options[select.selectedIndex].value;
        monaco.editor.setTheme(currentTheme);
    };
});

function getCode() {
    return [
        "#! lang=hausa",
        "",
        "ayyana gayar() {",
        " nuna('Sannu!');",
        "};",
        "",
        "gayar();"
    ].join("\n");
};

function reset() {
    outputContainer.innerText = "";
    outputContainer.style.borderColor = "initial";
    pythonCodeContainer.innerText = "running..."
}

function loading() {
    document.getElementById("loader").style.display = "block";

    setTimeout(() => {
        document.getElementById("loader").style.display = "none";
    }, 1000)
}
async function save_code(challenge_id = -1) {
    loading();
    let code = window.editor.getValue();


    let req_body = {
        title: "Solution to challenge:" + challenge_id,
        code: code,
        description: "N/A"

    }
    console.log("Sending a request to solution with ID: " + challenge_id)
    fetch("/api/challenges/" + challenge_id + "/solution", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "Authorization": "Bearer " + JSON.parse(localStorage.getItem("hapyland_token"))

        },
        body: JSON.stringify(req_body)

    }).then(async function success(response) {
        if (response.ok) {
            let res = await response.json();
            if (res.status == "success") {

                showToast("Code saved successfully")
            } else {
                showToast("Unable to save")

            }

        } else {
            //console.log(response.status, response)
            showToast("Unable to save")


        }
    }).catch(e => console.log)
}

async function runcode(challenge_id = -1) {

    reset();
    loading();

    let code = window.editor.getValue();
    let compile_only = document.getElementById("compile_only");

    let req_body = {
        code,
        option: "execute_only",
        compile_only: compile_only.checked,
        save: false,
        challenge_id: challenge_id
    }


    fetch('/api/run', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "Authorization": "Bearer " + JSON.parse(localStorage.getItem("hapyland_token"))

        },
        body: JSON.stringify(req_body)
    }).then(async function(response) {
        // ...
        console.log(response);
        if (response.ok) {
            console.log('Code compiled successfully!');
            let res = await response.json();

            console.log(res);

            if (res.status == "error" || res.data.error) {
                outputContainer.innerText = res.data.error;
                outputContainer.style.borderColor = "red";
                pythonCodeContainer.innerText = "ERROR!";
            } else {
                outputContainer.innerText = res.data.python_result;
                pythonCodeContainer.innerText = res.data.python_source;
            }
        } else {
            console.log(response);

            outputContainer.innerText = "ERROR2!";
            outputContainer.style.borderColor = "red";
            pythonCodeContainer.innerText = "ERROR3!";
        }
    }).catch(async function(response) {
        console.log('Code compiled successfully!');
        let res = await response.json();
        console.log(res);
    })

}