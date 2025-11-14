document.getElementById("form-viveiro").addEventListener("submit", async function (e) {
    e.preventDefault();  // impede o redirecionamento

    let form = e.target;
    let url = form.action;

    let formData = new FormData(form);

    let feedback = document.getElementById("viveiro-feedback");
    feedback.innerHTML = "<p style='color: blue;'>Processando...</p>";

    try {
        let response = await fetch(url, {
            method: "POST",
            body: formData,
        });

        let data = await response.json();

        if (data.status === "sucesso") {
            feedback.innerHTML =
                `<p style="color: green; font-weight: bold;">Tanque cadastrado com sucesso!</p>`;
            form.reset();
        } else {
            feedback.innerHTML =
                `<p style="color: red; font-weight: bold;">Erro: ${data.mensagem}</p>`;
        }

    } catch (error) {
        feedback.innerHTML =
            `<p style="color: red;">Erro inesperado: ${error}</p>`;
    }
});
