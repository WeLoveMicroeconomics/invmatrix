import streamlit as st
from sympy import Matrix, latex, Rational, sympify
import ast
import pandas as pd

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
        raw = ast.literal_eval(input_text)
        matrix = []
        for row in raw:
            matrix_row = []
            for item in row:
                val = sympify(item, rational=True)
                if isinstance(val, float):
                    val = Rational(val).limit_denominator()
                matrix_row.append(val)
            matrix.append(matrix_row)
        return Matrix(matrix)
    except Exception as e:
        st.error(f"Invalid matrix input: {e}")
        return None

# Display matrix in LaTeX and as a table
def display_matrix(matrix, label):
    st.markdown(f"**{label}:**")
    st.latex(latex(matrix))
    df = pd.DataFrame(matrix.tolist())
    st.dataframe(df, use_container_width=True)

# Parse matrices
A = parse_matrix(A_input) if A_input else None
B = parse_matrix(B_input) if B_input else None

if st.button("Compute"):
    if A:
        display_matrix(A, "Matrix A")
        if A.is_square:
            if A.det() != 0:
                try:
                    InvA = A.inv()
                    display_matrix(InvA, "Inverse of A")
                except Exception as e:
                    st.error(f"Error computing inverse of A: {e}")
            else:
                st.warning("Matrix A is not invertible (det = 0)")
        else:
            st.warning("Matrix A is not square, so it cannot be inverted.")

    if B:
        display_matrix(B, "Matrix B")
        if B.is_square:
            if B.det() != 0:
                try:
                    InvB = B.inv()
                    display_matrix(InvB, "Inverse of B")
                except Exception as e:
                    st.error(f"Error computing inverse of B: {e}")
            else:
                st.warning("Matrix B is not invertible (det = 0)")
        else:
            st.warning("Matrix B is not square, so it cannot be inverted.")

    if A and B:
        try:
            if A.shape[1] == B.shape[0]:
                AB = A * B
                display_matrix(AB, "A × B")
            else:
                st.warning(f"A × B not possible: A has {A.shape[1]} columns but B has {B.shape[0]} rows.")
        except Exception as e:
            st.error(f"Error computing A × B: {e}")

        try:
            if B.shape[1] == A.shape[0]:
                BA = B * A
                display_matrix(BA, "B × A")
            else:
                st.warning(f"B × A not possible: B has {B.shape[1]} columns but A has {A.shape[0]} rows.")
        except Exception as e:
            st.error(f"Error computing B × A: {e}")
