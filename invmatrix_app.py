import streamlit as st
import numpy as np

st.title("Matrix Operations: Inverse and Multiplication")

st.markdown("""
Enter matrices A and B in Python list format. Example:  
`[[1, 2], [3, 4]]`
""")

# Matrix A input
A_input = st.text_area("Matrix A", height=100)
# Matrix B input
B_input = st.text_area("Matrix B", height=100)

def parse_matrix(input_text):
    try:
        matrix = np.array(eval(input_text), dtype=float)
        if matrix.ndim != 2:
            raise ValueError("Matrix must be 2D")
        return matrix
    except Exception as e:
        st.error(f"Invalid matrix input: {e}")
        return None

A = parse_matrix(A_input) if A_input else None
B = parse_matrix(B_input) if B_input else None

# Perform actions
if st.button("Compute"):
    if A is not None:
        st.subheader("Matrix A")
        st.write(A)

        try:
            InvA = np.linalg.inv(A)
            st.success("Inverse of A:")
            st.write(InvA)
        except np.linalg.LinAlgError:
            st.warning("Matrix A is not invertible.")

    if B is not None:
        st.subheader("Matrix B")
        st.write(B)

        try:
            InvB = np.linalg.inv(B)
            st.success("Inverse of B:")
            st.write(InvB)
        except np.linalg.LinAlgError:
            st.warning("Matrix B is not invertible.")

    # Products
    if A is not None and B is not None:
        try:
            AB = np.dot(A, B)
            st.subheader("A × B")
            st.write(AB)
        except ValueError as e:
            st.error(f"A × B not computable: {e}")

        try:
            BA = np.dot(B, A)
            st.subheader("B × A")
            st.write(BA)
        except ValueError as e:
            st.error(f"B × A not computable: {e}")
