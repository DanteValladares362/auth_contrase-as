from flask import Flask, request, jsonify, render_template_string
import secrets

app = Flask(__name__)
r = secrets.SystemRandom()
W = ["Tigre", "Luna", "Roble", "Cafe", "Nube", "Fuego", "Piedra", "Volcan", "Mar"]
S = "!@#$%&*?"
L = str.maketrans("aeios", "4310$")

def gen(k):
    k = k.strip().replace(" ", "")
    k = k[:1].upper() + "".join(c.translate(L) if r.random() < .5 else c for c in k[1:].lower())
    return f"{k}{r.choice(S)}{r.choice(W)}{r.randint(100, 999)}{r.choice(S)}{r.choice(W).lower()}{r.randint(0, 9)}"

@app.route("/gen")
def g():
    k = request.args.get("k", "")
    return jsonify([gen(k) for _ in range(3)] if k.strip() else [])

HTML = """<!doctype html><meta charset=utf-8><title>Contraseñas S3guR4$</title>
<style>
body{font-family:sans-serif;max-width:480px;margin:30px auto}
input{width:100%;padding:10px;margin:6px 0;box-sizing:border-box;font-size:16px}
.r{padding:8px;margin:4px 0;border-radius:6px;color:#fff;background:#d33;transition:.3s}
.r.ok{background:#2a2}
.e{padding:8px;margin:4px 0;background:#eee;cursor:pointer;font-family:monospace;border-radius:6px}
</style>
<h2>Validador de contraseñas</h2>
<input id=p placeholder="Escribe tu contraseña" oninput=chk()>
<div id=rules></div><b id=s></b>
<h3>Generador</h3>
<input id=k placeholder="Palabra clave (ej: gato)" oninput=gen()>
<div id=ex></div>
<script>
const R=[["12 o más caracteres",v=>v.length>=12],
["Mayúsculas (A-Z)",v=>/[A-Z]/.test(v)],
["Minúsculas (a-z)",v=>/[a-z]/.test(v)],
["Números (0-9)",v=>/\\d/.test(v)],
["Símbolos (!@#$%...)",v=>/[^A-Za-z0-9]/.test(v)],
["Sin palabras obvias ni repeticiones",v=>v&&!/password|contrase|123|qwerty|admin|abc|(.)\\1\\1/i.test(v)]];
rules.innerHTML=R.map(x=>`<div class=r>${x[0]}</div>`).join("");
function chk(){let n=0;R.forEach((x,i)=>{let o=x[1](p.value);n+=o;rules.children[i].classList.toggle("ok",o)});
s.textContent=`Cumple ${n}/${R.length}`}
async function gen(){let a=await (await fetch("/gen?k="+encodeURIComponent(k.value))).json();
ex.innerHTML=a.map(x=>`<div class=e onclick="p.value=this.textContent;chk()">${x}</div>`).join("")}
chk()
</script>"""

@app.route("/")
def i():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)