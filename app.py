import streamlit as st
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, solve, sympify


st.set_page_config(page_title="Scientific Calculator", layout="centered")

st.title("Scientific Calculator")


# --- Session State Initialization ---
if "display" not in st.session_state:
    st.session_state.display = ""
if "result" not in st.session_state:
    st.session_state.result = None
if "result_error" not in st.session_state:
    st.session_state.result_error = False


mode = st.sidebar.selectbox("Select Mode", [
    "Basic UI",
    "Scientific",
    "Trigonometry",
    "Complex",
    "Matrix",
    "Equation Solver",
    "Graph"
])

angle_mode = st.sidebar.radio("Angle Mode", ["Degree", "Radian"])


# ──────────────────────────────────────────────
# Basic UI  (number-pad fixed)
# ──────────────────────────────────────────────
if mode == "Basic UI":

    # Read-only display driven entirely by session_state
    st.text_input("Display", value=st.session_state.display,
                  key="screen", disabled=True)

    buttons = [
        "7", "8", "9", "/",
        "4", "5", "6", "*",
        "1", "2", "3", "-",
        "0", ".", "=", "+"
    ]

    cols = st.columns(4)
    for i, button in enumerate(buttons):
        with cols[i % 4]:
            if st.button(button, key=f"btn_{button}_{i}"):
                if button == "=":
                    try:
                        st.session_state.result = str(eval(st.session_state.display))
                        st.session_state.result_error = False
                    except Exception:
                        st.session_state.result = "Error"
                        st.session_state.result_error = True
                else:
                    st.session_state.display += button
   
                    st.session_state.result = None
                st.rerun()

    if st.button("Clear", key="btn_clear"):
        st.session_state.display = ""
        st.session_state.result = None
        st.session_state.result_error = False
        st.rerun()

    # ── Result Section ──
    if st.session_state.result is not None:
        st.markdown("---")
        st.markdown("### 🟰 Result")
        if st.session_state.result_error:
            st.error(f"{st.session_state.result}")
        else:
            st.success(f" {st.session_state.result}")
            # Copy-friendly display
            st.code(st.session_state.result, language=None)


# ──────────────────────────────────────────────
# Scientific
# ──────────────────────────────────────────────
elif mode == "Scientific":
    expr = st.text_input("Enter expression (e.g., sqrt(16), log(10))")

    if st.button("Calculate"):
        try:
            result = eval(expr, {"__builtins__": None}, {
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "pi": math.pi,
                "e": math.e,
                "exp": math.exp,
                "abs": abs,
                "pow": pow,
            })
            st.markdown("---")
            st.markdown("### 🟰 Result")
            st.success(f"{result}")
            st.code(str(result), language=None)
        except Exception as err:
            st.markdown("---")
            st.markdown("### 🟰 Result")
            st.error(f"Invalid Expression — {err}")



elif mode == "Trigonometry":
    func = st.selectbox("Function", ["sin", "cos", "tan"])
    angle = st.number_input("Enter angle", value=0.0)

    if st.button("Calculate"):
        try:
            angle_rad = math.radians(angle) if angle_mode == "Degree" else angle
            result = getattr(math, func)(angle_rad)
            st.markdown("---")
            st.markdown("### 🟰 Result")
            st.success(f"{func}({angle}°) = {result}" if angle_mode == "Degree"
                       else f"{func}({angle} rad) = {result}")
            st.code(str(result), language=None)
        except Exception as err:
            st.markdown("---")
            st.markdown("### 🟰 Result")
            st.error(f"Error — {err}")



elif mode == "Complex":
    real = st.number_input("Real part", value=0.0)
    imag = st.number_input("Imaginary part", value=0.0)

    op = st.selectbox("Operation", ["Square", "Square Root", "Modulus", "Conjugate"])

    if st.button("Compute"):
        z = complex(real, imag)
        if op == "Square":
            res = z ** 2
        elif op == "Square Root":
            res = cmath.sqrt(z)
        elif op == "Modulus":
            res = abs(z)
        else:
            res = z.conjugate()

        st.markdown("---")
        st.markdown("### 🟰 Result")
        st.success(f"{op} of ({real} + {imag}j) = {res}")
        st.code(str(res), language=None)



elif mode == "Matrix":
    st.write("Enter 2×2 Matrix A")
    col1, col2 = st.columns(2)
    with col1:
        a11 = st.number_input("A[1,1]", value=1.0)
        a21 = st.number_input("A[2,1]", value=0.0)
    with col2:
        a12 = st.number_input("A[1,2]", value=0.0)
        a22 = st.number_input("A[2,2]", value=1.0)

    A = np.array([[a11, a12], [a21, a22]])

    bcol1, bcol2 = st.columns(2)

    with bcol1:
        if st.button("Determinant"):
            det = np.linalg.det(A)
            st.markdown("---")
            st.markdown("### 🟰 Result — Determinant")
            st.success(f"det(A) = {det:.6g}")
            st.code(str(det), language=None)

    with bcol2:
        if st.button("Inverse"):
            st.markdown("---")
            st.markdown("### 🟰 Result — Inverse")
            try:
                inv = np.linalg.inv(A)
                st.success("A⁻¹ =")
                st.dataframe(inv)
            except np.linalg.LinAlgError:
                st.error("Matrix is not invertible (det = 0)")

    if st.button("Eigenvalues"):
        vals, vecs = np.linalg.eig(A)
        st.markdown("---")
        st.markdown("### 🟰 Result — Eigenvalues")
        st.success(f"λ = {vals}")
        st.code(str(vals), language=None)


# ──────────────────────────────────────────────
# Equation Solver
# ──────────────────────────────────────────────
elif mode == "Equation Solver":
    eq = st.text_input("Enter equation in x (e.g., x**2 - 4  or  x**3 - x - 2)")

    if st.button("Solve"):
        try:
            x = symbols('x')
            expr = sympify(eq)
            sol = solve(expr, x)
            st.markdown("---")
            st.markdown("### 🟰 Result")
            if sol:
                st.success(f"Solution(s): {sol}")
                st.code(str(sol), language=None)
            else:
                st.warning("No real solution found.")
        except Exception as err:
            st.markdown("---")
            st.markdown("### 🟰 Result")
            st.error(f"Invalid Equation — {err}")


# ──────────────────────────────────────────────
# Graph
# ──────────────────────────────────────────────
elif mode == "Graph":
    expr = st.text_input("Enter function of x (e.g., sin(x), x**2 + 3*x)")
    x_min = st.number_input("X min", value=-10.0)
    x_max = st.number_input("X max", value=10.0)

    if st.button("Plot Graph"):
        try:
            x = np.linspace(x_min, x_max, 500)
            y = eval(expr, {"__builtins__": None}, {
                "x": x,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "exp": np.exp,
                "log": np.log,
                "log10": np.log10,
                "sqrt": np.sqrt,
                "abs": np.abs,
                "pi": np.pi,
                "e": np.e,
            })

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x, y, color="#4f8ef7", linewidth=2)
            ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
            ax.axvline(0, color="gray", linewidth=0.8, linestyle="--")
            ax.set_title(f"y = {expr}", fontsize=14)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True, alpha=0.3)
            fig.tight_layout()

            st.markdown("---")
            st.markdown("### Graph")
            st.pyplot(fig)
        except Exception as err:
            st.markdown("---")
            st.markdown("### Graph")
            st.error(f"Invalid Function — {err}")


st.caption("Built with Python + Streamlit")
