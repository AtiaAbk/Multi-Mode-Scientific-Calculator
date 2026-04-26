import streamlit as st
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, solve, sympify


st.set_page_config(page_title="Scientific Calculator", layout="centered")

st.title("Scientific Calculator")



if "display" not in st.session_state:
    st.session_state.display = ""


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


if mode == "Basic UI":
    st.text_input("Display", st.session_state.display, key="screen")

    cols = st.columns(4)

    buttons = [
        "7", "8", "9", "/",
        "4", "5", "6", "*",
        "1", "2", "3", "-",
        "0", ".", "=", "+"
    ]

    for i, button in enumerate(buttons):
        with cols[i % 4]:
            if st.button(button):
                if button == "=":
                    try:
                        st.session_state.display = str(eval(st.session_state.display))
                    except:
                        st.session_state.display = "Error"
                else:
                    st.session_state.display += button

    if st.button("Clear"):
        st.session_state.display = ""


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
                "exp": math.exp
            })
            st.success(result)
        except:
            st.error("Invalid Expression")


elif mode == "Trigonometry":
    func = st.selectbox("Function", ["sin", "cos", "tan"])
    angle = st.number_input("Enter angle")

    if st.button("Calculate"):
        try:
            if angle_mode == "Degree":
                angle = math.radians(angle)

            result = getattr(math, func)(angle)
            st.success(result)
        except:
            st.error("Error")


elif mode == "Complex":
    real = st.number_input("Real part")
    imag = st.number_input("Imaginary part")

    if st.button("Compute Square"):
        z = complex(real, imag)
        st.success(z**2)


elif mode == "Matrix":
    st.write("Enter 2x2 Matrix A")
    a11 = st.number_input("A11")
    a12 = st.number_input("A12")
    a21 = st.number_input("A21")
    a22 = st.number_input("A22")

    A = np.array([[a11, a12], [a21, a22]])

    if st.button("Determinant"):
        st.success(np.linalg.det(A))

    if st.button("Inverse"):
        try:
            st.write(np.linalg.inv(A))
        except:
            st.error("Matrix not invertible")


elif mode == "Equation Solver":
    eq = st.text_input("Enter equation (e.g., x**2 - 4)")

    if st.button("Solve"):
        try:
            x = symbols('x')
            expr = sympify(eq)
            sol = solve(expr)
            st.success(sol)
        except:
            st.error("Invalid Equation")


elif mode == "Graph":
    expr = st.text_input("Enter function of x (e.g., sin(x), x**2 + 3*x)")

    if st.button("Plot Graph"):
        try:
            x = np.linspace(-10, 10, 400)

            y = eval(expr, {"__builtins__": None}, {
                "x": x,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "exp": np.exp,
                "log": np.log,
                "sqrt": np.sqrt
            })

            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.set_title("Graph of " + expr)
            ax.grid()

            st.pyplot(fig)
        except:
            st.error("Invalid Function")


st.caption("Built with Python + Streamlit")