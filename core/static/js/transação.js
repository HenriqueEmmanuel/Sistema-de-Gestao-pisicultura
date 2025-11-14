document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-financeiro");

    if (!form) return;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const url = form.action;
        const formData = new FormData(form);
        const feedback = document.getElementById("finance-feedback");

        feedback.innerHTML = `<p style="color: blue;">Salvando...</p>`;

        try {
            const response = await fetch(url, {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (data.status === "sucesso") {
                feedback.innerHTML = `
                    <p style="color: green; font-weight: bold;">
                        Registro salvo com sucesso!
                    </p>
                `;
                form.reset();
            } else {
                feedback.innerHTML = `
                    <p style="color: red; font-weight: bold;">
                        Erro: ${data.mensagem}
                    </p>
                `;
            }
        } catch (err) {
            feedback.innerHTML = `
                <p style="color: red;">
                    Erro inesperado: ${err}
                </p>
            `;
        }
    });
});
