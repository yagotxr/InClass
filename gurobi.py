# -*- coding: utf-8 -*-
import gurobipy as grb
from gurobipy import GRB

model = grb.Model("model")

disciplinas = ['dis1', 'dis2', 'dis3', 'dis4', 'dis5', 'dis6']
demanda_disciplina = [5, 10, 15, 9, 20, 17]
horarios = [0, 1, 2, 3]
salas = ['sala1', 'sala2', 'sala3', 'sala4']
cadeiras = [20, 30, 40, 50]

horario = ([0, 1, 0, 0],
           [1, 0, 1, 0],
           [0, 0, 1, 0],
           [0, 0, 1, 1],
           [1, 0, 0, 0],
           [1, 1, 1, 1])

x = [[[0 for A in range(0, len(salas))] for B in range(0, len(horarios))] for C in range(0, len(disciplinas))]

s_mais = [[[0 for D in range(0, len(salas))] for E in range(0, len(horarios))] for F in range(0, len(disciplinas))]

s_menos = [[[0 for G in range(0, len(salas))] for H in range(0, len(horarios))] for I in range(0, len(disciplinas))]

v = [[0 for J in range(0, len(salas))] for K in range(0, len(disciplinas))]

t = [0 for L in range(0, len(disciplinas))]

try:
    for i in range(0, len(disciplinas)):
        for j in range(0, len(horarios)):
            for k in range(0, len(salas)):
                x[i][j][k] = model.addVar(0.0, 1.0, 0.0, GRB.BINARY, name="x %d" %k)
                s_mais[i][j][k] = model.addVar(0.0, GRB.INFINITY, 0.0, GRB.CONTINUOUS, name="smais %d" %k)
                s_menos[i][j][k] = model.addVar(0.0, GRB.INFINITY, 0.0, GRB.CONTINUOUS, name="smenos %d" %k)

    for i in range(0, len(disciplinas)):
        for k in range(0, len(salas)):
            v[i][k] = model.addVar(0.0, GRB.INFINITY, 0.0, GRB.CONTINUOUS, name="v %d" %k)

    # Restricao 3
    for i in range(0, len(disciplinas)):
        for j in range(0, len(horarios)):
            for k in range(0, len(salas)):
                expr = grb.LinExpr(0.0)
                expr = (cadeiras[k] - demanda_disciplina[i] * x[i][j][k] + s_mais[i][j][k] - s_menos[i][j][k])
                model.addConstr(expr, GRB.EQUAL, 0.0)

    # Restrição 4
    for k in range(0, len(salas)):
        for j in range(0, len(horarios)):
            expr = grb.LinExpr(0.0)
            for i in range(0, len(disciplinas)):
                expr = expr + x[i][j][k]
            model.addConstr(expr, GRB.LESS_EQUAL, 1.0)

    # Restriçao 5
    for i in range(0, len(disciplinas)):
        for j in range(0, len(horarios)):
            expr = grb.LinExpr(0.0)
            for k in range(0, len(salas)):
                expr = expr + x[i][j][k]
            model.addConstr(expr, GRB.EQUAL, horario[i][j])

    # Restrição 6
    for i in range(0, len(disciplinas)):
        for j in range(0, len(horarios)):
            for k in range(0, len(salas)):
                model.addConstr(x[i][j][k] - v[i][k], GRB.LESS_EQUAL, 0.0)

    # Restrição 7
    for i in range(0, len(disciplinas)):
        expr = grb.LinExpr(0.0)
        for k in range(0, len(salas)):
            expr = expr + v[i][k]
        expr = expr - 1
        model.addConstr(t[i], GRB.GREATER_EQUAL, expr)

    expr = grb.LinExpr(0.0)
    penalidade_cadeira_faltando = 50
    penalidade_cadeira_sobrando = 5
    penalidade_excesso_sala = 1

    for i in range(0, len(disciplinas)):
        expr = expr + (penalidade_excesso_sala * t[i])
        for j in range(0, len(horarios)):
            for k in range(0, len(salas)):
                expr = expr + (penalidade_cadeira_faltando * s_mais[i][j][k]) + (
                            penalidade_cadeira_sobrando * s_menos[i][j][k])

    model.setObjective(expr, GRB.MINIMIZE)

    model.update()
    # Optimize model
    model.optimize()

    # for v in model.getVars():
    #     print('%s %g' % (v.varName, v.x))
    oi = 0
    for i in range(0, len(disciplinas)):
        for j in range(0, len(horarios)):
            for k in range(0, len(salas)):
                if x[i][j][k].x > 0.5:
                    print("Discplina "+ disciplinas[i]+" esta alocada na sala "+ salas[k]+ " " + str(horarios[j]))
                    oi += 1

    print('Obj: %g' % model.objVal)

except grb.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
