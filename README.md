# 🧹 Autodesk Full Cleaner

**Limpieza profunda y automatizada de Autodesk en Windows: desinstalación en lote + limpieza de residuos.**

> ✅ Ideal para técnicos, empresas y usuarios que quieren un sistema totalmente libre de Autodesk, sin rastros ni conflictos.

---

## 📦 Características Principales

- **Desinstalación masiva automática**  
  El script PowerShell (`UninstallAutodesk.ps1`) detecta y desinstala silenciosamente todos los productos Autodesk instalados usando el registro de Windows.
- **Limpieza de residuos avanzada**  
  El script Python (`remove_autodesk.py`) elimina carpetas huérfanas, archivos temporales y claves de registro sobrantes que dejan los desinstaladores oficiales.
- **Manejo de errores**  
  Muestra productos que no han podido desinstalarse o carpetas que no pudieron eliminarse.
- **Úsalo por separado o en conjunto**  
  Ejecuta primero la desinstalación y después la limpieza para un “formateo Autodesk” total.

---

## 🚀 **Cómo usar Autodesk Full Cleaner**

### 1️⃣ Desinstalación masiva (PowerShell)
1. Abre **PowerShell como administrador**.
2. Permite temporalmente la ejecución de scripts:
    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope Process
    ```
3. Ejecuta el script:
    ```powershell
    .\UninstallAutodesk.ps1
    ```
4. Confirma la desinstalación cuando se te pregunte.

### 2️⃣ Limpieza profunda de residuos (Python)
1. Asegúrate de tener Python 3.x instalado.
2. Ejecuta el limpiador:
    ```bash
    python remove_autodesk.py
    ```
    > **Nota:** Ejecuta como administrador para máxima efectividad (especialmente en Windows 10/11).

---

## 📝 **Recomendaciones**

- **Desinstala primero, limpia después.**
- Si aparecen errores de permisos, asegúrate de tener privilegios de administrador.
- Revisa los resultados: el script informará sobre cualquier producto o residuo no eliminado.

---

## ⚠️ **Descargo de responsabilidad**
Este proyecto se proporciona “tal cual”, sin garantía de ningún tipo. Úsalo bajo tu propio riesgo.  
**Recomendamos siempre realizar una copia de seguridad de tus datos antes de usar cualquier herramienta de limpieza profunda.**

---

### 👨‍💻 Autor principal

Desarrollado por **Slider66** (2025).

---

## 🙋‍♂️ **Contribuciones y mejoras**

Pull requests y sugerencias son bienvenidas. Si tienes ideas para nuevos módulos (por ejemplo, soporte para otras marcas de software), ¡contribuye!
