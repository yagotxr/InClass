from gurobipy import *
from gurobipy.gurobipy import Model


def set_args():
    pass


"""
ESSA FUNÇÃO PEGA OS VALORES POR PARAMETRO, NÃO SEI SE É PELA URL OU POR CMD 

void setArgs(int argc, char** argv) {
    //opcoes de entrada terminal
    struct option OpcoesLongas[] = {
            {"ajuda", no_argument, NULL, 'h'},
            {"codigo do ensalamento", required_argument, NULL, 'e'},
            {"ano para ensalamento", required_argument, NULL, 'a'},
            {"semestre para ensalamento", required_argument, NULL, 's'},
            {"arquivo sala", required_argument, NULL, 'r'},
            {0, 0, 0, 0}
    };

    char optc = 0;  // Parece estranho... Mas todo CHAR é na verdade um INT
    while((optc = getopt_long(argc, argv, "h:e:a:s:r", OpcoesLongas, NULL)) != -1) {
            switch(optc) {
                case 'h' : 
                    break;                                   
                case 'e' :
                    strcpy(param_ensalamentoID, optarg);
                    break;
                case 'a':
                    strcpy(param_ano, optarg);
                    break;
                case 's' :
                    strcpy(param_semestre, optarg);
                    break;
                case 'r' :
                    break;    
                default :
                    printf("Parametros incorretos.\n");
            }
    }
}

"""

r = [][][] # número de alunos acima do limite de 60
s_p = [][][] # número de alunos que ultrapassa capacidade da sala
s_n = [][][] # número da capacidade que ultrapassa a demanda
x = [][][] # alocação de turmas (1 ou 0)
t = [] # número de salas diferentes que uma sala foi alocada
v = [][] # alocação de disciplina em sala


def set_funcoes_restricoes(model):
    for i in range(num_turmas):
        for j in range(num_horarios):
        # GRBLinExpr alocar_aula
            for k in range(num_salas):
        # restrição 1
        # model->addConstr( ((x[i][j][k]*demanda[i]) * (1-salas.at(k)->GetArCondicionado())) - 60 - r[i][j][k] <= 0);
                model.addConstr((x[i][j][k] * demanda[i]) * (1-salas[k].GetArCondicionado())- 60 - r[i][j][k] <= 0)
        # restrição 2
        # model->addConstr( x[i][j][k]*(salas.at(k)->GetCapacidade() - demanda[i]) + s_p[i][j][k] - s_n[i][j][k] == 0);
                model.addConstr(x[i][j][k] * (salas[k].GetCapaciadade() - demanda[i]) + s_p[i][j][k] - s_n[i][j][k] == 0)
        # restrição 3
        # model->addConstr(x[i][j][k] - v[i][k] <= 0);
                model.addConstr(model.x[i][j][k] - model.v[i][k] <= 0)
        # construção restrições 4
        # alocar_aula += x[i][j][k]
                alocar_aula += x[i][j][k]
        # conjunto de restrições 4
        # model->addConstr(alocar_aula == horario[i][j])
                model.addConstr(alocar_aula == horarios[i][j])
    for j in range(num_horarios):
        for k in range(num_salas):
            # GRBLinExpr uma_turma_sala_horario
            for i in range(num_turmas):
                uma_turma_sala_horario.AddTerm(x[i][j][k])
        # model->addConstr(uma_turma_sala_horario <= 1)
                model.addConstr(uma_turma_sala_horario <= 1)
    for i in range(num_turmas):
        # GRBLinExpr qtde_sala_utilizada_por_turma;
        for k in range(num_salas):
            qtde_sala_utilizada_por_turma.AddTerm(v[i][k])

        qtde_sala_utilizada_por_turma.AddTerm(-1)
    # model->addConstr(qtde_sala_utilizada_por_turma <= t[i]);
        model.addConstr(qtde_sala_utilizada_por_turma <= t[i])

## ACHO QUE ESSE METODO TA ERRADO...
def init_vars(model):
    # Create variables
    r = model.addVar(vtype=GRB.INTEGER, name="r")  # número de alunos acima do limite de 60
    s_p = model.addVar(vtype=GRB.INTEGER, name="sp_p")  # número de alunos que ultrapassa capacidade da sala
    s_n = model.addVar(vtype=GRB.INTEGER, name="s_n")  # número da capacidade que ultrapassa a demanda
    x = model.addVar(vtype=GRB.INTEGER, name="x")  # alocação de turmas (1 0u 0)
    t = model.addVar(vtype=GRB.INTEGER, name="t")  # número de salas diferentes que uma sala foi alocada
    v = model.addVar(vtype=GRB.INTEGER, name="v")  # alocação de disciplina em sala

    for i in range(num_turmas):

        # r[i] = new GRBVar * [num_horarios]
        r[i] = model.addVar(vtype=GRB.INTEGER)
        # s_p[i] = new GRBVar * [num_horarios]
        s_p[i] = model.addVar(vtype=GRB.INTEGER)
        # s_n[i] = new GRBVar * [num_horarios]
        s_n[i] = model.addVar(vtype=GRB.INTEGER)
        # x[i] = new GRBVar * [num_horarios]
        x[i] = model.addVar(vtype=GRB.INTEGER)

        for j in range(num_horarios):
            #r[i][j] = new GRBVar[num_salas]
            # s_p[i][j] = new GRBVar[num_salas]
            # s_n[i][j] = new GRBVar[num_salas]
            #x[i][j] = new GRBVar[num_salas]

            for k in range(num_salas):
                # r[i][j][k] = model->addVar(0.0, GRB_INFINITY, 0.0, GRB_CONTINUOUS)
                r[i][j][k] = model.addVar(0.0, GRB.INFINITY, 0.0, GRB.CONTINUOUS)
                # s_p[i][j][k] = model->addVar(0.0, GRB_INFINITY, 0.0, GRB_CONTINUOUS)
                s_p[i][j][k] = model.addVar(0.0, GRB.INFINITY, 0.0, GRB.CONTINUOUS)
                # s_n[i][j][k] = model->addVar(0.0, GRB_INFINITY, 0.0, GRB_CONTINUOUS)
                s_n[i][j][k] = model.addVar(0.0, GRB.INFINITY, 0.0, GRB.CONTINUOUS)
                # x[i][j][k] = model->addVar(0.0, 1.0, 0.0, GRB_BINARY)
                x[i][j][k] = model.addVar(0.0, 1.0, 0.0, GRB.BINARY)
    # t = new GRBVar[num_turmas]  #número de salas diferentes que uma sala foi alocada
    # v = newGRBVar * [num_turmas]
    for i in range(num_turmas):
        # t[i] = model->addVar(0.0, GRB_INFINITY, 0.0, GRB_CONTINUOUS);
        t[i] = model.addVar(0.0, GRB.INFINITY, 0.0, GRB.CONTINUOUS)
        # v[i] = new GRBVar[num_salas];
        for k in range(num_salas):
            # v[i][k] = model->addVar(0.0, GRB_INFINITY, 0.0, GRB_CONTINUOUS);
            v[i][k] = model.addVar((0.0, GRB.INFINITY, 0.0, GRB.CONTINUOUS))

def set_funcao_objetivo(model):
    alpha1 = 100.0
    alpha2 = 100.0
    alpha3 = 100.0


# Git de exemplo https://github.com/rocarvalho/ensalamento-interface-gurobi/blob/master/main.cpp
model: Model = Model("InClass")

num_horarios = 14
num_turmas = 0
num_salas = 0

salas = []
horarios = []

param_ensalamentoID = [30]
param_ano = [30]
param_semestre = [30]


url = 'vem aqui nossa api'


def main(argc, argv):
    set_args(argc, argv)

    get_horarios = []  # na verdade vamos fazer uma função para buscar no banco
    get_salas = []  # na verdade vamos fazer uma função para buscar no banco

    num_salas = salas.size()
    num_turmas = horarios.size()
    demanda = int([num_turmas])

    # cria matriz (turmas x horarios) e aloca 0 para cada elemento
    horario = [num_turmas]

    for i in range(num_turmas):
        horario[i] = int([num_horarios])
        for j in range(num_horarios):
            horario[i][j] = 0

    # aloca demanda de turma em vetor demanda e aloca turma em mapper que indica posição de turma

    turmas = []
    map (horarios, turmas) # Verificar se esta correto
    for i in range(num_turmas):
        turmas[i] = horarios[i]

        # demanda[i] = horarios[i]->GetAlunos_qtd(); não sei como traduzir ponteiro :´(

    #Converte horaio e dia em um valor de 0 até 13
        temp_horario = 0 # ((horarios[i]->GetDia() - 1) * 2  + horarios[i]->GetHorario()) - 1;
        horario[i][temp_horario] = 1

try:
    #GRBEnv env = GRBEnv()

    model: Model = Model("InClass")

    init_vars(model)
    set_funcao_objetivo(model)
    set_funcoes_restricoes()

    # Optimize model
    model.update()
    model.optimize()

    #Json::Value ensalamentosArr(Json::arrayValue)

    for i in range(num_turmas):
        for j in range(num_horarios):
            for k in range(num_salas):
                #if (x[i][j][k].get(GRB_DoubleAttr_X) > 0.5) {
            # if(x[i][j][k].get(GRB.DO))
                #    for (map < int, Horario * iterator pos = turmas.begin(); pos != turmas.end(); pos + +) {
                 #       if (pos->first == i) {
                  #          pos->second->SetSala(salas.at(k));
                   #         ensalamentosArr.append(pos->second->GetJson());
        pass

    # Json::Value root(Json::objectValue)

    #root["ensalamentos"] = ensalamentosArr

    url_horario = url + "ensalamentos/"
    url_horario += param_ensalamentoID
    url_horario += "/ensalar"
    # responseJson = HttpRequests::post(urlHorario, root);
    # cout << responseJson;

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')