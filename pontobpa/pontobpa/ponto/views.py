from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Marcacao
from datetime import datetime, timedelta
from django.utils import timezone
from .forms import MeuForm
from .models import Marcacao
from .models import MarcacoesPorDia
from django.contrib.auth.models import User
from django.http import HttpResponse
import xlwt
from django.db.models import Q

@login_required
def marcarPonto(request):
    return render(request, 'marcarPonto.html')


@login_required
def marcacaoRealizada(request):
    marcacao = Marcacao()
    marcacao.nome_usuario = request.user
    marcacao.id_usuario = request.user.id
    marcacao.data_marcacao = timezone.now()
    marcacao.save()
    return render(request, 'marcacaoComSucesso.html')


@login_required
def confirmarMarcacao(request):
    dataHoraAtual = timezone.now()
    return render(request, 'confirmarMarcacao.html', {'dataHoraAtual': dataHoraAtual})


@login_required
def visualizarMarcacoes(request):
    dataInicio = ""
    dataFim = ""
    idFuncionario = ""
    cartaoPonto = []

    if request.method == 'POST':
        try:
            userName = request.user.username
            dataInicio = request.POST['dataInicio']
            dataFim = request.POST['dataFim']
            if (userName == 'bpa'):
                idFuncionario = request.POST['Funcionarios']
            else:
                idFuncionario = request.user.id

            dataFimDate = datetime.strptime(dataFim, '%Y-%m-%d').date()
            dataFimDate = dataFimDate + timedelta(days=1)

            marcacoes = Marcacao.objects.filter(Q(id_usuario=idFuncionario), data_marcacao__gte=dataInicio,
                                                data_marcacao__lte=dataFimDate)

            marcacoesAux = marcacoes

            marcacoesDia = MarcacoesPorDia()

            i = 0
            x = 1
            sizeLista = len(marcacoes)
            while i < len(marcacoes):
                dataStr = marcacoes[i].data_marcacao.strftime('%d/%m/%Y')
                if (x < sizeLista):
                    dataAuxStr = marcacoes[x].data_marcacao.strftime('%d/%m/%Y')
                else:
                    dataAuxStr = ""
                horaStr = marcacoes[i].data_marcacao.strftime('%H:%M')

                if (dataStr != ""):
                    if (dataStr == dataAuxStr):
                        marcacoesDia.marcacoes += (horaStr,)
                        i = i + 1
                        x = x + 1
                    else:
                        marcacoesDia.marcacoes += (horaStr,)
                        marcacoesDia.dia_marcacoes = dataStr
                        cartaoPonto.append(marcacoesDia)
                        marcacoesDia = MarcacoesPorDia()
                        i = i + 1
                        x = x + 1
        except:
            pass
    userName = request.user.username
    if (userName == "bpa"):
        contexto = {
            'meu_form': MeuForm(),
            'cartaoPonto': cartaoPonto
        }
    else:
        contexto = {
            'cartaoPonto': cartaoPonto
        }
    return render(request, 'visualizarMarcacoes.html', contexto)


@login_required
def pontoManual(request):
    return render(request, 'pontoManual.html')


@login_required
def marcacaoManual(request):
    horarioMarcacao = ""
    dataMarcacao = ""
    marcacao = Marcacao()
    marcacao.nome_usuario = request.user
    marcacao.id_usuario = request.user.id
    try:
        if request.method == 'POST':
            horarioMarcacao = request.POST['horarioMarcacao']
            dataMarcacao = request.POST['dataMarcacao']

            if (horarioMarcacao == "" or dataMarcacao == ""):
                return render(request, 'pontoManual.html')
        marcacao.data_marcacao = dataMarcacao + " " + horarioMarcacao
        marcacao.save()
    except:
        pass

    return render(request, 'marcacaoComSucesso.html')


def export_xls(request, cartaoPontoExcel, dataInicio, dataFim):

    if(dataInicio != "" or dataFim != "" ):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="cartaoPonto.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Marcacoes')
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['NOME', 'DATA', 'MARCACOES', ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()


        i = 0
        linha = 1
        coluna = 0
        colunaMarcacao = 2
        while i < len(cartaoPontoExcel):
            ws.write(linha, coluna, cartaoPontoExcel[i].nome_funcionario)
            ws.write(linha, coluna + 1, cartaoPontoExcel[i].dia_marcacoes)
            x = 0
            while (x < len(cartaoPontoExcel[i].marcacoes)):
                ws.write(linha, colunaMarcacao, cartaoPontoExcel[i].marcacoes[x])
                colunaMarcacao = colunaMarcacao + 1
                x = x + 1
            i = i + 1
            colunaMarcacao = 2
            linha = linha + 1

        wb.save(response)

        return response
    return render(request, 'exportarMarcacoesXLS.html')


def pageExportExcel(request):
    return render(request, 'exportarMarcacoesXLS.html')

def filtro_export_xls(request):
    cartaoPontoExcel = []
    dataInicio = ""
    dataFim = ""
    idFuncionario = ""

    if request.method == 'POST':
        try:
            userName = request.user.username
            dataInicio = request.POST['dataInicio']
            dataFim = request.POST['dataFim']


            dataFimDate = datetime.strptime(dataFim, '%Y-%m-%d').date()
            dataFimDate = dataFimDate + timedelta(days=1)



            marcacoes = Marcacao.objects.filter(data_marcacao__gte=dataInicio,
                                                data_marcacao__lte=dataFimDate).order_by('nome_usuario')

            marcacoesAux = marcacoes

            marcacoesDia = MarcacoesPorDia()

            i = 0
            x = 1
            sizeLista = len(marcacoes)

            while i < len(marcacoes):
                dataStr = marcacoes[i].data_marcacao.strftime('%d/%m/%Y')
                nomeFuncionario =  marcacoes[i].nome_usuario
                if (x < sizeLista):
                    dataAuxStr = marcacoes[x].data_marcacao.strftime('%d/%m/%Y')
                else:
                    dataAuxStr = ""
                horaStr = marcacoes[i].data_marcacao.strftime('%H:%M')

                if (dataStr != ""):
                    if (dataStr == dataAuxStr):
                        marcacoesDia.marcacoes += (horaStr,)
                        i = i + 1
                        x = x + 1
                    else:
                        marcacoesDia.marcacoes += (horaStr,)
                        marcacoesDia.dia_marcacoes = dataStr
                        marcacoesDia.nome_funcionario = nomeFuncionario
                        cartaoPontoExcel.append(marcacoesDia)
                        marcacoesDia = MarcacoesPorDia()
                        i = i + 1
                        x = x + 1


        except:
            pass
    return export_xls(request, cartaoPontoExcel, dataInicio, dataFim)