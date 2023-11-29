import tkinter as tk
from tkinter.simpledialog import askinteger, askstring
from tkinter import messagebox
from neo4j import GraphDatabase
import datetime

class Neo4jCRUD:
    def __init__(self, uri, username, password):
        self._uri = uri
        self._username = username
        self._password = password
        self._driver = None

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._username, self._password))

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def show_list(self, title, items, width=600, height=100):
        list_window = tk.Toplevel(root)
        list_window.title(title)

        listbox = tk.Listbox(list_window)
        for item in items:
            listbox.insert(tk.END, item)

        listbox.pack(fill=tk.BOTH, expand=True)

        list_window.geometry(f"{width}x{height}")
        
    def create_department(self, dept_no, dname, loc):
        query = f"CREATE (d:Dept {{DEPTNO: {dept_no}, DNAME: '{dname}', LOC: '{loc}'}})"
        with self._driver.session() as session:
            try:
                session.run(query)
                print(f"Departamento con número {dept_no} agregado exitosamente.")
            except Exception as e:
                print(f"Error al agregar el departamento con número {dept_no}: {e}")

    def show_departments(self):
        query = "MATCH (d:Dept) RETURN d.DEPTNO, d.DNAME, d.LOC"
        with crud._driver.session() as session:
            result = session.run(query)
            departments = [f"DeptNo: {record['d.DEPTNO']}, Name: {record['d.DNAME']}, Location: {record['d.LOC']}" for record in result]
            crud.show_list("Departments", departments)

    def update_department(self, dept_no, new_dname, new_loc):
        query = f"MATCH (d:Dept {{DEPTNO: {dept_no}}}) SET d.DNAME = '{new_dname}', d.LOC = '{new_loc}'"
        with self._driver.session() as session:
            session.run(query)

    def delete_department(self, dept_no):
        query = f"MATCH (d:Dept {{DEPTNO: {dept_no}}}) DETACH DELETE d"
        with self._driver.session() as session:
            session.run(query)

    def create_employee(self, emp_no, ename, job, mgr, hire_date, sal, comm, dept_no):
        query = (
            f"CREATE (e:Emp {{EMPNO: {emp_no}, ENAME: '{ename}', JOB: '{job}', MGR: {mgr}, "
            f"HIREDATE: date('{hire_date}'), SAL: {sal}, COMM: {comm}, DEPTNO: {dept_no}}})"
        )
        with self._driver.session() as session:
            session.run(query)
        query2 = (
            f"MATCH (e1:Emp {{EMPNO: {emp_no}}}), (d1:Dept {{DEPTNO: {dept_no}}}) CREATE (e1)-[:WORKS_FOR]->(d1)"
        )
        with self._driver.session() as session:
            session.run(query2)

    def show_employees(self):
        query = "MATCH (e:Emp) RETURN e.EMPNO, e.ENAME, e.JOB"
        with crud._driver.session() as session:
            result = session.run(query)
            employees = [f"EmpNo: {record['e.EMPNO']}, Name: {record['e.ENAME']}, Job: {record['e.JOB']}" for record in result]
            crud.show_list("Employees", employees)

    def update_employee(self, emp_no, ename, job, mgr, hire_date, sal, comm, dept_no):
        query = (
            f"MATCH (e1:Emp)-[r:WORKS_FOR]->(:Dept) WHERE e1.EMPNO = {emp_no} DELETE r"
        )
        with self._driver.session() as session:
            session.run(query)
        query2 = f"MATCH (e:Emp {{EMPNO: {emp_no}}}) SET e.ENAME = '{ename}', e.HIREDATE = '{hire_date}', e.JOB ='{job}', e.MGR = '{mgr}', e.SAL = '{sal}',e.COMM = '{comm}'"
        with self._driver.session() as session:
            session.run(query2)
        query3 = (
            f"MATCH (e1:Emp {{EMPNO: {emp_no}}}), (d1:Dept {{DEPTNO: {dept_no}}}) CREATE (e1)-[:WORKS_FOR]->(d1)"
        )
        with self._driver.session() as session:
            session.run(query3)

    def delete_employee(self, emp_no):
        query = f"MATCH (e:Emp {{EMPNO: {emp_no}}}) DETACH DELETE e"
        with self._driver.session() as session:
            session.run(query)

    def noEmp_depto(self, deptno):
        query = f"MATCH (e:Emp)-[:WORKS_FOR]->(d:Dept {{DEPTNO: {deptno}}}) RETURN COUNT(e) AS no_of_employees"
        with self._driver.session() as session:
            result = session.run(query)
            return result.single()["no_of_employees"]
        

# Configuración de Neo4j
neo4j_uri = "bolt://localhost:7687"  # Reemplaza con tu URI de Neo4j
neo4j_user = "neo4j"  # Reemplaza con tu usuario de Neo4j
neo4j_password = "basesdedatos"  # Reemplaza con tu contraseña de Neo4j

# Instancia del manejador de Neo4j
crud = Neo4jCRUD(uri=neo4j_uri, username=neo4j_user, password=neo4j_password)
crud.connect()

# tkinter
root = tk.Tk()
root.title("Sistema de Gestión de Departamentos y Empleados")

# ComboBox 
action_var = tk.StringVar(root)
action_var.set("Seleccione una acción")
actions = [
    "Agregar Departamento",
    "Mostrar Departamentos",
    "Actualizar Departamento",
    "Borrar Departamento",
    "Agregar Empleado",
    "Mostrar Empleados",
    "Actualizar Empleado",
    "Eliminar Empleado",
    "Número de Empleados por Departamento"
]
action_combobox = tk.OptionMenu(root, action_var, *actions)
action_combobox.pack()

def execute_action():
    selected_action = action_var.get()
    
    if selected_action == "Agregar Departamento":
        deptno = askinteger("Agregar Departamento", "Número de departamento:")
        if deptno is not None:
            dname = askstring("Agregar Departamento", "Nombre:")
            if dname is not None:
                loc = askstring("Agregar Departamento", "Ubicación:")
                if loc is not None:
                        crud.create_department(deptno, dname, loc)
                        messagebox.showinfo("Notificación",("El departamento con número: " + str(deptno) +" ha sido agregado "))
    elif selected_action == "Mostrar Departamentos":
        crud.show_departments()
    elif selected_action == "Actualizar Departamento":
        deptno = askinteger("Actualizar Departamento", "Número de departamento a actualizar:")
        if deptno is not None:
            new_dname = askstring("Actualizar Departamento", "Nuevo nombre:")
            if new_dname is not None:
                new_loc = askstring("Actualizar Departamento", "Nueva ubicación:")
                if new_loc is not None:
                    crud.update_department(deptno, new_dname, new_loc)
                    messagebox.showinfo("Notificación",("El departamento con número: " + str(deptno) +" ha sido actualizado "))
    elif selected_action == "Borrar Departamento":
        deptno = askinteger("Borrar Departamento", "Número de departamento a borrar:")
        if deptno is not None:
            crud.delete_department(deptno)
            messagebox.showinfo("Notificación",("El departamento con número: " + str(deptno) +" ha sido eliminado "))
    elif selected_action == "Agregar Empleado":
        empno = askinteger("Agregar Empleado", "Número de empleado:")
        if empno is not None:
            ename = askstring("Agregar Empleado", "Nombre de empleado:")
            if ename is not None:
                job = askstring("Agregar Empleado", "Nombre trabajo:")
                if job is not None:
                    mgr = askinteger("Agregar Empleado", "Número del manager:")
                    if mgr is not None:
                        hiredate = askstring("Agregar Empleado", "Ingresa la fecha con el siguiente formato: YYYY-MM-DD:")
                        if hiredate is not None:
                            hiredate = datetime.datetime.strptime(hiredate, "%Y-%m-%d")
                            hiredate = hiredate.strftime("%Y-%m-%d")
                            sal = askinteger("Agregar Empleado", "Salario:")
                            if sal is not None:
                                comm = askinteger("Agregar Empleado", "Comisión:")
                                if comm is not None:
                                    deptno = askinteger("Agregar Empleado", "Número de departamento:")
                                    if deptno is not None:
                                        crud.create_employee(empno, ename, job, mgr, hiredate, sal, comm, deptno)
                                        messagebox.showinfo("Notificación",("El empleado con número: " + str(empno) +" ha sido agregado "))
    elif selected_action == "Mostrar Empleados":
        crud.show_employees()
    elif selected_action == "Actualizar Empleado":
        empno = askinteger("Actualizar Empleado", "Número de empleado:")
        if empno is not None:
            new_ename = askstring("Actualizar Empleado", "Nombre de empleado:")
            if new_ename is not None:
                new_job = askstring("Actualizar Empleado", "Nombre trabajo:")
                if new_job is not None:
                    new_mgr = askinteger("Actualizar Empleado", "Número del manager:")
                    if new_mgr is not None:
                        new_hiredate = askstring("Actualizar Empleado", "Ingresa la fecha con el siguiente formato: YYYY-MM-DD:")
                        if new_hiredate is not None:
                            new_hiredate = datetime.datetime.strptime(new_hiredate, "%Y-%m-%d")
                            new_hiredate = new_hiredate.strftime("%Y-%m-%d")
                            new_sal = askinteger("Actualizar Empleado", "Salario:")
                            if new_sal is not None:
                                new_comm = askinteger("Actualizar Empleado", "Comisión:")
                                if new_comm is not None:
                                    new_deptno = askinteger("Actualizar Empleado", "Número de departamento:")
                                    if new_deptno is not None:
                                        crud.update_employee(empno, new_ename, new_job, new_mgr, new_hiredate, new_sal, new_comm, new_deptno)
                                        messagebox.showinfo("Notificación",("El empleado con número: " + str(empno) +" ha sido actualizado "))
    elif selected_action == "Eliminar Empleado":
        empno = askinteger("Eliminar Empleado", "Número de empleado a borrar:")
        if empno is not None:
            crud.delete_employee(empno)
            messagebox.showinfo("Notificación",("El empleado con número: " + str(empno) +" ha sido eliminado "))
    elif selected_action == "Número de Empleados por Departamento":
        deptno = askinteger("Número de Empleados por Departamento", "Número de departamento:")
        if deptno is not None:
            noed = crud.noEmp_depto(deptno)
            messagebox.showinfo("Notificación",("El número de empleados del departamento: " + str(deptno) +" es: " + str(noed)))

execute_button = tk.Button(root, text="Ejecutar Acción", command=execute_action)
execute_button.pack()

root.geometry("600x300")
root.geometry("+300+100") 

root.mainloop()

# Cierre del manejador de Neo4j al salir de la aplicación
crud.close()