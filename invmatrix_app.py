import streamlit as st
from fractions import Fraction
from sympy import Matrix, latex, Rational, sympify
from sympy.parsing.sympy_parser import parse_expr
import ast

st.title("Matrix Operations with Rational Numbers and LaTeX Display")

st.markdown("""
Enter matrices A and B using Python list format with fractional elements if needed.  
Examples:
- `[[1, 2], [3, 4]]`
- `[[1/2, 3/4], [-2/3, 5]]`
- `[[0.5, 1.25], [1/3, 2/7]]`
""")

# Matrix input areas
A_input = st.text_area("Matrix A", height=100)
B_input = st.text_area("Matrix B", height=100)

# Parse input string into a matrix of Rational numbers
def parse_matrix(input_text):
    try:
        # Safely parse using ast.literal_eval
        raw = ast.literal_eval(input_text)
        matrix = []
        for row in raw:
            matrix_row = []
            for item in row:
                # Convert each entry to Rational via sympy
                val = sympify(item, rational=True)
                if isinstance(val, float):  # convert float to rational if needed
                    val = Rational(val).limit_denominator()
                matrix_row.append(val)
            matrix.append(matrix_row)
        return Matrix(matrix)
    except Exception as e:
        st.error(f"Invalid matrix input: {e}")
        return None

# Display matrix in LaTeX
def display_matrix_latex(matrix, label):
    st.markdown(f"**{label}:**")
    st.latex(latex(matrix))

# Parse matrices
A = parse_matrix(A_input) if A_input else None
B = parse_matrix(B_input) if B_input else None

if st.button("Compute"):
    if A:
        display_matrix_latex(A, "Matrix A")
        if A.det() != 0:
            InvA = A.inv()
            display_matrix_latex(InvA, "Inverse of A")
        else:
            st.warning("Matrix A is not invertible (det = 0)")

    if B:
        display_matrix_latex(B, "Matrix B")
        if B.det() != 0:
            InvB = B.inv()
            display_matrix_latex(InvB, "Inverse of B")
        else:
            st.warning("Matrix B is not invertible (det = 0)")

    if A and B:
        try:
            AB = A * B
            display_matrix_latex(AB, "A × B")
        except Exception as e:
            st.error(f"Error computing A × B: {e}")

        try:
            BA = B * A
            display_matrix_latex(BA, "B × A")
        except Exception as e:
            st.error(f"Error computing B × A: {e}")
